import random
from collections import defaultdict
import math
from participant import Participant

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