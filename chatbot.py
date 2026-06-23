"""Planet chatbot logic - rule-based responses about planets and the solar system."""

import re

PLANET_DATA = {
    "mercury": {
        "description": "Mercury is the smallest planet in our solar system and the closest to the Sun.",
        "distance_from_sun": "57.9 million km",
        "moons": 0,
        "diameter": "4,879 km",
        "day_length": "59 Earth days",
        "year_length": "88 Earth days",
        "temperature": "-180°C to 430°C",
        "fun_fact": "Mercury has no atmosphere, causing extreme temperature swings.",
    },
    "venus": {
        "description": "Venus is the second planet from the Sun and the hottest planet in our solar system.",
        "distance_from_sun": "108.2 million km",
        "moons": 0,
        "diameter": "12,104 km",
        "day_length": "243 Earth days",
        "year_length": "225 Earth days",
        "temperature": "465°C (average)",
        "fun_fact": "A day on Venus is longer than a year on Venus.",
    },
    "earth": {
        "description": "Earth is the third planet from the Sun and the only known planet to harbour life.",
        "distance_from_sun": "149.6 million km",
        "moons": 1,
        "diameter": "12,742 km",
        "day_length": "24 hours",
        "year_length": "365.25 days",
        "temperature": "-88°C to 58°C",
        "fun_fact": "Earth is the densest planet in the solar system.",
    },
    "mars": {
        "description": "Mars is the fourth planet from the Sun, often called the Red Planet.",
        "distance_from_sun": "227.9 million km",
        "moons": 2,
        "diameter": "6,779 km",
        "day_length": "24 hours 37 minutes",
        "year_length": "687 Earth days",
        "temperature": "-125°C to 20°C",
        "fun_fact": "Mars has the tallest volcano in the solar system — Olympus Mons.",
    },
    "jupiter": {
        "description": "Jupiter is the fifth planet from the Sun and the largest planet in our solar system.",
        "distance_from_sun": "778.5 million km",
        "moons": 95,
        "diameter": "139,820 km",
        "day_length": "10 hours",
        "year_length": "12 Earth years",
        "temperature": "-110°C (cloud tops)",
        "fun_fact": "Jupiter's Great Red Spot is a storm that has lasted over 350 years.",
    },
    "saturn": {
        "description": "Saturn is the sixth planet from the Sun, famous for its stunning ring system.",
        "distance_from_sun": "1.43 billion km",
        "moons": 146,
        "diameter": "116,460 km",
        "day_length": "10.7 hours",
        "year_length": "29 Earth years",
        "temperature": "-140°C (average)",
        "fun_fact": "Saturn is the least dense planet — it would float on water.",
    },
    "uranus": {
        "description": "Uranus is the seventh planet from the Sun and rotates on its side.",
        "distance_from_sun": "2.87 billion km",
        "moons": 28,
        "diameter": "50,724 km",
        "day_length": "17 hours",
        "year_length": "84 Earth years",
        "temperature": "-195°C (average)",
        "fun_fact": "Uranus rotates on an axial tilt of 98°, essentially on its side.",
    },
    "neptune": {
        "description": "Neptune is the eighth and farthest known planet from the Sun.",
        "distance_from_sun": "4.5 billion km",
        "moons": 16,
        "diameter": "49,244 km",
        "day_length": "16 hours",
        "year_length": "165 Earth years",
        "temperature": "-200°C (average)",
        "fun_fact": "Neptune has the strongest winds in the solar system, reaching 2,100 km/h.",
    },
}

SOLAR_SYSTEM_FACTS = [
    "Our solar system is about 4.6 billion years old.",
    "The Sun contains 99.86% of the solar system's total mass.",
    "There are 8 planets in our solar system.",
    "The asteroid belt lies between Mars and Jupiter.",
    "The Kuiper Belt is a region beyond Neptune filled with icy bodies.",
    "Pluto was reclassified as a dwarf planet in 2006.",
    "Light from the Sun takes about 8 minutes to reach Earth.",
    "The solar system is located in the Milky Way galaxy.",
]

GREETINGS = {"hi", "hello", "hey", "greetings", "howdy", "hola"}

