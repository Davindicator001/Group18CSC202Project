import re
from collections import defaultdict
from scene_validator import is_action, is_dialogue, is_scene_heading, is_character_name

"""
Character Development Validator Module

This module analyzes screenplay character development through:
1. Tracking character introductions and first appearances
2. Monitoring speaking patterns across scenes
3. Identifying underdeveloped characters
4. Validating proper character presence in action descriptions

Dependencies:
- scene_validator: Provides line type detection functions
"""


def character_development_validator(script):
    """
    Analyze character development across the script.
    Flags characters introduced but not speaking, or speaking too little.
    """
    lines = script.strip().split('\n')
    character_speakers = defaultdict(int)  # Track how many lines each character spoke
    introduced = {}  # Track first appearance (via action or dialogue)
    current_character = None
    scenes = 0
    scene_map = defaultdict(set)  # Track which scenes a character appears in

    for i, line in enumerate(lines):
        line = line.strip()

        if is_scene_heading(line):
            scenes += 1
            continue

        # Track character name before dialogue
        if is_character_name(line):
            current_character = line.strip()
            if current_character not in introduced:
                introduced[current_character] = i + 1

        elif is_dialogue(line) and current_character:
            character_speakers[current_character] += 1
            scene_map[current_character].add(scenes)

        elif is_action(line):
            # Find all ALL CAPS words that look like names
            possible_names = re.findall(r'\b[A-Z][A-Z ]{1,39}\b', line)
            for name in possible_names:
                name = name.strip()
                if name not in introduced:
                    introduced[name] = i + 1

        # Reset speaker context on blank line
        elif not line:
            current_character = None

    # Build report
    report = ["\nCharacter Development Report", "--------------------------------", ""]
    report.append("Introduced Characters:")
    for char, line_no in introduced.items():
        intro = f"{char} (Line {line_no})"
        if char not in character_speakers:
            report.append(f"    - {intro}: Introduced via action only ❌")
        else:
            report.append(f"    - {intro}: Introduced via dialogue only ⚠️")

    report.append("\nSpeaking Presence:")
    for char, count in character_speakers.items():
        scene_count = len(scene_map[char])
        if count == 1:
            report.append(f"{char}: ⚠️ Only speaks once")
        else:
            report.append(f"{char}: Speaks {count} times across {scene_count} scenes")

    # Final warnings
    report.append("\nWarnings:")
    for char in introduced:
        if char not in character_speakers:
            report.append(f"{char}: ❌ Never speaks")

    return '\n'.join(report)

