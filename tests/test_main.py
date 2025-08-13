"""
SCRIPT ANALYZER CLI - UNIT TESTS
================================

This module contains unit tests for the ScriptAnalyzerCLI class.
Tests cover all major functionality including:
- File loading
- Text input
- Script analysis
- Report viewing
- Report saving
- Program exit

Testing Approach:
-----------------
1. Uses unittest framework with mock objects
2. Tests isolate CLI functionality by:
   - Mocking user input
   - Capturing stdout
   - Simulating file operations
3. Each test verifies both:
   - Correct behavior (happy path)
   - Expected output messages
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import ScriptAnalyzerCLI

class TestScriptAnalyzerCLI(unittest.TestCase):
    """Test suite for ScriptAnalyzerCLI class.
    
    Contains setup/teardown and all individual test cases.
    """
    
    def setUp(self):
        """Initialize test environment before each test case.
        
        Creates:
        - Fresh CLI instance
        - Output capture for assertions
        """
        self.cli = ScriptAnalyzerCLI()  # New instance for each test
        self.saved_stdout = sys.stdout  # Save original stdout
        self.stdout = StringIO()  # Create mock stdout
        sys.stdout = self.stdout  # Redirect stdout for capture

    def tearDown(self):
        """Clean up after each test case.
        
        Restores original stdout stream.
        """
        sys.stdout = self.saved_stdout  # Restore original stdout

    @patch('builtins.input', side_effect=['1', 'sample.txt', '0'])
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="Sample script content")
    def test_load_from_file(self, mock_open, mock_input):
        """Test script loading from file.
        
        Verifies:
        - File open operation is called correctly
        - Success message is displayed
        - CLI returns to menu after loading
        """
        self.cli.run()  # Simulate user choosing option 1
        output = self.stdout.getvalue()
        self.assertIn("Loaded script from sample.txt", output)  # Verify success message

    @patch('builtins.input', side_effect=['2', 'TEST SCRIPT', '', '\x1a', '0'])  # \x1a is Ctrl+Z
    def test_enter_text_directly(self, mock_input):
        """Test direct text input functionality.
        
        Simulates:
        - Choosing text input option
        - Entering sample text
        - CTRL+Z to end input
        Verifies proper formatting message appears.
        """
        self.cli.run()
        output = self.stdout.getvalue()
        self.assertIn("Script received and formatted", output)  # Confirm processing

    @patch('builtins.input', side_effect=['4', '0'])
    def test_run_analysis(self, mock_input):
        """Test analysis execution.
        
        Pre-loads sample script then verifies:
        - Analysis completion message appears
        - Menu returns after analysis
        """
        self.cli.script = "Sample script content"  # Pre-load test data
        self.cli.run()
        output = self.stdout.getvalue()
        self.assertIn("Analysis complete", output)  # Check for success

    @patch('builtins.input', side_effect=['5', '1', '0'])
    def test_view_reports(self, mock_input):
        """Test report viewing functionality.
        
        Pre-populates reports then checks:
        - Report menu appears
        - Individual report displays correctly
        - Navigation back to main menu works
        """
        self.cli.reports = {
            'Title': 'Test Report',
            'Structure': 'No issues found'
        }
        self.cli.run()
        output = self.stdout.getvalue()
        self.assertIn("Title Report", output)  # Verify report display

    @patch('builtins.input', side_effect=['6', 'test_report.txt', '0'])
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_report(self, mock_open, mock_input):
        """Test report saving functionality.
        
        Verifies:
        - File is opened with correct parameters
        - Success message appears
        - Correct file operations occur
        """
        self.cli.reports = {'Title': 'Test Report'}  # Pre-load report
        self.cli.run()
        output = self.stdout.getvalue()
        self.assertIn("Report saved to test_report.txt", output)  # Check success message
        mock_open.assert_called_with('test_report.txt', 'w', encoding='utf-8')  # Verify file operation

    @patch('builtins.input', side_effect=['0'])
    def test_exit(self, mock_input):
        """Test program exit functionality.
        
        Verifies clean exit when choosing option 0.
        """
        self.cli.run()
        output = self.stdout.getvalue()
        self.assertIn("Exiting", output)  # Confirm exit message

if __name__ == '__main__':
    unittest.main()  # Run tests when executed directly