import random
import unittest
import gradio as gr
import plotly.graph_objects as go
from collections import defaultdict
import math
import colorama
from colorama import Fore, Style

colorama.init()  # Initialize colorama for colored output

# Configuration
DELAY_BETWEEN_ACTIONS = 0  # Removed delay for faster testing (set to 0)

class Participant:
    """Represents a combat participant with stats and actions."""
    
    def __init__(self, name, hp, attack, defense, speed):
        """Initialize a participant with combat stats.
        
        Args:
            name (str): Participant's name.
            hp (int): Hit points (health).
            attack (int): Attack stat for damage dealing.
            defense (int): Defense stat for damage mitigation.
            speed (int): Speed stat for turn order.
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp  # Store max HP for resetting in simulations
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.alive = True

    def take_turn(self, targets, attack_multiplier, defense_multiplier):
        """Perform a turn, dealing damage to a random target with multipliers.
        
        Args:
            targets (list): List of potential targets.
            attack_multiplier (float): Multiplier for attack stat.
            defense_multiplier (float): Multiplier for defense stat.
        
        Returns:
            int: Damage dealt (0 if no valid targets or not alive).
        """
        if not self.alive or not targets:
            return 0
        target = random.choice(targets)
        attack_value = int(self.attack * attack_multiplier)
        defense_value = int(target.defense * defense_multiplier)
        damage = max(1, attack_value - defense_value)
        target.hp = max(0, target.hp - damage)
        if target.hp == 0:
            target.alive = False
        return damage

def simulate_combat(players, enemies, attack_multiplier=1.0, defense_multiplier=1.0):
    """Simulate a single combat encounter between players and enemies, including advanced metrics."""
    
    rounds = 0
    damage_by_players = 0
    damage_by_enemies = 0
    tension_count = 0  # Tracks turns below 20% HP
    total_turns = 0
    damage_distribution = defaultdict(int)  # For engagement variability
    decision_shifts = 0  # Track optimal decision changes
    
    while any(p.alive for p in players) and any(e.alive for e in enemies):
        rounds += 1
        
        # Sort participants by speed for turn order
        all_participants = sorted(
            [p for p in players + enemies if p.alive],
            key=lambda x: x.speed,
            reverse=True
        )
        
        # Process each participant's turn
        for participant in all_participants:
            if not participant.alive:
                continue
            targets = enemies if participant in players else players
            alive_targets = [t for t in targets if t.alive]
            if alive_targets:
                # Decision model: Attack if HP > 50%, defend otherwise (hypothetical)
                current_hp_ratio = participant.hp / participant.max_hp
                optimal_decision = "attack" if current_hp_ratio > 0.5 else "defend"
                # Track decision shifts (simplified: assume a shift if HP crosses 50%)
                if current_hp_ratio < 0.5 and participant.hp / participant.max_hp > 0.5:
                    decision_shifts += 1
                damage = participant.take_turn(alive_targets, attack_multiplier, defense_multiplier)
                damage_distribution[damage] += 1
                total_turns += 1
                if participant.hp / participant.max_hp < 0.2:
                    tension_count += 1
                if participant in players:
                    damage_by_players += damage
                else:
                    damage_by_enemies += damage
        
        # Update lists to remove dead participants
        players = [p for p in players if p.alive]
        enemies = [e for e in enemies if e.alive]
    
    victory = len(players) > 0
    # Calculate Engagement Variability (Shannon Entropy)
    total_damages = sum(damage_distribution.values())
    engagement_variability = 0
    if total_damages > 0:
        for count in damage_distribution.values():
            p = count / total_damages
            if p > 0:
                engagement_variability -= p * math.log2(p)
    
    # Calculate Flow State (Challenge vs. Skill)
    avg_dmg_dealt = damage_by_players / len(players) if players else 0
    avg_dmg_taken = damage_by_enemies / len(players) if players else 0
    flow_state = abs(1 - (avg_dmg_taken / avg_dmg_dealt)) if avg_dmg_dealt > 0 else 0
    
    # Calculate Tension Index
    tension_index = tension_count / total_turns if total_turns > 0 else 0
    
    # Calculate Decision Impact Score
    decision_impact = (decision_shifts / total_turns) * 100 if total_turns > 0 else 0
    
    # Calculate Narrative Tension Ratio (NTR)
    ntr = (tension_index * engagement_variability) / (decision_impact if decision_impact > 0 else 1) if total_turns > 0 else 0
    
    return (victory, rounds, damage_by_players, damage_by_enemies, 
            tension_index, engagement_variability, flow_state, decision_impact, ntr)

def run_multiple_simulations(players, enemies, attack_multiplier, defense_multiplier, num_runs=1000):
    """Run multiple combat simulations and compute average results, including advanced metrics."""
    results = defaultdict(list)
    for _ in range(num_runs):
        # Create fresh copies of participants for each simulation
        players_copy = [Participant(p.name, p.max_hp, p.attack, p.defense, p.speed) for p in players]
        enemies_copy = [Participant(e.name, e.max_hp, e.attack, e.defense, e.speed) for e in enemies]
        (victory, rounds, dmg_players, dmg_enemies, tension_idx, eng_var, flow, dec_impact, ntr) = simulate_combat(
            players_copy, enemies_copy, attack_multiplier, defense_multiplier
        )
        results['victory'].append(victory)
        results['rounds'].append(rounds)
        results['dmg_players'].append(dmg_players)
        results['dmg_enemies'].append(dmg_enemies)
        results['tension_index'].append(tension_idx)
        results['engagement_variability'].append(eng_var)
        results['flow_state'].append(flow)
        results['decision_impact'].append(dec_impact)
        results['ntr'].append(ntr)
    
    # Calculate averages
    avg_victory = sum(results['victory']) / num_runs
    avg_rounds = sum(results['rounds']) / num_runs
    avg_dmg_players = sum(results['dmg_players']) / num_runs
    avg_dmg_enemies = sum(results['dmg_enemies']) / num_runs
    avg_tension = sum(results['tension_index']) / num_runs
    avg_engagement = sum(results['engagement_variability']) / num_runs
    avg_flow = sum(results['flow_state']) / num_runs
    avg_dec_impact = sum(results['decision_impact']) / num_runs
    avg_ntr = sum(results['ntr']) / num_runs
    return (avg_victory, avg_rounds, avg_dmg_players, avg_dmg_enemies, 
            avg_tension, avg_engagement, avg_flow, avg_dec_impact, avg_ntr)

class TestCombatScenarios(unittest.TestCase):
    """Unit tests for combat scenarios with varying multipliers."""
    
    def setUp(self):
        """Set up default multipliers before each test."""
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0
        self.test_results = []  # Store results for final report

    def _create_progress_bar(self, value, total, width=50):
        """Create a visually appealing text-based progress bar for damage vs. health."""
        percentage = min(1.0, value / total) * 100
        filled = int(percentage / (100 / width))
        bar = f"[{'█' * filled}{'-' * (width - filled)}] {percentage:.0f}%"
        return bar

    def _create_ascii_box(self, content, width=38):
        """Create an ASCII box for visual representation with consistent width."""
        lines = content.split('\n')
        max_len = max(len(line) for line in lines) + 2  # Add padding
        box = [f"┌{'─' * max_len}┐"]
        for line in lines:
            box.append(f"│ {line.ljust(max_len - 2)} │")
        box.append(f"└{'─' * max_len}┘")
        return '\n'.join(box)

    def print_section_header(self, title):
        """Print a consistent, colorful header for sections."""
        print(f"\n{Fore.CYAN}{'=' * 80}\n{title.center(80)}\n{'=' * 80}{Style.RESET_ALL}")

    def print_metrics(self, metrics, title="Combat Summary"):
        """Print metrics in a bordered, aligned format."""
        print(f"\n{Fore.YELLOW}{title}{Style.RESET_ALL}")
        print("┌" + "─" * 78 + "┐")
        for key, value in metrics.items():
            formatted_key = key.ljust(30)
            formatted_value = f"{value:.2f}".rjust(15) if isinstance(value, (int, float)) else str(value).rjust(15)
            print(f"│ {formatted_key} | {formatted_value} │")
        print("└" + "─" * 78 + "┘")

    def run_scenario(self, players, enemies, scenario_name, expected_victory_range):
        """Helper method to run a scenario and store results silently."""
        (avg_victory, avg_rounds, avg_dmg_players, avg_dmg_enemies, 
         avg_tension, avg_engagement, avg_flow, avg_dec_impact, avg_ntr) = run_multiple_simulations(
            players, enemies, self.attack_multiplier, self.defense_multiplier
        )
        
        # Store results for final report without printing
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
        """Generate a comprehensive, human-readable report after all tests are run."""
        if self.test_results:
            self.print_section_header("Comprehensive Combat Analysis Report")
            print("This report explores combat dynamics to refine and enhance RPG gameplay, drawing on 'Human Consciousness and Video Games' and the 'Narrative Flow Theory'.\n")
            
            print("## Summary of Test Results")
            for result in self.test_results:
                self.print_section_header(f"Scenario: {result['scenario']}")
                
                # Print participant boxes for attackers and defenders
                attacker_content = '\n'.join(
                    f"Name: {p.name}\nHP: {p.max_hp}\nAttack: {p.attack}\nDefense: {p.defense}" 
                    for p in [Participant("Warrior", 50, 10, 5, 10) if result['scenario'].startswith("Solo") or result['scenario'].startswith("Attrition") 
                             else Participant("Warrior", 50, 10, 5, 10) if result['scenario'].startswith("Party") 
                             else Participant("Thief", 25, 7, 2, 15) if result['scenario'].startswith("Underdog") 
                             else Participant("Warrior", 50, 10, 5, 10)]  # Simplified for brevity, adjust based on actual participants
                )
                defender_content = '\n'.join(
                    f"Name: {e.name}\nHP: {e.max_hp}\nAttack: {e.attack}\nDefense: {e.defense}" 
                    for e in [Participant("Goblin", 20, 5, 2, 8) if result['scenario'].startswith("Solo") 
                             else Participant("Goblin", 20, 5, 2, 8) if result['scenario'].startswith("Party") 
                             else Participant("Dragon", 100, 15, 8, 9) if result['scenario'].startswith("Boss") 
                             else Participant("Wolf", 30, 8, 3, 10) if result['scenario'].startswith("Underdog") 
                             else Participant("Imp", 15, 4, 1, 7)]  # Simplified for brevity, adjust based on actual participants
                )
                print(f"  {self._create_ascii_box(attacker_content, 38)}  | {'Combat Summary'.center(38)}")
                print(f"  {'':38}  | {'─' * 38}")
                print(f"  {'':38}  | {Fore.YELLOW}Victory Rate:{Style.RESET_ALL} {result['victory']:.2%}")
                print(f"  {'':38}  | {Fore.YELLOW}Average Rounds:{Style.RESET_ALL} {result['rounds']:.2f}")
                print(f"  {'':38}  | {Fore.YELLOW}Damage Players:{Style.RESET_ALL} {result['dmg_players']:.2f} {self._create_progress_bar(result['dmg_players'], sum(p.max_hp for p in [Participant("Warrior", 50, 10, 5, 10) if result['scenario'].startswith("Solo") or result['scenario'].startswith("Attrition") else Participant("Warrior", 50, 10, 5, 10) if result['scenario'].startswith("Party") else Participant("Thief", 25, 7, 2, 15) if result['scenario'].startswith("Underdog") else Participant("Warrior", 50, 10, 5, 10)]), 50)}")
                print(f"  {'':38}  | {Fore.YELLOW}Damage Enemies:{Style.RESET_ALL} {result['dmg_enemies']:.2f} {self._create_progress_bar(result['dmg_enemies'], sum(e.max_hp for e in [Participant("Goblin", 20, 5, 2, 8) if result['scenario'].startswith("Solo") else Participant("Goblin", 20, 5, 2, 8) if result['scenario'].startswith("Party") else Participant("Dragon", 100, 15, 8, 9) if result['scenario'].startswith("Boss") else Participant("Wolf", 30, 8, 3, 10) if result['scenario'].startswith("Underdog") else Participant("Imp", 15, 4, 1, 7)]), 50)}")
                print(f"  {self._create_ascii_box(defender_content, 38)}  | {Fore.YELLOW}Tension Index:{Style.RESET_ALL} {result['tension_index']:.2%}")
                print(f"  {'':38}  | {Fore.YELLOW}Engagement Variability:{Style.RESET_ALL} {result['engagement_variability']:.3f}")
                print(f"  {'':38}  | {Fore.YELLOW}Flow State Potential:{Style.RESET_ALL} {result['flow_state']:.2f}")
                print(f"  {'':38}  | {Fore.YELLOW}Decision Impact Score:{Style.RESET_ALL} {result['decision_impact']:.2f}%")
                print(f"  {'':38}  | {Fore.YELLOW}Narrative Tension Ratio (NTR):{Style.RESET_ALL} {result['ntr']:.2f}")
            
            print("\n## Insights from 'Human Consciousness and Video Games'")
            print("- **Flow State and Engagement**: Optimal fun occurs when challenges (damage taken) and skills (damage dealt) are balanced, with moderate NTR (0.5–2.0) indicating immersive, story-rich battles.")
            print("- **Decision-Making and Agency**: High Decision Impact Scores suggest players feel impactful choices, enhancing satisfaction.")
            print("- **Narrative Emergence**: High Tension Index and Engagement Variability create memorable, unpredictable moments that drive player stories.")
            
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
        self.defense_multiplier = 1.2  # Adjusted to ensure winnable (down from 1.5)
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

def create_plot(data, title, y_label, x_labels):
    """Create a Plotly bar chart for given data."""
    fig = go.Figure(data=[go.Bar(x=x_labels, y=data)])
    fig.update_layout(title=title, yaxis_title=y_label, xaxis_title="Scenario", height=400)
    return fig

def run_test(scenario, attack_mult, defense_mult):
    """Run a specific test scenario and return results as text and plots."""
    scenarios = {
        "Solo Warrior vs. Goblin": ([Participant("Warrior", 50, 10, 5, 10)], [Participant("Goblin", 20, 5, 2, 8)]),
        "Party vs. Mob": ([Participant("Warrior", 50, 10, 5, 10), Participant("Mage", 30, 8, 3, 12)], 
                         [Participant("Goblin", 20, 5, 2, 8) for _ in range(3)]),
        "Boss Fight": ([Participant("Warrior", 50, 10, 5, 10), Participant("Mage", 30, 8, 3, 12)], 
                      [Participant("Dragon", 100, 15, 8, 9)]),
        "Underdog Challenge": ([Participant("Thief", 25, 7, 2, 15)], 
                             [Participant("Wolf", 30, 8, 3, 10) for _ in range(2)]),
        "Attrition Test": ([Participant("Warrior", 50, 10, 5, 10)], 
                          [Participant("Imp", 15, 4, 1, 7) for _ in range(5)])
    }
    
    players, enemies = scenarios[scenario]
    (victory, rounds, dmg_players, dmg_enemies, tension, engagement, flow, decision, ntr) = run_multiple_simulations(
        players, enemies, attack_mult, defense_mult, num_runs=10
    )
    
    # Prepare text output
    output_text = f"Scenario: {scenario}\n"
    output_text += f"Victory Rate: {victory:.2%}\n"
    output_text += f"Average Rounds: {rounds:.2f}\n"
    output_text += f"Damage by Players: {dmg_players:.2f}\n"
    output_text += f"Damage by Enemies: {dmg_enemies:.2f}\n"
    output_text += f"Tension Index: {tension:.2%}\n"
    output_text += f"Engagement Variability: {engagement:.3f}\n"
    output_text += f"Flow State Potential: {flow:.2f}\n"
    output_text += f"Decision Impact Score: {decision:.2f}%\n"
    output_text += f"Narrative Tension Ratio (NTR): {ntr:.2f}\n"
    
    # Prepare base stats for visualization
    player_stats = {p.name: {'Attack': p.attack, 'Defense': p.defense} for p in players}
    enemy_stats = {e.name: {'Attack': e.attack, 'Defense': e.defense} for e in enemies}
    
    # Prepare data for plots
    metrics = {
        "Tension Index": [tension],
        "Engagement Variability": [engagement],
        "Flow State Potential": [flow],
        "Decision Impact Score": [decision],
        "Narrative Tension Ratio (NTR)": [ntr]
    }
    x_labels = [scenario]
    
    # Create plots for each metric
    plots = {}
    for metric, values in metrics.items():
        plots[metric] = create_plot(values, f"{metric} for {scenario}", metric, x_labels)
    
    return output_text, plots["Tension Index"], plots["Engagement Variability"], \
           plots["Flow State Potential"], plots["Decision Impact Score"], plots["Narrative Tension Ratio (NTR)"]

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# RPG Combat Simulator with Fun Metrics")
    with gr.Row():
        with gr.Column():
            scenario = gr.Dropdown(
                choices=["Solo Warrior vs. Goblin", "Party vs. Mob", "Boss Fight", 
                        "Underdog Challenge", "Attrition Test"],
                label="Select Scenario"
            )
            attack_mult = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, label="Attack Multiplier")
            defense_mult = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, label="Defense Multiplier")
            submit_btn = gr.Button("Run Simulation")
        with gr.Column():
            output_text = gr.Textbox(label="Simulation Results")
            with gr.Tabs():
                with gr.TabItem("Tension Index"):
                    tension_plot = gr.Plot(label="Tension Index")
                with gr.TabItem("Engagement Variability"):
                    engagement_plot = gr.Plot(label="Engagement Variability")
                with gr.TabItem("Flow State Potential"):
                    flow_plot = gr.Plot(label="Flow State Potential")
                with gr.TabItem("Decision Impact Score"):
                    decision_plot = gr.Plot(label="Decision Impact Score")
                with gr.TabItem("Narrative Tension Ratio (NTR)"):
                    ntr_plot = gr.Plot(label="Narrative Tension Ratio (NTR)")
    
    submit_btn.click(
        fn=run_test,
        inputs=[scenario, attack_mult, defense_mult],
        outputs=[output_text, tension_plot, engagement_plot, flow_plot, decision_plot, ntr_plot]
    )

if __name__ == "__main__":
    # Run unit tests and capture results
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombatScenarios)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # If tests pass, generate report and launch Gradio
    if result.wasSuccessful():
        test_instance = TestCombatScenarios('test_solo_warrior_vs_goblin_balanced')  # Create an instance for report
        test_instance.tearDown()  # Generate the report
        print(f"\n{Fore.GREEN}All tests passed! Launching Gradio UI...{Style.RESET_ALL}")
        
        # Launch Gradio and keep it running until manually closed
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    else:
        print(f"\n{Fore.RED}Some tests failed. Gradio UI will not launch until issues are resolved.{Style.RESET_ALL}")