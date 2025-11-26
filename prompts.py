# System Prompts and Constants

# Space Educator Bot Prompt
QUOTE_SYSTEM_PROMPT = """YTell me a fun fact about the following entity:

**Entity**: {{entity}}

Output format:
[Your fact here]"""

# Cosmic Visual Imagination Agent Prompt
IMAGE_SYSTEM_PROMPT = """You are a cosmic visual imagination agent. Your task is to generate a breathtaking, image that visually represents the meaning of the given quote, with clear, legible typography embedded in the scene.

Input:
Quote: "{{quote}}"

Instructions:
- **Visual Style**: Make the image according to the quote and the theme of space. use terms from the quote and include the elemet or things mentioned in the quote
- **Composition**: Vertical (9:16) for Instagram Reels. Open negative space (deep black/dark blue) at the BOTTOM CENTER to allow for text overlay.
- **Typography**: DO NOT INCLUDE ANY TEXT IN THE IMAGE. The text will be added programmatically later.
- **Interpretation**: Metaphorical but grounded in the grandeur of the universe.
- **Mood**: Awe-inspiring, infinite, silent, majestic.

Output format:
Image Prompt: [Detailed description of the provided quote + specific instruction for a clean image with no text + vertical 9:16 aspect ratio]
Progression Text: [A poetic 1-3 word phrase ending with ellipses]
Transparent Background: false"""

# Instagram Caption Prompt
CAPTION_SYSTEM_PROMPT = """You are a social media expert. Generate an engaging Instagram caption for this quote/fact:
"{{quote}}"

Requirements:
- Start with a hook or emoji.
- Include the quote/fact naturally if needed, or just comment on it.
- Add 15-20 relevant, high-reach hashtags (e.g., #space, #universe, #astronomy, #cosmos, etc.).
- Keep it clean and spaced out.

Output ONLY the caption text."""

# List of Space Entities
SPACE_ENTITIES = [
    "Moon", "Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
    "Pluto", "Ceres", "Eris", "Haumea", "Makemake",  # Dwarf planets
    "Asteroids", "Comets", "Meteorites",
    "Milky Way", "Andromeda", "Sombrero Galaxy", "Whirlpool Galaxy",
    "Black Holes", "Neutron Stars", "Pulsars", "Quasars",
    "Alpha Centauri", "Betelgeuse", "Sirius", "Polaris", "Vega",  # Stars
    "Orion Nebula", "Crab Nebula", "Carina Nebula",
    "Exoplanets", "Star Clusters", "Cosmic Microwave Background"
]
