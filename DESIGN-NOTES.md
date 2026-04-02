# Design Notes

## Product goal

Shadow Mage is a portable agent-conversion overlay for OpenClaw.
The goal is not merely persona replacement. The goal is to create a robust teaching agent for MTG-literate users who are new to OpenClaw.

## Core design pillars

1. **Persona** — Shadow Mage should feel distinct, confident, and flavorful.
2. **Education** — it should actively teach OpenClaw by mapping concepts onto MTG mechanics.
3. **Novelty** — it should surprise and delight through card references and concept-card rendering.
4. **Robustness** — it should still function when enrichment paths fail.

## Technical notes

- Scryfall is the primary real-card data source.
- Anchored presets can use Scryfall `art_crop` artwork.
- Unanchored concept cards fall back to a deterministic local template renderer.
- Concept card mana symbols use local Mana font assets.
- The renderer emits explicit art-source metadata so the agent can report truthfully.
