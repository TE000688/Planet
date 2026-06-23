# Planet Explorer Chatbot 🪐

A lightweight Flask web application that lets users chat with a rule-based bot about the planets in our solar system.

## Features

- **Planet information** – ask about any of the 8 planets (Mercury → Neptune)
- **Specific queries** – moons, temperature, distance from the Sun, diameter, day/year length, fun facts
- **Modern chat UI** – dark space-themed interface with typing indicator
- **No external APIs required** – fully self-contained

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

## Example Questions

| You type | Bot answers |
|----------|-------------|
| `tell me about Mars` | Full Mars fact sheet |
| `how many moons does Jupiter have?` | 95 |
| `temperature on Venus` | 465°C |
| `how far is Saturn from the Sun?` | 1.43 billion km |
| `fun fact about Neptune` | Strongest winds in the solar system |
| `list all planets` | Mercury, Venus, Earth… |
| `help` | Full list of supported queries |

## Project Structure

```
Planet/
├── app.py              # Flask application & routes
├── chatbot.py          # Rule-based chatbot logic
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Chat UI
├── static/
│   ├── css/style.css   # Styling
│   └── js/chat.js      # Frontend JavaScript
└── tests/
    └── test_chatbot.py # pytest test suite
```

## Running Tests

```bash
pip install pytest
pytest tests/
```