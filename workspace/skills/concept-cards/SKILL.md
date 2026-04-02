---
name: concept-cards
description: "Render custom MTG-style concept cards that teach OpenClaw architecture using card text grammar. Use this skill when you want to visually explain an OpenClaw concept by rendering it as a Magic: The Gathering card with oracle text written in card text grammar. The card renderer creates classic-frame card images with custom names, types, oracle text, flavor text, mana costs, and color frames. Includes preset concept cards for common OpenClaw concepts (heartbeat, SOUL.md, context window, tool policy, session reset, etc.) and supports fully custom cards."
---

# OpenClaw Concept Card Renderer

Render custom MTG-style cards that teach OpenClaw concepts using card text grammar.

## When to Use

Use this skill when teaching an OpenClaw concept and a visual card would reinforce the lesson. The concept card shows the OpenClaw behavior written as MTG oracle text — triggered abilities, activated abilities, static abilities, and restrictions — in a classic card frame the user will recognize.

Use concept cards for key teaching moments, not every interaction. One concept card per teaching session is the right frequency. The card should anchor the lesson, not replace the conversation.

## Presets

Render a preset concept card:

```bash
skills/concept-cards/bin/render_card --preset heartbeat --output /tmp/heartbeat.png
skills/concept-cards/bin/render_card --preset soul --output /tmp/soul.png
skills/concept-cards/bin/render_card --list-presets
```

Available presets: `heartbeat`, `soul`, `context_window`, `null_rod`, `session_reset`, `graveyard_weight`, `memory_write`, `strip_mine`, `mind_twist`, `time_walk`, `weatherlight`, `lotus`

## Custom Cards

Render a custom concept card for any OpenClaw concept:

```bash
skills/concept-cards/bin/render_card \
    --name "Model Resolver" \
    --type "Enchantment" \
    --cost "{2}{U}" \
    --color blue \
    --text "If a spell you cast would fail to resolve, instead cast it using the next available mana source.\n(If the primary API provider fails, route to the fallback.)" \
    --flavor "The resolver handled it. You noticed nothing." \
    --output /tmp/resolver.png
```

### Parameters

- `--name` — Card name (the OpenClaw concept name)
- `--cost` — Mana cost in `{symbol}` format: `{W}`, `{U}`, `{B}`, `{R}`, `{G}`, `{1}`, `{2}`, `{X}`, `{T}`
- `--type` — Type line: `Enchantment`, `Artifact`, `Sorcery`, `Instant`, `Creature — Type`, `Land`
- `--text` — Oracle text. Use `\n` for line breaks. Write in card text grammar (triggered/activated/static abilities)
- `--flavor` — Flavor text (appears italic, below separator line)
- `--color` — Frame color: `white`, `blue`, `black`, `red`, `green`, `gold`, `colorless`, `artifact`
- `--power`, `--toughness` — For creature cards
- `--output` — Output file path (PNG)

### JSON input

```bash
skills/concept-cards/bin/render_card --json '{"name":"My Card","type_line":"Artifact","oracle_text":"Card text here","color":"artifact"}' --output /tmp/card.png
```

## Card Text Grammar Guide

Write oracle text using MTG card text patterns:

- **Triggered ability:** "At the beginning of [event], [effect]." / "When [event], [effect]." / "Whenever [condition], [effect]."
- **Activated ability:** "{cost}: {effect}." / "{T}, {cost}: {effect}."
- **Static ability:** "As long as [condition], [effect]." / "[Things] have [ability]."
- **Replacement effect:** "If [event] would [happen], [do this instead]."
- **Restriction:** "[This] can't be [action]." / "Prevent [effect]."
- **Reminder text:** Use parentheses for plain-English explanations: "(This maps to HEARTBEAT.md in OpenClaw.)"

## Dependencies

Requires Python 3. Wrapper `skills/concept-cards/bin/render_card` auto-creates a local venv in the workspace and installs Pillow if needed. Uses system fonts (DejaVu Sans/Serif on Linux).

## Output

Renders 745×1040 PNG images in classic pre-8th-Edition card frame style. Suitable for display in Telegram, Discord, WhatsApp, and other chat channels.
