"""
text_to_script.py — Screenplay Formatting Module

Core functionality for converting raw text into properly formatted screenplay format
according to industry standards.

Key Features:
- Scene heading detection and formatting (INT./EXT.)
- Transition line recognition and right-alignment
- Character name identification and upper-casing
- Parenthetical handling with proper indentation
- Dialogue formatting with centering
- Action line preservation

The module can be used:
  1. As a command-line tool: python formatter.py <input.txt> [output.txt]
  2. Through its API by importing the format_script function

Input: Raw screenplay text with basic structure
Output: Properly formatted screenplay adhering to industry standards
"""

import re
import sys
from pathlib import Path
from scene_validator import is_action, is_dialogue, is_scene_heading, is_character_name, is_emotion
# ---------- Regex patterns ---------- 
SCENE_RE       = re.compile(r'^\s*(INT\.|EXT\.)', re.I)
TRANSITION_RE  = re.compile(r'^\s*(CUT TO:|FADE (IN|OUT):|DISSOLVE TO:)', re.I)
#  groups:      1-name          2-paren (optional)    3-dialogue
DIALOGUE_RE = re.compile(r'^\s*([\w\-\s]+?)(?:\s*\(([^)]+)\))?\s*:\s*(.+)$')

# ---------- Core formatter ----------
def format_script(text: str) -> str:
    """
    Convert raw screenplay text into properly formatted industry-standard screenplay layout.
    
    The function identifies different screenplay elements (scene headings, dialogue, 
    transitions, etc.) and applies proper formatting:
    - Scene headings in all caps at left margin
    - Transitions right-aligned
    - Character names centered and in all caps
    - Dialogue lines indented below character names
    - Parentheticals properly indented and placed between character and dialogue
    
    Args:
        text (str): Raw screenplay text to format
        
    Returns:
        str: Formatted screenplay text with industry-standard layout
        
    Processing Rules:
        1. Scene headings (starting with INT./EXT.) are capitalized and left-aligned
        2. Transition lines are right-aligned
        3. Character names are centered and followed by their dialogue
        4. Parentheticals are indented 10 spaces below character names
        5. Dialogue lines are indented 5 spaces
        6. Action descriptions appear as-is
    """
    formatted: list[str] = [] 
    for raw in text.splitlines():
        line = raw.strip()

        if not line:                      # preserve blank lines
            formatted.append('')
            continue

        # 1) Scene headings
        if SCENE_RE.match(line):
            formatted.append(line.upper().strip())
            continue
        
        # 2) Transitions
        if TRANSITION_RE.match(line):
            formatted.append(f"{line.upper():>60}")
            continue

        # 3) Dialogue (with optional parenthetical)
        m = DIALOGUE_RE.match(line)
        if m:
            char_name, paren, dialogue = m.groups()
            formatted.append(char_name.upper().strip().center(40))  # name
            if paren:
                formatted.append((' ' * 10) + f"({paren.strip()})")  # parenthetical indented 10
            formatted.append((' ' * 5) + dialogue.strip())    # dialogue indented 5
            continue
        if is_character_name(line):
            formatted.append(line.upper().strip().center(40))
            continue
        if is_emotion(line):
            formatted.append((' ' * 10) + f"{line.strip()}")
            continue
        if is_dialogue(line):
            formatted.append((' ' * 5) + line.strip())    # dialogue indented 5
            continue
            
        # 4) Action
        formatted.append(line)

    return '\n'.join(formatted)

def line_write():
    raw_text = ""
    lines = []
    print("Since no .txt file provided, Enter Each line of your draft and hit enter")
    print("When youre done press q and enter to continue...\n")
    while True:
        error= ""
        try:
            text = input("line: ")
            if text.strip() == "q" and len(lines) <= 1:
                error = "Enter at least 2 lines before proceeding"
                raise ValueError
            if text.strip() == "q":
                print("lines collected, proceeding...\n")
                break
            if(len(text) < 5): 
                error = "Enter a valid line" 
                raise ValueError
            lines.append(text)
        except:
            print(error)
    raw_text = '\n'.join(lines)
    return raw_text

