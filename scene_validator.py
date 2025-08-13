import re
from collections import defaultdict
"""
Scene Validator Module

Provides:
1. Heuristic functions to identify screenplay elements (scene headings, dialogue, etc.)
2. Scene structure validation to ensure proper screenplay formatting
3. Character tracking for dialogue assignment analysis

These utilities form the foundation for higher-level screenplay analysis modules.
"""

# Determine if the line is a scene heading (e.g., INT./EXT.)
def is_scene_heading(line):
    return line.strip().upper().startswith(('INT.', 'EXT.'))

# Determine if the line is a transition cue (e.g., CUT TO:, FADE OUT:)
def is_transition(line):
    return line.strip().upper().endswith(('TO:', 'OUT:', 'IN:'))

# Determine if the line is a parenthetical/emotion cue (e.g., (angrily))
def is_emotion(line):
    return line.strip().startswith('(') and line.strip().endswith(')')

# Determine if the line is a character name (ALL CAPS and not too long)
def is_character_name(line):
    line = line.strip()
    return (
        line.isupper()
        and len(line) <= 40
        and 1 <= len(line.split()) <= 4
        and not is_scene_heading(line)
        and not is_transition(line)
        and not is_emotion(line)
    )


# Determine if the line is an action line (not matching anything else)
def is_action(line):
    line = line.strip()
    return (
        line and
        not is_scene_heading(line) and
        not is_transition(line) and
        not is_character_name(line) and
        not is_emotion(line) and
        not line.endswith(("?", "!")) # likely dialogue if ends with these
    )

# Determine if the line looks like dialogue (used for error tracking)
def is_dialogue(line):
    line = line.strip()
    return (
        line and
        not is_scene_heading(line) and
        not is_transition(line) and
        not is_character_name(line) and
        not is_emotion(line) and
        (line.endswith(('.', '?', '!')) or len(line.split()) > 3)
    )

# Main function to validate scene structure and character use
def scene_structure_validator(script):
    lines = script.strip().split('\n')
    scene_count = 0
    valid_headings = []
    header_issues = []
    scene_issues = []
    character_lines = defaultdict(int)
    action_present = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Check for scene heading
        if is_scene_heading(line):
            scene_count += 1
            valid_headings.append(f"    - {line} ✔")
            continue

        # Check for transition not followed by a heading
        if is_transition(line):
            if i + 1 >= len(lines) or not is_scene_heading(lines[i + 1]):
                header_issues.append(f"⚠️ Line {i+1}: transition not followed by a scene heading")
            continue

        # Track action presence
        if is_action(line):
            action_present = True
            continue

        # Check for dialogue contextually
        if is_dialogue(line):
            if i >= 1 and is_character_name(lines[i - 1]):
                character = lines[i - 1].strip().upper()
                character_lines[character] += 1
            elif i >= 2 and is_emotion(lines[i - 1]) and is_character_name(lines[i - 2]):
                character = lines[i - 2].strip().upper()
                character_lines[character] += 1
            else:
                character_lines["UNKNOWN"] += 1
                scene_issues.append(f"❌ Line {i+1}: dialogue not preceded by character name")

    # Compile the report output
    report = ["\nScene Structure Report:", "--------------------------------"]
    report.append(f"Total Scenes: {scene_count}\n")
    if valid_headings:
        report.append("Valid Headings:")
        report.extend(valid_headings)
    else:
        report.append("❌ No valid scene headings found.")

    report.append("\nHeader Reports:")
    if header_issues:
        report.extend([f"    - {issue}" for issue in header_issues])
    else:
        report.append("    - ✔ No header errors")

    report.append("\nScene Reports:")
    if scene_issues:
        report.extend([f"    - {issue}" for issue in scene_issues])
    else:
        report.append("    - ✔ No scene structure issues")

    if not action_present:
        report.append("    - ⚠️ Script has no action lines")

    return '\n'.join(report)

# Tracks character dialogue lines and visualizes distribution
def character_tracking(script):
    lines = script.strip().split('\n')
    current_character = None
    character_lines = defaultdict(int)

    for i, line in enumerate(lines):
        line = line.strip()
        if is_character_name(line):
            current_character = line
        elif is_dialogue(line):
            if current_character:
                character_lines[current_character] += 1
            else:
                character_lines["UNKNOWN"] += 1
        elif line == '':
            current_character = None

    # Compile the character dialogue report
    analysis = ["\nCharacters Found:"]
    for character, count in character_lines.items():
        analysis.append(f"    - {character}: {count} lines")

    analysis.append("\nCharacter Dialogue Distribution:")
    total_lines = sum(character_lines.values())
    for character, count in character_lines.items():
        percent = (count / total_lines) * 100 if total_lines else 0
        bar = "█" * int(percent // 5)
        analysis.append(f"{character:<12}: {bar} {round(percent)}%")

    analysis.append("\nCharacter Report:")
    if "UNKNOWN" in character_lines:
        analysis.append("    - ⚠️ Some dialogue has no character assigned")
    else:
        analysis.append("    - ✔ No character assignment issues")

    return '\n'.join(analysis)
