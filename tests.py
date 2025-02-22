import unittest
from combat import run_multiple_simulations
from participant import Participant
import colorama
from colorama import Fore, Style
from tabulate import tabulate

colorama.init()

class TestCombatScenarios(unittest.TestCase):
    """Unit tests for combat scenarios with varying multipliers."""
    
    def setUp(self):
        """Set up default multipliers before each test."""
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0
        self.test_results = []  # Store results for final report and CSV

    def _create_progress_bar(self, value, total, width=50):
        """Create a visually appealing text-based progress bar for damage vs. health."""
        percentage = min(1.0, value / total) * 100
        filled = int(percentage / (100 / width))
        bar = f"[{'█' * filled}{'-' * (width - filled)}] {percentage:.0f}%"
        return bar

    def print_section_header(self, title):
        """Print a consistent, colorful header for sections."""
        print(f"\n{Fore.CYAN}{'=' * 80}\n{title.center(80)}\n{'=' * 80}{Style.RESET_ALL}")

    def run_scenario(self, players, enemies, scenario_name, expected_victory_range):
        """Helper method to run a scenario and store results silently."""
        (avg_victory, avg_rounds, avg_dmg_players, avg_dmg_enemies, 
         avg_tension, avg_engagement, avg_flow, avg_dec_impact, avg_ntr) = run_multiple_simulations(
            players, enemies, self.attack_multiplier, self.defense_multiplier
        )
        
        # Store results for final report and CSV
        self.test_results.append({
            'scenario': scenario_name,
            'victory': avg_victory,
            'rounds': avg_rounds,
            'dmg_players': avg_dmg_players,
            'dmg_enemies': avg_dmg_enemies,
            'tension_index': avg_tension,
            'engagement_variability': avg_engagement,
            'flow_state': avg_flow,
            'decision_impact': avg_dec_impact,
            'ntr': avg_ntr
        })
        
        self.assertGreaterEqual(avg_victory, expected_victory_range[0])
        self.assertLessEqual(avg_victory, expected_victory_range[1])

    def tearDown(self):
        """Generate a concise, tabular report after all tests are run and save to CSV."""
        if self.test_results:
            self.print_section_header("Combat Test Results Summary")
            
            # Prepare data for table
            table_data = []
            for result in self.test_results:
                table_data.append([
                    result['scenario'],
                    f"{result['victory']:.2%}",
                    f"{result['rounds']:.2f}",
                    f"{result['dmg_players']:.2f} / {result['dmg_enemies']:.2f}",
                    f"{result['tension_index']:.2%}",
                    f"{result['engagement_variability']:.3f}",
                    f"{result['flow_state']:.2f}",
                    f"{result['decision_impact']:.2f}%",
                    f"{result['ntr']:.2f}"
                ])
            
            # Print table with tabulate
            headers = ["Scenario", "Victory Rate", "Rounds", "Damage (P/E)", "Tension Index", 
                      "Eng. Var.", "Flow State", "Dec. Impact", "NTR"]
            print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[30, 12, 12, 20, 12, 12, 12, 12, 12]))
            
            # Save to CSV for model training
            import csv
            with open('combat_results.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for row in table_data:
                    writer.writerow(dict(zip(headers, row)))
            
            print("\nResults saved to 'combat_results.csv' for model training.")
            
            print("\n## Insights from 'Human Consciousness and Video Games'")
            print("- **Flow State and Engagement**: Optimal fun occurs when challenges and skills are balanced, with moderate NTR (0.5–2.0) indicating immersive battles.")
            print("- **Decision-Making and Agency**: High Decision Impact Scores suggest impactful choices.")
            print("- **Narrative Emergence**: High Tension Index and Engagement Variability drive story-rich moments.")
            
            print("\n## Recommendations for Refinement")
            print("- Adjust multipliers to target NTR between 0.5–2.0 for maximum engagement.")
            print("- Increase Tension Index in underdog scenarios for narrative depth.")
            print("- Balance Flow State Potential near 1.0 to maintain immersion.")
            self.print_section_header("End of Report")

    def test_solo_warrior_vs_goblin_balanced(self):
        """Test a solo warrior vs. goblin with balanced multipliers."""
        warrior = Participant("Warrior", 50, 10, 5, 10)
        goblin = Participant("Goblin", 20, 5, 2, 8)
        self.run_scenario([warrior], [goblin], "Solo Warrior vs. Goblin (Balanced)", (0.9, 1.0))

    def test_party_vs_mob_attacker_favored(self):
        """Test a party vs. mob with attacker-favored multipliers."""
        self.attack_multiplier = 1.5
        self.defense_multiplier = 1.0
        warrior = Participant("Warrior", 50, 10, 5, 10)
        mage = Participant("Mage", 30, 8, 3, 12)
        goblins = [Participant("Goblin", 20, 5, 2, 8) for _ in range(3)]
        self.run_scenario([warrior, mage], goblins, "Party vs. Mob (Attacker-Favored)", (0.8, 1.0))

    def test_boss_fight_defender_favored(self):
        """Test a boss fight with defender-favored multipliers."""
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.2  # Adjusted to ensure winnable
        warrior = Participant("Warrior", 50, 10, 5, 10)
        mage = Participant("Mage", 30, 8, 3, 12)
        dragon = Participant("Dragon", 100, 15, 8, 9)
        self.run_scenario([warrior, mage], [dragon], "Boss Fight (Defender-Favored)", (0.0, 0.3))

    def test_underdog_challenge_scaled(self):
        """Test an underdog challenge with scaled multipliers."""
        self.attack_multiplier = 0.8  # Adjusted to allow some wins
        self.defense_multiplier = 1.2  # Adjusted to balance difficulty
        thief = Participant("Thief", 25, 7, 2, 15)
        wolves = [Participant("Wolf", 30, 8, 3, 10) for _ in range(2)]
        self.run_scenario([thief], wolves, "Underdog Challenge (Scaled)", (0.0, 0.1))

    def test_attrition_test_extreme(self):
        """Test an attrition scenario with extreme multipliers."""
        self.attack_multiplier = 1.5  # Adjusted to ensure winnable
        self.defense_multiplier = 0.8  # Adjusted to balance difficulty
        warrior = Participant("Warrior", 50, 10, 5, 10)
        imps = [Participant("Imp", 15, 4, 1, 7) for _ in range(5)]
        self.run_scenario([warrior], imps, "Attrition Test (Extreme)", (0.9, 1.0))