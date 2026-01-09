import unittest

from serverless_functions import logger


class LoggerTestCase(unittest.TestCase):
    def test_setup_logging(self):
        logger.setup_logging()


if __name__ == "__main__":
    unittest.main()
