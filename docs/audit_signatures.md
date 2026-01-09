# Audit Signature Catalog

This catalog documents the tracking signatures used by the audit engine. The
entries are grouped to help auditors validate why a tracker was flagged.

## Known analytics vendors

| Signature | Vendor | Notes |
| --- | --- | --- |
| `google-analytics.com` | Google Analytics | Standard GA script URL |
| `googletagmanager.com` | Google Tag Manager | GTM container |
| `doubleclick.net` | DoubleClick | Google ads platform |
| `connect.facebook.net` | Meta Pixel | Facebook tracking script |
| `facebook.net` | Meta Pixel | Facebook tracking script |
| `hotjar.com` | Hotjar | UX behavior analytics |
| `clarity.ms` | Microsoft Clarity | Session analytics |
| `segment.com` | Segment | CDP and analytics |
| `cdn.segment.com` | Segment | CDN for Segment bundle |
| `mixpanel.com` | Mixpanel | Product analytics |
| `snapchat.com` | Snap Pixel | Snapchat marketing pixel |
| `tiktok.com` | TikTok Pixel | TikTok marketing pixel |

## Keyword-based matches

The engine also flags generic tracker keywords to surface suspicious resources.
These are not tied to a specific vendor but are typically associated with
analytics, advertising, or data collection scripts.

| Keyword | Rationale |
| --- | --- |
| `track` | Generic tracking terminology |
| `analytics` | Analytics libraries |
| `pixel` | 1x1 tracking pixels |
| `beacon` | Beacon-style telemetry |
| `advertising` | Ad network scripts |
| `remarketing` | Retargeting or remarketing scripts |

## Validation guidance

When a match appears, review the `value` field in the audit output to determine
whether the resource is truly a tracker or a benign asset.

## Extended catalog (reference)

The following entries are **not currently enabled** in the default configuration
but are included for auditing reference. They can be added to the signature list
if needed.

| Signature | Vendor | Notes |
| --- | --- | --- |
| `adform.net` | Adform | DSP and ad delivery |
| `adnxs.com` | AppNexus | Programmatic ads |
| `adsafeprotected.com` | IAS | Ad verification |
| `advertising.com` | AOL | Advertising network |
| `amazon-adsystem.com` | Amazon Ads | Advertising scripts |
| `amplitude.com` | Amplitude | Product analytics |
| `audiencemanager.de` | Adobe Audience Manager | DMP |
| `bluekai.com` | Oracle BlueKai | DMP |
| `branch.io` | Branch | Mobile attribution |
| `cdn.optimizely.com` | Optimizely | Experimentation |
| `criteo.com` | Criteo | Retargeting |
| `crsspxl.com` | Cross Pixel | Ad measurement |
| `demdex.net` | Adobe | Audience manager |
| `doubleverify.com` | DoubleVerify | Ad verification |
| `everesttech.net` | Adobe | Data tracking |
| `googleadservices.com` | Google Ads | Ads scripts |
| `googlesyndication.com` | Google Ads | Ad syndication |
| `gstatic.com` | Google | Static resources (check context) |
| `hotjar.io` | Hotjar | Session analytics |
| `insight.adsrvr.org` | The Trade Desk | Ad platform |
| `krxd.net` | Salesforce Krux | DMP |
| `licdn.com` | LinkedIn | Insight tag |
| `matomo.org` | Matomo | Analytics |
| `metrika.yandex` | Yandex Metrica | Analytics |
| `newrelic.com` | New Relic | Performance monitoring |
| `optimizely.com` | Optimizely | Experimentation |
| `pendo.io` | Pendo | Product analytics |
| `pingdom.net` | Pingdom | Monitoring |
| `quantserve.com` | Quantcast | Measurement |
| `qualtrics.com` | Qualtrics | Surveys |
| `redditstatic.com` | Reddit | Pixel tracking |
| `sentry.io` | Sentry | Error tracking |
| `scorecardresearch.com` | Comscore | Analytics |
| `segment.io` | Segment | CDP |
| `smartlook.com` | Smartlook | Session analytics |
| `snowplowanalytics.com` | Snowplow | Data collection |
| `stats.wp.com` | WordPress | Stats |
| `taboola.com` | Taboola | Content recommendations |
| `teads.tv` | Teads | Video ads |
| `trak.io` | Trak | Analytics |
| `trustarc.com` | TrustArc | Consent management |
| `twitter.com/i/adsct` | Twitter | Ads conversion tracking |
| `vwo.com` | VWO | Conversion optimization |
| `woopra.com` | Woopra | Analytics |

## Suggested classification tags

| Tag | Description |
| --- | --- |
| `analytics` | Behavior analytics or product insights |
| `advertising` | Ad-serving or ad measurement |
| `marketing` | Marketing attribution |
| `performance` | Monitoring or performance tracking |
| `consent` | Consent management systems |
| `other` | Uncategorized tracking activity |

## Review checklist

1. Identify the third-party domain.
2. Determine if the domain is essential for site functionality.
3. Validate whether explicit consent is required.
4. Update privacy documentation if necessary.
5. Confirm retention policies for tracker data.
