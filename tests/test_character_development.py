import unittest
import sys
import os

# Add project root to path for importing sibling modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character_development import character_development_validator

class TestCharacterDevelopment(unittest.TestCase):
    """
    Unit tests for character_development_validator() from character_development.py.
    Validates character introductions, speaking frequency, and presence across scenes.
    """

    def test_single_character_multiple_scenes(self):
        """Tests a character that is properly introduced and speaks across scenes"""
        script = """
INT. LIVING ROOM – NIGHT

SARAH
I can’t believe this is happening.

CUT TO:
INT. BEDROOM – DAY

SARAH
I’ll deal with it.
"""
        result = character_development_validator(script)
        self.assertIn("SARAH (Line 3): Introduced via dialogue only ⚠️", result)
        self.assertIn("SARAH: Speaks 2 times across 2 scenes", result)

    def test_character_only_in_action(self):
        """Tests a character mentioned only in action lines but never speaks"""
        script = """
INT. KITCHEN – NIGHT

SARAH stirs the pot while JOHN watches.

MARK walks in silently.
"""
        result = character_development_validator(script)
        self.assertIn("Warnings:", result)
        self.assertIn("JOHN (Line 3): Introduced via action only", result)

    def test_character_only_speaks_once(self):
        """Tests a character who speaks just once"""
        script = """
INT. OFFICE – EVENING

MARK
We need to talk.
"""
        result = character_development_validator(script)
        self.assertIn("MARK (Line 3): Introduced via dialogue only ⚠️", result)
        self.assertIn("MARK: ⚠️ Only speaks once", result)

    def test_character_never_speaks(self):
        """Tests a character who is introduced but never speaks"""
        script = """
INT. GARAGE – MORNING

SARAH stands silently, staring at the engine.

MARK enters.
"""
        result = character_development_validator(script)
        self.assertIn("SARAH: ❌ Never speaks", result)
        self.assertIn("MARK: ❌ Never speaks", result)

    def test_multiple_characters_and_cross_scene_tracking(self):
        """Tests multiple characters speaking across multiple scenes"""
        script = """
INT. PARK – DAY

SARAH
Hey!

MARK
What's up?

CUT TO:
EXT. ROAD – NIGHT

SARAH
Be careful.

MARK
I always am.
"""
        result = character_development_validator(script)
        self.assertIn("SARAH: Speaks 2 times across 2 scenes", result)
        self.assertIn("MARK: Speaks 2 times across 2 scenes", result)
        self.assertNotIn("❌", result)  # No major errors

if __name__ == '__main__':
    unittest.main()
