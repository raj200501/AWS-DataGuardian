import unittest
import logger

class LoggerTestCase(unittest.TestCase):
    def test_setup_logging(self):
        logger.setup_logging()
        self.assertTrue(True)  # Ensure no exceptions are raised

if __name__ == '__main__':
    unittest.main()
