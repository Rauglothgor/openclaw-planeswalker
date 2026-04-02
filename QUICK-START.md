# Quick Start

This guide is written for a novice installer.

## What you are doing

You are taking the Shadow Mage overlay package and applying it to a target OpenClaw agent workspace so that agent becomes:
- a Shadow Mage persona
- an MTG-based OpenClaw teacher
- a card-generating novelty/education agent

## What you need first

Before you start, make sure the target environment has:

- an existing OpenClaw agent workspace
- `python3` available
- Python virtual environment support (`python3 -m venv`)
- internet access for Scryfall lookups

## Important first-run behavior

The concept-card system uses a wrapper script that may create a local Python virtual environment and install Pillow on first use.

That means the first card render may be slower than normal. This is expected.

## Recommended install method

Do **not** rely on a blind installer script.

Instead, use an existing capable OpenClaw agent and give it the installation prompt from the README. That agent should:
- overlay the package intentionally
- preserve the target workspace shape
- avoid copying junk like runtime state, backups, or test files
- verify the result after applying it

## After install, test in this order

1. Ask the agent who it is
2. Ask it to fetch **Black Lotus** and show the image
3. Ask it to render the `soul` preset
4. Ask it to render the `lotus` preset
5. Ask which art source each card used

## Success criteria

You are successful if:
- the agent behaves like Shadow Mage
- Scryfall card lookup works
- concept cards render successfully
- mana symbols look correct
- anchored presets can use Scryfall art
- unanchored presets fall back cleanly
