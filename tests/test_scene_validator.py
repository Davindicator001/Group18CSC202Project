import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scene_validator import (
    is_scene_heading, is_transition, is_emotion, is_character_name,
    is_action, is_dialogue, scene_structure_validator, character_tracking
)

class TestSceneValidator(unittest.TestCase):
    """
    Unit tests for the scene_validator.py module.
    Covers all line classification heuristics and validation/report functions.
    """

    # ---------------- HEURISTICS ----------------

    def test_scene_heading(self):
        """Scene heading should start with INT. or EXT."""
        self.assertTrue(is_scene_heading("INT. ROOM - DAY"))
        self.assertTrue(is_scene_heading("EXT. PARK – NIGHT"))
        self.assertFalse(is_scene_heading("FADE OUT:"))

    def test_transition(self):
        """Transitions like CUT TO: or FADE OUT: should be recognized."""
        self.assertTrue(is_transition("CUT TO:"))
        self.assertTrue(is_transition("FADE OUT:"))
        self.assertFalse(is_transition("INT. KITCHEN"))

    def test_emotion(self):
        """Emotions are lines like (angrily) or (whispers)"""
        self.assertTrue(is_emotion("(angrily)"))
        self.assertFalse(is_emotion("angrily"))
        self.assertFalse(is_emotion("(just"))

    def test_character_name(self):
        """Character names must be all caps, short, and not scene-related"""
        self.assertTrue(is_character_name("SARAH"))
        self.assertTrue(is_character_name("DR. EVIL"))
        self.assertFalse(is_character_name("INT. HALLWAY"))
        self.assertFalse(is_character_name("cut to:"))
        self.assertFalse(is_character_name("(angrily)"))

    def test_action(self):
        """Actions are standalone narrative lines not matching any other pattern"""
        self.assertTrue(is_action("He picks up the glass and stares at it."))
        self.assertFalse(is_action("MARK"))
        self.assertFalse(is_action("FADE IN:"))

    def test_dialogue(self):
        """Dialogues are not actions, not character names, and have actual content"""
        self.assertTrue(is_dialogue("I can't believe this is happening."))
        self.assertFalse(is_dialogue("CUT TO:"))
        self.assertFalse(is_dialogue(""))

    # ---------------- VALIDATION ----------------

    def test_scene_structure_validator(self):
        """Tests a valid script block for correct heading, character, and dialogue structure"""
        script = """
INT. LIVING ROOM – NIGHT

SARAH
(angrily)
I can't believe this is happening.

MARK
We don’t have a choice.

Sarah walks in

CUT TO:
INT. BEDROOM – LATER

SARAH
It's over.
FADE OUT:
"""
        result = scene_structure_validator(script)
        self.assertIn("Scene Structure Report:", result)
        self.assertIn("Total Scenes: 2", result)
        self.assertIn("Header Reports:", result)
        self.assertIn("✔ No scene structure issues", result)

    def test_character_tracking(self):
        """Ensures character lines and dialogue counts are reported accurately"""
        script = """
INT. ROOM – DAY

SARAH
Let’s get out of here.

MARK
We’re not done yet.

SARAH
We are now.
"""
        result = character_tracking(script)
        self.assertIn("Characters Found:", result)
        self.assertIn("SARAH: 2 lines", result)
        self.assertIn("MARK: 1 lines", result)
        self.assertIn("✔ No character assignment issues", result)


if __name__ == '__main__':
    unittest.main()
