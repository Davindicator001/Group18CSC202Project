
from pathlib import Path
import sys
from datetime import datetime
from text_to_script import line_write, format_script
from character_development import character_development_validator
from media_readability import readability_analysis
from scene_validator import scene_structure_validator, character_tracking
from pacing_and_distribution import scene_pacing_and_distribution
from speaking_time import character_speaking_stats

class ScriptAnalyzerCLI:
    def __init__(self):
        self.script = ""
        self.reports = {}
        self.current_edit = None

    def extract_title(self, script: str) -> str:
        for line in script.splitlines():
            if line.strip():
                return line.strip()
        return "Untitled Script"

    def show_menu(self):
        print("\n" + "="*50)
        print("SCRIPT ANALYZER CLI TOOL")
        print("="*50)
        print("1. Load script from file")
        print("2. Enter script text directly")
        if self.script:
            print("3. Edit current script")
            print("4. Run analysis")
            print("5. View reports")
            print("6. Save report to file")
        print("0. Exit")
        print("="*50)

    def load_from_file(self):
        filepath = input("Enter file path: ").strip()
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                raw_text = file.read()
                self.script = format_script(raw_text)
                print(f"\nLoaded script from {filepath}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def enter_text(self):
        """Receive script text directly from user input.
        
        Continuously reads lines until EOF (Ctrl+Z) is detected.
        Formats the input using text_to_script module and stores it.
        """
        print("\nEnter your script text (press Ctrl+Z on empty line when done):")
        raw_text = []
        try:
            while True:
                line = input()
                raw_text.append(line)
        except EOFError:  # Triggered by Ctrl+Z
            pass
        self.script = format_script('\n'.join(raw_text))  # Apply standardized formatting
        print("\nScript received and formatted")

    def edit_script(self):
        """Edit the current script interactively.
        
        Shows current script and allows adding new content.
        Uses Ctrl+Z (Windows) or ^D signal to end input.
        Appends new content to existing script with formatting.
        """
        print("\nCurrent script:")
        print(self.script)
        print("\nEnter new script text (press Ctrl+Z on empty line when done):")
        raw_text = []
        try:
            while True:
                line = input()
                if line.strip() == "^D":  # Alternative EOF signal
                    raise EOFError
                raw_text.append(line)
        except EOFError:  # Triggered by Ctrl+Z or ^D
            pass
        # Combine existing and new script with formatting
        self.script = "\n" + self.script + format_script('\n'.join(raw_text))
        print("\nScript updated")

    def run_analysis(self):
        """Run all available analyses on the current script.
        
        Creates a comprehensive report dictionary with:
        - Title and timestamp
        - Structural analysis
        - Character tracking
        - Development analysis
        - Pacing analysis
        - Readability score
        - Speaking time statistics
        """
        print("\nRunning analysis...")
        title = self.extract_title(self.script)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Run all analysis functions from imported modules
        self.reports = {
            "Title & Date": title+"\n"+current_time,  # Script metadata
            "Structure": scene_structure_validator(self.script),  # From scene_validator.py
            "Characters": character_tracking(self.script),  # From scene_validator.py
            "Development": character_development_validator(self.script),  # From character_development.py
            "Pacing": scene_pacing_and_distribution(self.script),  # From pacing_and_distribution.py
            "Readability": readability_analysis(self.script),  # From media_readability.py
            "Speaking": character_speaking_stats(self.script)  # From speaking_time.py
        }
        print("Analysis complete")

    def view_reports(self):
        """Display analysis reports through an interactive menu.
        
        Shows available reports and allows selecting individual reports
        or viewing the full combined report. Validates user input and
        handles navigation back to main menu.
        """
        if not self.reports:
            print("No reports available. Please run analysis first.")
            return

        print("\n" + "="*50)
        print("REPORTS MENU")
        print("="*50)
        # List all available report sections
        for i, (name, _) in enumerate(self.reports.items(), 1):
            print(f"{i}. View {name} report")
        print(f"{len(self.reports.items())+1}. View Full report")
        print("0. Back to main menu")
        print("="*50)

        choice = input("Select report to view: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(self.reports):
                # Show individual report
                report_name = list(self.reports.keys())[choice-1]
                print(f"\n{report_name} Report:")
                print("="*50)
                print(self.reports[report_name])
            elif choice == len(self.reports)+1:
                # Show combined report
                print(f"\nFull Report:")
                print("="*50)
                full_report = "\n\n".join(f"{k}:\n{v}" for k, v in self.reports.items())
                print(full_report)        
            elif choice == 0:
                return  # Return to main menu

    def save_report(self):
        if not self.reports:
            print("No reports available to save")
            return

        filename = input("Enter filename to save report: ").strip()
        full_report = "\n\n".join(f"{k}:\n{v}" for k, v in self.reports.items())
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(full_report)
            print(f"Report saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def run(self):
        """Main execution loop of the CLI application.
        
        Continuously presents menu and handles user choices:
        1. Load script from file
        2. Enter script manually
        3. Edit current script (if loaded)
        4. Run analysis (if script loaded)
        5. View reports (if analysis done)
        6. Save reports (if reports exist)
        0. Exit program
        
        Validates choices and provides feedback for invalid input.
        """
        while True:
            self.show_menu()
            choice = input("Enter your choice: ")
            
            # Menu option handlers
            if choice == "1":
                self.load_from_file()
            elif choice == "2":
                self.enter_text()
            elif choice == "3" and self.script:
                self.edit_script()
            elif choice == "4" and self.script:
                self.run_analysis()
            elif choice == "5" and self.script:
                self.view_reports()
            elif choice == "6" and self.script:
                self.save_report()
            elif choice == "0":
                print("Exiting...")
                break  # Exit the loop and program
            else:
                print("Invalid choice. Please try again.")  # Input validation

if __name__ == "__main__":
    cli = ScriptAnalyzerCLI()
    cli.run()
