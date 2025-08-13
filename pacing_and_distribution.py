from collections import defaultdict
from scene_validator import is_action, is_dialogue, is_scene_heading, is_character_name

"""
Scene Pacing & Distribution Analysis Module

Analyzes screenplay pacing through:
1. Scene-by-scene dialogue/action balance detection
2. Character-specific dialogue distribution metrics
3. Narrative flow assessment based on scene structure

Provides insights into:
- Scene balance (dialogue-heavy vs action-heavy)
- Character utilization distribution
- Overall pacing consistency across the script

Dependencies:
- scene_validator: For line type identification
"""

def scene_pacing_and_distribution(script):
	lines = script.strip().split('\n')
	scenes = []
	current_scene = {"heading": None, "content": []}
	scene_counter = 0

	# First split the script into scenes
	for line in lines:
		if is_scene_heading(line):
			if current_scene["heading"]:
				scenes.append(current_scene)
			scene_counter += 1
			current_scene = {"heading": line.strip(), "content": [], "index": scene_counter}
		else:
			current_scene["content"].append(line)
	if current_scene["heading"]:
		scenes.append(current_scene)

	# Now analyze each scene
	scene_reports = []
	character_lines = defaultdict(int)
	total_dialogue_lines = 0

	for scene in scenes:
		dialogue_count = 0
		action_count = 0
		current_character = None

		for line in scene["content"]:
			if is_character_name(line):
				current_character = line.strip().upper()
			elif is_dialogue(line):
				dialogue_count += 1
				total_dialogue_lines += 1
				if current_character:
					character_lines[current_character] += 1
				else:
					character_lines["UNKNOWN"] += 1
			elif is_action(line):
				action_count += 1

		# Scene pacing type
		if dialogue_count > action_count * 2:
			balance = "💬 Dialogue-heavy"
		elif action_count > dialogue_count * 2:
			balance = "🏃 Action-heavy"
		else:
			balance = "⚖️ Balanced"

		scene_reports.append({
			"index": scene["index"],
			"heading": scene["heading"],
			"dialogue": dialogue_count,
			"action": action_count,
			"balance": balance,
			"quantity": dialogue_count + action_count
		})

	# Build output report
	report = ["\nScene Pacing Report", "--------------------"]
	ill_paced = False
	if scene_counter == 0:
 		report.append("No scenes detected")
	elif scene_counter == 1:
		report.append("Only one scene detected")
		for i,s in enumerate(scene_reports):
			report.append(f"Scene {s['index']}: {s['heading']}")
			report.append(f"    - Dialogue: {s['dialogue']} lines")
			report.append(f"    - Action: {s['action']} lines")
			report.append(f"    - Balance: {s['balance']}\n")
	else:
		for i,s in enumerate(scene_reports):
			report.append(f"Scene {s['index']}: {s['heading']}")
			report.append(f"    - Dialogue: {s['dialogue']} lines")
			report.append(f"    - Action: {s['action']} lines")
			report.append(f"    - Balance: {s['balance']}\n")
			if i > 0 :
				p = scene_reports[i-1]
				if abs(s['quantity'] - p['quantity']) >= 4:
					ill_paced = True
	if ill_paced and scene_counter > 1:
		report.append("Significant variation in scene lengths - Consider breaking up longer scenes")
	else:
		report.append("Scene length distribution is balanced")
	report.append("Dialogue Distribution:")
	report.append("----------------------")
	if total_dialogue_lines == 0:
		report.append("    No dialogue found in the script.")
	else:
		for char, count in character_lines.items():
			percent = (count / total_dialogue_lines) * 100
			bar = "█" * int(percent // 5)
			report.append(f"    {char:<12}: {bar} {round(percent)}%")

	return '\n'.join(report)
