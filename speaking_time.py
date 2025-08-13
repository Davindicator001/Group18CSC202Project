from collections import defaultdict
from scene_validator import is_dialogue, is_character_name

def character_speaking_stats(script):
    lines = script.strip().split('\n')  # Split script into individual lines
    current_character = None  # Track the most recent character name
    character_word_count = defaultdict(int)  # Store word counts per character
    character_line_count = defaultdict(int)  # Store dialogue line counts per character
    total_lines = 0  # Count total number of dialogue lines
    
    for line in lines:
        if is_character_name(line):  # Detect and store character name
            current_character = line.strip().upper()
        elif is_dialogue(line):  # Identify dialogue lines
            total_lines += 1
            words = len(line.split())
            if current_character:  # Attribute words and lines to the known character
                character_word_count[current_character] += words
                character_line_count[current_character] += 1
            else:  # Fallback if character name is missing
                character_word_count["UNKNOWN"] += words
                character_line_count["UNKNOWN"] += 1
    
    # Build speaking statistics report
    report = ["\nCharacter Speaking Time Report", "-------------------------------"]
    report.append(f"Total dialogue lines: {total_lines} lines")

    for character in character_word_count:
        words = character_word_count[character]
        lines_spoken = character_line_count[character]
        time_sec = words / 2.5  # Estimate speaking time (150 wpm ≈ 2.5 words/sec)
        time_str = f"{int(time_sec // 60)} min {int(time_sec % 60)} sec" if time_sec >= 60 else f"{int(time_sec)} sec"
        
        # Add character-specific stats
        report.append(f"{character}:")
        report.append(f"    - Lines: {lines_spoken}")
        report.append(f"    - Words: {words}")
        report.append(f"    - Estimated Speaking Time: {time_str}\n")
    
    if len(character_line_count) == 0:  # Handle case where no dialogue was found
        report.append("No dialogue lines found")
    
    return '\n'.join(report)  # Return the formatted report as a single string
