import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from speaking_time import character_speaking_stats

class TestSpeakingTime(unittest.TestCase):
    def setUp(self):
        self.sample_script = """
        INT. HOUSE - DAY
        
        JOHN
        This is a line of dialogue that should count for John.
        
        MARY
        Mary's dialogue line here.
        
        JOHN
        Another line for John.
        """
        
        self.empty_script = ""
        
    def test_character_line_counts(self):
        """Test accurate counting of character speaking lines"""
        report = character_speaking_stats(self.sample_script)
        self.assertIn("JOHN:\n    - Lines: 2", report)
        self.assertIn("MARY:\n    - Lines: 1", report)
        
    def test_empty_script(self):
        """Test handling of empty script input"""
        report = character_speaking_stats(self.empty_script)
        self.assertIn("No dialogue lines found", report)
        
    def test_character_ranking(self):
        """Test character ranking by speaking time"""
        report = character_speaking_stats(self.sample_script)
        # John should come first since he has more lines
        self.assertTrue(report.find("JOHN") < report.find("MARY"))
        
    def test_formatting(self):
        """Test report formatting"""
        report = character_speaking_stats(self.sample_script)
        self.assertIn("Character Speaking Time Report", report)
        self.assertIn("Total dialogue lines: 3", report)
        
if __name__ == '__main__':
    unittest.main()