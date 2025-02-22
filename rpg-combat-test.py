import random
import unittest
from collections import defaultdict
import colorama
from colorama import Fore, Style

colorama.init()  # Initialize colorama for colored output

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
        # Calculate damage using updated formula
        attack_value = int(self.attack * attack_multiplier)
        defense_value = int(target.defense * defense_multiplier)
        damage = max(1, attack_value - defense_value)
        target.hp = max(0, target.hp - damage)
        if target.hp == 0:
            target.alive = False
        return damage

def simulate_combat(players, enemies, attack_multiplier=1.0, defense_multiplier=1.0):
    """Simulate a single combat encounter between players and enemies.
    
    Args:
        players (list): List of Player Participant objects.
        enemies (list): List of Enemy Participant objects.
        attack_multiplier (float): Multiplier for attack stats (default: 1.0).
        defense_multiplier (float): Multiplier for defense stats (default: 1.0).
    
    Returns:
        tuple: (victory (bool), rounds (int), damage_by_players (int), damage_by_enemies (int)).
    """
    rounds = 0
    damage_by_players = 0
    damage_by_enemies = 0
    
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
                damage = participant.take_turn(alive_targets, attack_multiplier, defense_multiplier)
                if participant in players:
                    damage_by_players += damage
                else:
                    damage_by_enemies += damage
        
        # Update lists to remove dead participants
        players = [p for p in players if p.alive]
        enemies = [e for e in enemies if e.alive]
    
    victory = len(players) > 0  # Players win if any survive
    return victory, rounds, damage_by_players, damage_by_enemies

def run_multiple_simulations(players, enemies, attack_multiplier, defense_multiplier, num_runs=1000):
    """Run multiple combat simulations and compute average results.
    
    Args:
        players (list): List of Player Participant objects.
        enemies (list): List of Enemy Participant objects.
        attack_multiplier (float): Multiplier for attack stats.
        defense_multiplier (float): Multiplier for defense stats.
        num_runs (int): Number of simulations to run (default: 1000).
    
    Returns:
        tuple: (avg_victory (float), avg_rounds (float), avg_dmg_players (float), avg_dmg_enemies (float)).
    """
    results = defaultdict(list)
    for _ in range(num_runs):
        # Create fresh copies of participants for each simulation
        players_copy = [Participant(p.name, p.max_hp, p.attack, p.defense, p.speed) for p in players]
        enemies_copy = [Participant(e.name, e.max_hp, e.attack, e.defense, e.speed) for e in enemies]
        victory, rounds, dmg_players, dmg_enemies = simulate_combat(
            players_copy, enemies_copy, attack_multiplier, defense_multiplier
        )
        results['victory'].append(victory)
        results['rounds'].append(rounds)
        results['dmg_players'].append(dmg_players)
        results['dmg_enemies'].append(dmg_enemies)
    
    # Calculate averages
    avg_victory = sum(results['victory']) / num_runs
    avg_rounds = sum(results['rounds']) / num_runs
    avg_dmg_players = sum(results['dmg_players']) / num_runs
    avg_dmg_enemies = sum(results['dmg_enemies']) / num_runs
    return avg_victory, avg_rounds, avg_dmg_players, avg_dmg_enemies

class TestCombatScenarios(unittest.TestCase):
    """Unit tests for combat scenarios with varying multipliers."""
    
    def setUp(self):
        """Set up default multipliers before each test."""
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0

    def run_scenario(self, players, enemies, scenario_name, expected_victory_range):
        """Helper method to run a scenario and assert victory rate.
        
        Args:
            players (list): List of Player Participant objects.
            enemies (list): List of Enemy Participant objects.
            scenario_name (str): Descriptive name of the scenario.
            expected_victory_range (tuple): (min, max) expected victory rate range.
        """
        avg_victory, avg_rounds, avg_dmg_players, avg_dmg_enemies = run_multiple_simulations(
            players, enemies, self.attack_multiplier, self.defense_multiplier
        )
        # Print formatted output with colors and spacing
        print(f"\n{'=' * 50}")
        print(f"{Fore.YELLOW}{scenario_name}{Style.RESET_ALL}")
        print(f"  Victory: {Fore.GREEN if avg_victory >= expected_victory_range[0] and avg_victory <= expected_victory_range[1] else Fore.RED}{avg_victory:.2%}{Style.RESET_ALL}")
        print(f"  Rounds: {avg_rounds:.2f}")
        print(f"  Dmg Players: {avg_dmg_players:.2f}")
        print(f"  Dmg Enemies: {avg_dmg_enemies:.2f}")
        print(f"{'=' * 50}\n")
        self.assertGreaterEqual(avg_victory, expected_victory_range[0])
        self.assertLessEqual(avg_victory, expected_victory_range[1])

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
        self.defense_multiplier = 1.5  # Keep high defense for enemies
        warrior = Participant("Warrior", 50, 10, 5, 10)
        mage = Participant("Mage", 30, 8, 3, 12)
        dragon = Participant("Dragon", 100, 15, 8, 9)
        self.run_scenario([warrior, mage], [dragon], "Boss Fight (Defender-Favored)", (0.0, 0.3))  # Adjusted range

    def test_underdog_challenge_scaled(self):
        """Test an underdog challenge with scaled multipliers."""
        self.attack_multiplier = 1.2
        self.defense_multiplier = 1.2
        thief = Participant("Thief", 25, 7, 2, 15)
        wolves = [Participant("Wolf", 30, 8, 3, 10) for _ in range(2)]
        self.run_scenario([thief], wolves, "Underdog Challenge (Scaled)", (0.0, 0.1))  # Adjusted range

    def test_attrition_test_extreme(self):
        """Test an attrition scenario with extreme multipliers."""
        self.attack_multiplier = 2.0
        self.defense_multiplier = 0.5
        warrior = Participant("Warrior", 50, 10, 5, 10)
        imps = [Participant("Imp", 15, 4, 1, 7) for _ in range(5)]
        self.run_scenario([warrior], imps, "Attrition Test (Extreme)", (0.9, 1.0))  # Relaxed range

if __name__ == "__main__":
    unittest.main()