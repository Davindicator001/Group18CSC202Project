import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from text_to_script import format_script

class TestScriptFormatter(unittest.TestCase):
    """
    Unit tests for the format_script function in text_to_script.py.
    These tests verify formatting of scene headings, transitions, 
    character blocks, parentheticals, and action lines.
    """

    def test_scene_heading_formatting(self):
        """Scene headings (e.g., INT./EXT.) should be uppercased and left-aligned."""
        raw = "int. kitchen – night"
        expected = "INT. KITCHEN – NIGHT"
        self.assertIn(expected, format_script(raw))

    def test_transition_alignment(self):
        """Transitions like CUT TO: should be uppercased and right-aligned to column 60."""
        raw = "CUT TO:"
        formatted = format_script(raw)
        self.assertTrue(formatted.endswith("CUT TO:"))

    def test_dialogue_with_parenthetical(self):
        """Character with parenthetical should be centered, then indent parenthetical and dialogue."""
        raw = "Sarah (calmly): I’ll take care of it."
        result = format_script(raw).splitlines()

        # Expected:
        #        SARAH (centered ~40 cols)
        #          (calmly)
        #      I’ll take care of it.
        self.assertIn(" " * 10 + "(calmly)", result)
        self.assertIn(" " * 5 + "I’ll take care of it.", result)
        self.assertTrue(any("SARAH" in line for line in result))

    def test_character_name_only(self):
        """Lone character names should be centered and uppercased."""
        raw = "MARK"
        formatted = format_script(raw)
        self.assertIn("MARK", formatted)
        self.assertTrue(formatted.strip().isupper())

    def test_emotion_line(self):
        """Emotion lines like (angrily) should be indented by 10 spaces."""
        raw = "(angrily)"
        formatted = format_script(raw)
        self.assertIn(" " * 10 + "(angrily)", formatted)

    def test_action_line(self):
        """Lines that are neither character nor dialogue should be preserved as action."""
        raw = "He walks to the door and pauses."
        formatted = format_script(raw)
        self.assertIn("He walks to the door and pauses.", formatted)

    def test_blank_lines_preserved(self):
        """Blank lines should remain unchanged."""
        raw = "INT. ROOM – DAY\n\nMARK: Hello.\n\nCUT TO:"
        formatted = format_script(raw)
        self.assertIn('', formatted.splitlines())

    def test_multiple_blocks(self):
        """Check proper formatting of multiple dialogue blocks in a row."""
        raw = (
            "INT. ROOM – NIGHT\n"
            "Sarah: Are you serious?\n"
            "Mark (whispers): We don’t have a choice.\n"
            "CUT TO:"
        )
        formatted = format_script(raw).splitlines()
        self.assertTrue(any("SARAH" in line for line in formatted))
        self.assertTrue(any("MARK" in line for line in formatted))
        self.assertTrue(any(" " * 10 in line and "(whispers)" in line for line in formatted))
        self.assertTrue(any("We don’t have a choice." in line for line in formatted))

if __name__ == '__main__':
    unittest.main()
