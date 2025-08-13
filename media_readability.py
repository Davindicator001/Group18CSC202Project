from collections import defaultdict
from scene_validator import is_dialogue, is_scene_heading, is_character_name

"""
Media Readability Analyzer

Analyzes screenplay readability across different media formats:
- Web: Short-form content pacing optimization
- TV: Visual storytelling considerations
- Stage: Dialogue-heavy script requirements

Identifies:
- Scene length issues by format
- Dialogue density problems
- Long line readability concerns
- Format-specific optimization opportunities

Dependencies:
- scene_validator: For element type detection functions
"""

def readability_analysis(script):
    """
    Perform format-specific readability analysis on a screenplay.
    
    Args:
        script (str): Complete screenplay text to analyze
        
    Returns:
        str: Comprehensive readability report with:
            - Scene length issues for web format
            - Dialogue density analysis for stage format
            - Long line warnings for readability
            - Format-specific flags with suggestions
            
    Analyzes each scene for:
        - Scene length by format (web, tv, stage)
        - Dialogue density (especially important for stage)
        - Long line readability concerns
        - Format-specific optimization opportunities
    """
    lines = script.strip().split("\n")
    scenes = []
    current_scene = {"heading": None, "content": []}
    scene_counter = 0

    # Split the script into scenes
    for line in lines:
        if is_scene_heading(line):
            if current_scene["heading"]:
                scenes.append(current_scene)
            scene_counter += 1
            current_scene = {
                "heading": line.strip(),
                "content": [],
                "index": scene_counter,
            }
        else:
            current_scene["content"].append(line)
    if current_scene["heading"]:
        scenes.append(current_scene)
        
    # Scene analysis structure:
    #   - Scene length evaluation for different media formats
    #   - Dialogue density analysis for stage format
    #   - Line length and block detection for readability
    #   - Content structure recommendations

    report = ["\nReadability Analysis", "----------------------"]
    long_lines = 0
    format_flags = {"Web": [], "TV": [], "Stage": []}

    for scene in scenes:
        scene_len = len(scene["content"])
        long_line_blocks = 0
        consecutive_long = 0

        for line in scene["content"]:
            if len(line) > 100:
                long_lines += 1
                consecutive_long += 1
            else:
                consecutive_long = 0

            if consecutive_long >= 5:
                long_line_blocks += 1

        # Web format pacing check
        if scene_len > 15:
            format_flags["Web"].append(
                f"Scene {scene['index']} too long for short-form pacing ⚠️"
            )

        # Stage format check (should be mostly dialogue)
        # Temporary simplified dialogue detection
        dialogue_lines = sum(1 for line in scene["content"] 
                           if line.strip() and not is_scene_heading(line) and not is_character_name(line))
        if dialogue_lines / max(scene_len, 1) < 0.3:
            format_flags["Stage"].append(
                f"Scene {scene['index']} is action-heavy for stage format ⚠️"
            )

        # TV format check (flag blocks of long lines)
        if long_line_blocks >= 1:
            format_flags["TV"].append(
                f"Scene {scene['index']} has dense narration blocks ⚠️"
            )

    report.append("\nFormat Flags:")
    for category, flags in format_flags.items():
        if flags:
            for f in flags:
                report.append(f"    - {category}: {f}")
        else:
            report.append(f"    - {category}: ✔ No issues found")

    report.append("\nGeneral Issues:")
    if long_lines == 0:
        report.append("    - ✔ No overly long lines found")
    else:
        report.append(
            f"    - {long_lines} line(s) exceed 100 characters (may reduce readability)"
        )

    return "\n".join(report)

