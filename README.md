# Shadow Mage

**Teach OpenClaw through Magic: The Gathering.**

![Jared Carthalion, the Shadow Mage](media/jared-carthalion-shadow-mage.png)

> A dispossessed heir, a beggar-prince, a keeper of Moxes, and a survivor who reaches power through discipline rather than entitlement. That is the emotional center of Shadow Mage.

Shadow Mage is a portable OpenClaw agent overlay that turns a new or existing agent into an MTG-fluent guide for users who already understand Magic but not OpenClaw.

It does three things at once:
- adopts the **Shadow Mage** persona
- teaches **OpenClaw concepts using MTG mechanics and metaphors**
- adds **novelty and delight** through real MTG card lookups and custom concept-card rendering

The quality bar is not flavor for its own sake. The MTG overlay only stays if it creates **conceptual compression** — if it makes OpenClaw easier to understand than plain-English explanation alone would.

## Who this is for

This repo is for someone who already understands **Magic: The Gathering** much better than they understand **OpenClaw**.

It assumes you may be new to:
- OpenClaw agent workspaces
- skill folders
- persistent instruction files
- Python helper scripts
- the difference between a persona prompt and a real installed capability

This package is meant to give you a Shadow Mage agent **without requiring you to invent the system yourself**.

## What this package includes

- Shadow Mage persona files (`SOUL.md`, `AGENTS.md`, `IDENTITY.md`, etc.)
- MTG ↔ OpenClaw teaching references
- **Scryfall skill** for real card lookups and images
- **Concept card renderer** for custom MTG-style OpenClaw teaching cards
- built-in **mana symbol assets**
- wrapper-based local dependency bootstrap for concept-card rendering
- Scryfall-art support for anchored presets and deterministic local fallback for non-anchored cards

## Intended result

Overlay this onto a new or existing OpenClaw agent workspace and that agent becomes a proactive educational guide that explains OpenClaw like a planeswalker explaining the stack to a new mage.

## Package layout

This repo is intentionally shaped as an overlay package:

- `workspace/...` → overlay onto the target agent workspace root
- `workspace/references/...` → target workspace `references/`
- `workspace/skills/...` → target workspace `skills/`

## Before You Install

You do **not** need to be an expert, but you do need a few basics available in the target environment:

- an existing OpenClaw agent workspace to apply the overlay to
- `python3` available on the host
- Python venv support available (`python3 -m venv`)
- outbound network access for Scryfall lookups
- permission for the target agent to read/write its workspace files

### Important first-run note

The concept-card renderer uses a wrapper script:

- `skills/concept-cards/bin/render_card`

On first use, that wrapper may create a **local virtual environment** and install **Pillow** automatically. That means the **first concept-card render may take longer than later renders**. This is expected.

Do **not** assume the feature is broken just because the first render is slower.

Do **not** use the direct script path for normal use if the wrapper exists. Prefer:

- `skills/concept-cards/bin/render_card`

over:

- `skills/concept-cards/scripts/render_card.py`

## Installation Prompt

Use this with an existing OpenClaw agent that has access to the unpacked package files:

```text
Apply this Shadow Mage overlay package onto the target agent workspace.

Goals:
- make the target agent behave as Shadow Mage
- preserve the target workspace shape instead of mutating folders to fit the package
- overlay only the intended runtime files from `workspace/`
- include the references and skills
- do not copy runtime junk, backups, venvs, test renders, or workspace-state files
- keep local quirks that should survive, but prefer the package versions for Shadow Mage persona/teaching behavior

Specifically:
- overlay `workspace/AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, and `MEMORY.md` into the target agent workspace
- overlay `workspace/references/` into the target workspace `references/`
- overlay `workspace/skills/` into the target workspace `skills/`
- ensure concept-cards keeps its wrapper/bootstrap path and mana assets
- do not alter unrelated workspace structure just to make the package fit

After applying:
1. verify the agent starts and responds in Shadow Mage voice
2. verify Scryfall lookup works
3. verify a concept-card preset render works
4. verify an anchored preset can use Scryfall art and an unanchored preset can fall back locally
5. report exactly what was changed and any mismatches or skipped files
```

This package is best applied intentionally by an agent, not blindly copied by a generic installer.

## Suggested Validation Checklist

If you are new to this, do these checks in order after installation:

### 1. Basic persona check
Start a fresh session with the target agent and ask who it is.

You are looking for:
- Shadow Mage voice
- MTG-fluent teaching tone
- practical help, not just theatrical roleplay

### 2. Real card lookup check
Ask the agent to fetch **Black Lotus** and show the image.

You are looking for:
- successful Scryfall lookup
- an actual MTG card image

### 3. Concept-card renderer check
Ask the agent to render a preset concept card.

Start with:
- `soul`

You are looking for:
- an image is actually produced
- mana symbols render correctly
- the card looks like a real teaching card rather than broken placeholder output

### 4. Anchored art check
Ask the agent to render:
- `lotus`

You are looking for:
- the card art box uses real Scryfall anchor art
- the agent can truthfully report that the art source was Scryfall

### 5. Fallback check
Ask the agent to render:
- `soul`

You are looking for:
- the art box falls back to the local template style when no MTG anchor art is configured
- the agent can truthfully report that the art source was the template fallback

## If Something Goes Wrong

### If Scryfall lookup fails
Check:
- the host has outbound internet access
- `python3` works
- the agent can access the installed `skills/scryfall-mtg/` files

### If concept-card rendering fails on first run
Check:
- `python3` exists
- `python3 -m venv` works on that host
- the agent is using the wrapper path, not the direct script path
- the first run may simply need extra time for Pillow bootstrap

### If the persona feels shallow
Check whether the overlay files actually replaced the target agent's persona/instruction files. A prompt can imitate Shadow Mage temporarily, but the package is supposed to install the **behavior stack**, not just style.

## Notes

- This is an **overlay package**, not a full OpenClaw workspace export.
- It intentionally excludes transient runtime state, venvs, backups, and test renders.
- Concept-card rendering bootstraps its own local venv when needed.
- Real MTG anchor art uses Scryfall where configured; otherwise concept cards fall back to the local template renderer.
- The package includes a Jared Carthalion lore note in `references/jared-carthalion-shadow-mage.md` for flavor, inspiration, and future refinement.

## Vibe

Part tutorial. Part spellbook. Part novelty engine.

OpenClaw, taught through the color pie.
