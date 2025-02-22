import random

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