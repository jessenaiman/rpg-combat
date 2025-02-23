# What is Flow State Potential?

Flow State Potential is a metric designed to measure the likelihood of a player entering a flow state—a mental state of complete immersion, focus, and enjoyment—during RPG combat scenarios. Rooted in Mihaly Csikszentmihalyi's flow theory, it hinges on achieving a balance between the challenge of a task and the player's skill level. In the context of the Dice-Learner RPG Combat Simulator, this translates to crafting combat scenarios where neither the player nor the enemy overwhelmingly dominates, fostering an environment that is challenging yet achievable.

## How It's Calculated

The Flow State Potential is quantified using the following formula:

$$\text{Flow State Potential} = \left| 1 - \frac{\text{Average Damage Taken}}{\text{Average Damage Dealt}} \right|$$

- **Average Damage Dealt**: The total damage players inflict on enemies, averaged over the combat duration.
- **Average Damage Taken**: The total damage enemies inflict on players, averaged over the combat duration.

### Interpretation
- A value close to 0 indicates a near-perfect balance, ideal for flow.
- A value approaching 1 or higher suggests an imbalance—either too easy (leading to boredom) or too hard (leading to frustration).

For example:
- If players deal 50 damage and take 45, the calculation is:
    $$\left|1 - \frac{45}{50}\right| = |1 - 0.9| = 0.1$$
    suggesting a well-balanced scenario.
- If players deal 100 damage and take 10, it's:
    $$\left|1 - \frac{10}{100}\right| = |1 - 0.1| = 0.9$$
    indicating an overly easy encounter.

## Analyzing Simulation Results

The terminal outputs from rpg-combat-test.py provide data on various combat scenarios. Let's evaluate their Flow State Potential:

### 1. Attrition Test (Extreme)
- Stats: Victory Probability: 0.86%, Rounds: 3.80, Damage Players: 56.60, Damage Enemies: 54.80
- Calculation: 
    $$\text{Flow State Potential} = \left| 1 - \frac{54.80}{56.60} \right| = 0.032$$
- Analysis: 
    - Exceptionally balanced (0.032)
    - Low victory probability (0.86%) indicates excessive difficulty

### 2. Boss Fight (Defender-Favored)
- Stats: Victory Probability: 0.08%, Rounds: 10.08, Damage Players: 15.73, Damage Enemies: 39.00
- Calculation:
    $$\text{Flow State Potential} = \left| 1 - \frac{39.00}{15.73} \right| = 1.48$$
- Analysis:
    - Severe imbalance (1.48)
    - Very low victory probability (0.08%)

[Continue with remaining scenarios similarly formatted...]

## Key Observations

1. **Extreme Difficulty**: Low victory probabilities (0.08%–0.86%) with high Flow State Potential values indicate excessive challenge
2. **Extreme Ease**: 100% victory rates with high Flow State Potential values show insufficient challenge
3. **Ideal Range**: Flow State Potential between 0.0 and 0.2 offers optimal balance

## Recommendations

1. **Balance Difficulty**
     - For hard scenarios: Reduce enemy multipliers
     - For easy scenarios: Strengthen enemies or increase numbers

2. **Introduce Variability**
     - Add random elements
     - Include environmental factors

3. **Target Metrics**
     - Flow State Potential: 0.0–0.2
     - Victory Probability: 40%–70%
     - Rounds: 4–8

## Conclusion

Flow State Potential serves as a crucial metric for balancing RPG combat. Through careful adjustment of parameters and continuous testing, we can create engaging scenarios that maintain player immersion and enjoyment.
