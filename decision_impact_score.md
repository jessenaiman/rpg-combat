# What is the Decision Impact Score?

The Decision Impact Score is a metric designed to evaluate the dynamism and strategic depth of combat scenarios in an RPG (role-playing game) setting. It measures how often players need to adapt their strategies—such as switching from attacking to defending—based on critical changes, like health dropping below a certain threshold (e.g., 50% HP). This score is particularly useful for assessing player engagement, as it rewards combat systems that require thoughtful decision-making over rote or predictable actions.

## Definition and Calculation

The Decision Impact Score quantifies the frequency of meaningful strategic shifts during combat. It's calculated as:

$$ \text{Decision Impact Score} = \left( \frac{\text{Number of Optimal Decision Shifts}}{\text{Total Turns}} \right) \times 100 $$

Where:
- **Optimal Decision Shifts**: These occur when a player's health crosses a predefined threshold (e.g., 50% HP), prompting a change in tactics
- **Total Turns**: The total number of combat rounds in a given scenario

A higher score indicates more frequent decision points, suggesting a combat system that keeps players engaged by demanding adaptability. A score of 0% implies a static fight where strategy rarely changes.

## Insights from Simulation Results

### Attrition Test (Extreme)
**Stats**: Victory 0.86%, Rounds 3.80, Damage Players 50.68, Damage Enemies 54.80  
**Analysis**: With only 3.80 rounds on average and a near-zero victory rate, fights end quickly. Decision Impact Score likely very low (~0%).

### Boss Fight (Defender-Favored)
**Stats**: Victory 0.08%, Rounds 10.08, Damage Players 15.73, Damage Enemies 39.00  
**Analysis**: Longer fights offer more turns for potential decision shifts. Decision Impact Score moderate (5-10%).

### Underdog Challenge (Scaled)
**Stats**: Victory 0.08%, Rounds 2.08, Damage Players 10.00, Damage Enemies 28.00  
**Analysis**: Very short rounds show rapid defeats. Decision Impact Score near 0%.

### Party vs. Mob (Attacker-Favored)
**Stats**: Victory 100%, Rounds 3.08, Damage Players 69.00, Damage Enemies 12.86  
**Analysis**: Quick wins with minimal damage taken. Decision Impact Score 0%.

### Solo Warrior vs. Goblin (Balanced)
**Stats**: Victory 100%, Rounds 3.08, Damage Players 24.00, Damage Enemies 2.00  
**Analysis**: One-sided win with low enemy damage. Decision Impact Score 0%.

## Recommendations

1. Target balanced scenarios (40-60% victory rates)
2. Add dynamic elements to trigger strategic shifts
3. Iterate and test for scores of 10-20% as engagement sweet spot

## Conclusion

The Decision Impact Score helps design RPG combat that rewards adaptability. Current simulations show extreme scenarios yield low scores, suggesting poor engagement. Future development should focus on balanced encounters that encourage strategic thinking.