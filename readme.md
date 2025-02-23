# Dice-Learner RPG Combat Simulator

## Description
The Dice-Learner RPG Combat Simulator is a Python tool that models turn-based combat scenarios inspired by classics like *Final Fantasy 1* and *Dragon Quest 1-3*. It leverages unit tests, a Gradio UI, and advanced metrics to validate combat balance and explore engagement mechanics, drawing from *"Human Consciousness and Video Games"* and "Narrative Flow Theory."

### Features
- Modular architecture (`participant.py`, `combat.py`, `tests.py`, `ui.py`, `main.py`)
- Dual operation modes: terminal (testing/reports) and Gradio (interactive UI)
- Tabular terminal reporting with CSV export for model training
- Real-time combat simulation with advanced metrics:
   - Tension Index
   - Engagement Variability
   - Flow State Potential
   - Decision Impact Score
   - Narrative Tension Ratio (NTR)
- Comprehensive analytics with theoretical insights

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dice-learner.git
cd dice-learner
```

2. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install gradio plotly colorama tabulate
```

## Usage

### Terminal Mode
```bash
python main.py --mode terminal
```

### Gradio Mode
```bash
python main.py --mode gradio
```

### Combined Mode
```bash
python main.py
```

## Project Status

### Current Features
- Turn-based combat system
- Advanced metrics integration
- Tabular reporting system
- Interactive Gradio interface
- Automated testing suite

### Planned Features
- AI-driven balance optimization
- Enhanced UI capabilities
- Extended combat mechanics
- Advanced metric systems
- Performance optimizations

## Technical Requirements
- Python 3.x
- Gradio
- Plotly
- Colorama
- Tabulate

## Troubleshooting
- Verify Gradio at http://127.0.0.1:7860
- Check terminal permissions for CSV export
- Review test configurations in tests.py

## Contributing
We welcome contributions! Please submit pull requests or open issues via GitHub.

## License
This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2024 Dice-Learner RPG Combat Simulator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
