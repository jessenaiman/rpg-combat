import argparse
import unittest
import sys
import colorama
from colorama import Fore, Style
from tests import TestCombatScenarios

colorama.init()

def run_terminal_mode():
    """Run tests, generate report, and save to CSV in terminal mode."""
    # Load and run tests using the unittest framework
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombatScenarios)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        # Create a test instance and manually call tearDown to generate the report
        # We need to ensure test_results is populated, so we'll use the test runner's context
        test_instance = TestCombatScenarios('test_solo_warrior_vs_goblin_balanced')
        test_instance.setUp()  # Initialize test_results
        # Since tests have already run, we can safely call tearDown with stored results
        test_instance.tearDown()
        print(f"\n{Fore.GREEN}All tests passed! Results saved to 'combat_results.csv'.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Some tests failed. Check the output for details.{Style.RESET_ALL}")
        sys.exit(1)

def run_gradio_mode():
    """Launch only the Gradio UI in interactive mode."""
    from ui import demo
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG Combat Simulator - Choose operating mode.")
    parser.add_argument('--mode', choices=['terminal', 'gradio'], default='both',
                        help="Operating mode: 'terminal' for tests and report, 'gradio' for UI, or 'both' (default) for both.")
    
    args = parser.parse_args()
    
    if args.mode in ['terminal', 'both']:
        run_terminal_mode()
    
    if args.mode in ['gradio', 'both']:
        run_gradio_mode()