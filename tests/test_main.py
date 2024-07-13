import unittest
from main import lambda_handler

class MainTestCase(unittest.TestCase):
    def test_lambda_handler(self):
        event = {
            "body": '{"url": "http://example.com"}'
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("result", response["body"])

if __name__ == '__main__':
    unittest.main()
