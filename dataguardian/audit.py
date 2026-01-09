"""Privacy audit engine for DataGuardian (stdlib-only)."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from typing import List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import build_opener, Request, HTTPCookieProcessor

from dataguardian.models import AuditResult, TrackerFinding

LOGGER = logging.getLogger(__name__)

TRACKER_SIGNATURES = {
    "google-analytics.com": "Google Analytics",
    "googletagmanager.com": "Google Tag Manager",
    "doubleclick.net": "DoubleClick",
    "facebook.net": "Meta Pixel",
    "connect.facebook.net": "Meta Pixel",
    "hotjar.com": "Hotjar",
    "clarity.ms": "Microsoft Clarity",
    "segment.com": "Segment",
    "mixpanel.com": "Mixpanel",
    "cdn.segment.com": "Segment",
    "snapchat.com": "Snap Pixel",
    "tiktok.com": "TikTok Pixel",
}

TRACKER_KEYWORDS = [
    "track",
    "analytics",
    "pixel",
    "beacon",
    "advertising",
    "remarketing",
]

HTML_ATTRS_TO_SCAN = {
    "script": ["src"],
    "img": ["src", "data-src"],
    "iframe": ["src"],
    "link": ["href"],
}


@dataclass(frozen=True)
class AuditInput:
    url: str
    html: str
    cookies: dict


class _HTMLTrackerParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.matches: List[Tuple[str, str, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag not in HTML_ATTRS_TO_SCAN:
            return
        for attr in HTML_ATTRS_TO_SCAN[tag]:
            value = attrs_dict.get(attr)
            if value:
                self.matches.append((tag, attr, value))


class AuditEngine:
    """Runs deterministic privacy audits against HTML content."""

    def __init__(self, timeout_seconds: int = 10, user_agent: str = "DataGuardian/1.0"):
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def fetch(self, url: str) -> AuditInput:
        headers = {"User-Agent": self.user_agent}
        LOGGER.info("Fetching URL for audit", extra={"url": url})
        cookie_jar = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie_jar))
        request = Request(url, headers=headers)
        with opener.open(request, timeout=self.timeout_seconds) as response:
            html = response.read().decode("utf-8", errors="replace")
        cookies = {cookie.name: cookie.value for cookie in cookie_jar}
        return AuditInput(url=url, html=html, cookies=cookies)

    def audit(self, *, url: Optional[str] = None, html: Optional[str] = None, source_label: Optional[str] = None) -> AuditResult:
        if not url and not html:
            raise ValueError("Provide either url or html for auditing")
        if url and html:
            raise ValueError("Provide only one of url or html")

        if url:
            audit_input = self.fetch(url)
        else:
            label = source_label or "inline-html"
            audit_input = AuditInput(url=label, html=html or "", cookies={})

        findings, third_party_domains = self._analyze_html(audit_input.html, audit_input.url)
        trackers = len(findings)
        cookies = len(audit_input.cookies)
        risk_score = self._calculate_risk_score(trackers, cookies, third_party_domains)

        result = AuditResult(
            url=audit_input.url,
            scanned_at=datetime.now(timezone.utc),
            trackers=trackers,
            cookies=cookies,
            third_party_domains=third_party_domains,
            risk_score=risk_score,
            findings=findings,
        )
        return result

    def _analyze_html(self, html: str, url: str) -> Tuple[List[TrackerFinding], int]:
        parser = _HTMLTrackerParser()
        parser.feed(html)
        base_domain = self._extract_domain(url)

        findings: List[TrackerFinding] = []
        third_party_domains: set[str] = set()

        for tag_name, attr, value in parser.matches:
            normalized = value.lower()
            reason = self._match_tracker_reason(normalized)
            if reason:
                findings.append(
                    TrackerFinding(
                        tag=tag_name,
                        attribute=attr,
                        value=value,
                        reason=reason,
                    )
                )
            domain = self._extract_domain(value)
            if domain and base_domain and domain != base_domain:
                third_party_domains.add(domain)

        return findings, len(third_party_domains)

    def _match_tracker_reason(self, value: str) -> Optional[str]:
        for signature, label in TRACKER_SIGNATURES.items():
            if signature in value:
                return label
        for keyword in TRACKER_KEYWORDS:
            if keyword in value:
                return f"Keyword match: {keyword}"
        return None

    def _calculate_risk_score(self, trackers: int, cookies: int, third_party_domains: int) -> int:
        score = trackers * 10 + cookies * 2 + third_party_domains * 5
        return min(score, 100)

    def _extract_domain(self, url: str) -> Optional[str]:
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return parsed.netloc.lower()
        if "//" in url:
            parsed = urlparse(f"https:{url}")
            return parsed.netloc.lower()
        if url.startswith("www."):
            return url.split("/")[0].lower()
        return None


def serialize_result(result: AuditResult) -> str:
    """Convert an AuditResult into JSON for storage."""

    return json.dumps(result.to_dict(), default=str)
