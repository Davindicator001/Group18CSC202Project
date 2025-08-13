import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from media_readability import readability_analysis
from scene_validator import is_scene_heading

class TestMediaReadability(unittest.TestCase):
    def setUp(self):
        """Setup sample scripts for testing different formats"""
        self.web_script = """
        INT. OFFICE - DAY
        
        Brief scene with quick action.
        
        EXT. STREET - DAY
        
        Another quick scene.
        """
        
        self.stage_script = """
        ACT 1, SCENE 1
        
        Character dialogue line 1.
        Character dialogue line 2.
        """
        
        self.tv_script = """
        INT. HOSPITAL - NIGHT
        
        A very long action description that continues for more than one hundred characters to trigger the long line detection in the readability analysis function.
        A very long action description that continues for more than one hundred characters to trigger the long line detection in the readability analysis function.
        A very long action description that continues for more than one hundred characters to trigger the long line detection in the readability analysis function.
        A very long action description that continues for more than one hundred characters to trigger the long line detection in the readability analysis function.
        A very long action description that continues for more than one hundred characters to trigger the long line detection in the readability analysis function.
        """

    def test_web_format_pacing(self):
        """Test web format scene length warnings"""
        report = readability_analysis(self.web_script)
        # Should not flag short scenes (web format prefers short scenes)
        self.assertNotIn("too long for short-form pacing", report)

    def test_stage_format_dialogue_density(self):
        """Test stage format dialogue density"""
        report = readability_analysis(self.stage_script)
        self.assertNotIn("action-heavy for stage format", report)

    def test_tv_format_long_lines(self):
        """Test TV format long line detection"""
        report = readability_analysis(self.tv_script)
        self.assertIn("exceed 100 characters", report)
        self.assertIn("dense narration blocks", report)

    def test_empty_script(self):
        """Test handling of empty script"""
        report = readability_analysis("")
        self.assertIn("No issues found", report)

    def test_format_specific_flags(self):
        """Test that format-specific flags appear"""
        report = readability_analysis(self.tv_script)
        self.assertIn("Format Flags", report)
        self.assertIn("Web:", report)
        self.assertIn("TV:", report)
        self.assertIn("Stage:", report)

if __name__ == '__main__':
    unittest.main()