# Quick Start

1. Unpack this package somewhere convenient.
2. Overlay `workspace/` onto the target OpenClaw agent workspace.
3. Preserve the target workspace shape; do not mutate the package to fit weird local folder names.
4. Start a fresh session with the target agent.
5. Test:
   - a real Scryfall card lookup (for example: Black Lotus)
   - a concept-card preset render (for example: soul or lotus)

## Expected behavior

- The agent should respond in the Shadow Mage persona.
- It should teach OpenClaw concepts using MTG language and metaphors.
- It should be able to fetch real MTG card data/images through Scryfall.
- It should be able to render custom concept cards with proper mana symbols.
