import gradio as gr
import plotly.graph_objects as go
from combat import run_multiple_simulations
from participant import Participant

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
    demo.launch()