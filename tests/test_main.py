import json
import unittest
from unittest.mock import patch

from serverless_functions import main


class MainTestCase(unittest.TestCase):
    def test_lambda_handler(self):
        with patch.object(main, "perform_privacy_audit") as fake_audit, patch.object(
            main, "save_audit_result"
        ) as fake_save:
            fake_audit.return_value = {"trackers": 1, "cookies": 0}
            event = {"body": json.dumps({"url": "http://example.com"})}
            response = main.lambda_handler(event, {})

            self.assertEqual(response["statusCode"], 200)
            payload = json.loads(response["body"])
            self.assertEqual(payload["message"], "Audit completed")
            fake_audit.assert_called_once_with("http://example.com")
            fake_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
