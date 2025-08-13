import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pacing_and_distribution import scene_pacing_and_distribution

class TestPacingAndDistribution(unittest.TestCase):
    def setUp(self):
        self.well_paced_script = """
        INT. HOUSE - DAY
        
        JOHN
        Dialogue line.
        
        EXT. PARK - DAY
        
        MARY
        Another line.
        
        INT. OFFICE - NIGHT
        
        JOHN
        More dialogue.
        """
        
        self.poor_paced_script = """
        INT. HOUSE - DAY
        
        JOHN
        Line 1.
        Line 2.
        Line 3.
        Line 4.
        Line 5.
        
        EXT. PARK - DAY
        
        MARY
        Brief line.
        """

    def test_scene_length_balance(self):
        """Test detection of unbalanced scene lengths"""
        report = scene_pacing_and_distribution(self.well_paced_script)
        self.assertIn("Scene length distribution is balanced", report)
        
        report = scene_pacing_and_distribution(self.poor_paced_script)
        self.assertIn("Significant variation in scene lengths", report)

    def test_pacing_analysis(self):
        """Test pacing recommendations"""
        report = scene_pacing_and_distribution(self.poor_paced_script)
        self.assertIn("Consider breaking up longer scenes", report)

    def test_empty_script(self):
        """Test handling of empty script"""
        report = scene_pacing_and_distribution("")
        self.assertIn("No scenes detected", report)

    def test_single_scene(self):
        """Test single scene handling"""
        script = "INT. HOUSE - DAY\nDialogue"
        report = scene_pacing_and_distribution(script)
        self.assertIn("Only one scene detected", report)

if __name__ == '__main__':
    unittest.main()