HELP_TEXT = (
    "I can help you explore our solar system! Try asking me:\n"
    "• 'Tell me about Mars'\n"
    "• 'How many moons does Jupiter have?'\n"
    "• 'What is the temperature on Venus?'\n"
    "• 'How far is Saturn from the Sun?'\n"
    "• 'Give me a fun fact about Neptune'\n"
    "• 'List all planets'\n"
    "• 'Solar system fact'"
)


def _find_planet(text: str) -> str | None:
    """Return the first planet name found in *text*, or None."""
    text_lower = text.lower()
    for planet in PLANET_DATA:
        if planet in text_lower:
            return planet
    return None


def _planet_summary(planet: str) -> str:
    data = PLANET_DATA[planet]
    return (
        f"**{planet.capitalize()}**\n"
        f"{data['description']}\n\n"
        f"• Distance from Sun: {data['distance_from_sun']}\n"
        f"• Diameter: {data['diameter']}\n"
        f"• Moons: {data['moons']}\n"
        f"• Day length: {data['day_length']}\n"
        f"• Year length: {data['year_length']}\n"
        f"• Temperature: {data['temperature']}\n"
        f"• Fun fact: {data['fun_fact']}"
    )


def get_response(user_message: str) -> str:
    """Return a chatbot response for the given *user_message*."""
    text = user_message.strip()
    if not text:
        return "Please type a message!"

    lower = text.lower()

    # Greeting
    first_word = re.split(r"\W+", lower)[0]
    if first_word in GREETINGS or lower in GREETINGS:
        return (
            "Hello! 👋 Welcome to the Planet Explorer chatbot! "
            "I can answer questions about the planets in our solar system. "
            "Type 'help' to see what I can do."
        )

    # Help
    if "help" in lower or "what can you do" in lower:
        return HELP_TEXT

    # List planets
    if re.search(r"\b(list|all|name).*(planet|planets)\b", lower) or re.search(
        r"\bplanets?\b.*\b(list|all)\b", lower
    ):
        names = ", ".join(p.capitalize() for p in PLANET_DATA)
        return f"The 8 planets of our solar system are:\n{names}"

    # Solar system fact
    if "solar system" in lower and re.search(r"\bfact\b", lower):
        import random
        return random.choice(SOLAR_SYSTEM_FACTS)

    planet = _find_planet(lower)

    if planet is None:
        # Generic solar system / space questions
        if "solar system" in lower:
            import random
            return random.choice(SOLAR_SYSTEM_FACTS)
        if "planet" in lower:
            return (
                "I know all about the 8 planets! Ask me about a specific one, "
                "or say 'list planets' to see them all."
            )
        return (
            "I'm not sure about that. I specialise in planets and the solar system. "
            "Type 'help' for a list of things you can ask me."
        )

    # Planet-specific queries
    if re.search(r"\b(moon|moons)\b", lower):
        count = PLANET_DATA[planet]["moons"]
        if count == 0:
            return f"{planet.capitalize()} has no moons."
        return f"{planet.capitalize()} has {count} moon{'s' if count != 1 else ''}."

    if re.search(r"\b(temperature|temp|hot|cold)\b", lower):
        return (
            f"The temperature on {planet.capitalize()} is "
            f"{PLANET_DATA[planet]['temperature']}."
        )

    if re.search(r"\b(distance|far|close|km)\b", lower):
        return (
            f"{planet.capitalize()} is {PLANET_DATA[planet]['distance_from_sun']} "
            f"from the Sun."
        )

    if re.search(r"\b(diameter|size|big|large|small)\b", lower):
        return (
            f"The diameter of {planet.capitalize()} is "
            f"{PLANET_DATA[planet]['diameter']}."
        )

    if re.search(r"\b(day|rotation|rotate)\b", lower):
        return (
            f"A day on {planet.capitalize()} lasts "
            f"{PLANET_DATA[planet]['day_length']}."
        )

    if re.search(r"\b(year|orbit|revolution)\b", lower):
        return (
            f"{planet.capitalize()} takes {PLANET_DATA[planet]['year_length']} "
            f"to complete one orbit around the Sun."
        )

    if re.search(r"\b(fun fact|fact|interesting|cool|wow)\b", lower):
        return f"Fun fact about {planet.capitalize()}: {PLANET_DATA[planet]['fun_fact']}"

    # Default: full summary
    return _planet_summary(planet)
