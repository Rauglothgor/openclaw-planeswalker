# Shadow Mage

**Teach OpenClaw through Magic: The Gathering.**

<img src="media/jared-carthalion-shadow-mage.png" alt="Jared Carthalion, the Shadow Mage" width="420" />

> A dispossessed heir, a beggar-prince, a keeper of Moxes, and a survivor who reaches power through discipline rather than entitlement. That is the emotional center of the **Shadow Mage**.

Shadow Mage is a portable OpenClaw agent overlay that turns a new or existing agent into an MTG-fluent guide for users who already understand Magic but not OpenClaw.

It does three things at once:
- adopts the **Shadow Mage** persona
- teaches **OpenClaw concepts using MTG mechanics and metaphors**
- adds **novelty and delight** through real MTG card lookups and custom concept-card rendering

The quality bar is not flavor for its own sake. The MTG overlay only stays if it creates **conceptual compression** — if it makes OpenClaw easier to understand than plain-English explanation alone would.

## Who this is for

This repo is for someone who already has an OpenClaw agent and wants to transform that agent into **Shadow Mage** — a guide who teaches OpenClaw through Magic: The Gathering.

You do not need to manually figure out the internals of the package first. If you can get to your OpenClaw agent, that is enough.

## The simple install path

This package is meant to be installed the easy way:

1. download **`shadow-mage-overlay-package.zip`** from this repo
2. give that zip file to your existing OpenClaw agent
3. copy the install prompt below
4. paste the prompt to your agent
5. let the agent apply the package, handle setup, and verify the result

That is the intended experience.

The repo is for distribution and inspection.
The **zip + prompt** is the install path.

## Installation Prompt

Give this prompt to your existing OpenClaw agent together with the downloaded package zip:

```text
Apply this Shadow Mage overlay package onto the target agent workspace and do everything needed to make the target agent fully usable as Shadow Mage.

Your job is not just to copy files. Your job is to finish the installation completely and verify that it really works.

Goals:
- turn the target agent into Shadow Mage
- preserve the target workspace shape instead of mutating folders to fit the package
- overlay only the intended runtime files from `workspace/`
- include the references and skills
- avoid copying runtime junk, backups, test renders, local virtual environments, or workspace-state files
- keep local quirks that should survive, but prefer the package versions for Shadow Mage persona/teaching behavior

You must also handle setup work needed for the installed skills to function. Do not push technical setup back to the user if you can handle it yourself.

Before you claim success, you must explicitly check and handle these requirements in the target environment:
- `python3` exists and runs
- `python3 -m venv` works
- the target workspace can create and use a local venv for concept-cards
- outbound network access is available for Scryfall lookups
- the concept-cards wrapper path is present and used instead of the direct script path
- if first-run bootstrap is needed for concept-cards, perform it

Specifically:
- overlay `workspace/AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, and `MEMORY.md` into the target agent workspace
- overlay `workspace/references/` into the target workspace `references/`
- overlay `workspace/skills/` into the target workspace `skills/`
- ensure concept-cards keeps its wrapper/bootstrap path and mana assets
- prefer the concept-cards wrapper path over direct script invocation
- do not alter unrelated workspace structure just to make the package fit

After applying, verify all of this yourself:
1. the agent starts and responds in Shadow Mage voice
2. Scryfall lookup works
3. a concept-card preset render works
4. the `lotus` preset can use Scryfall art
5. the `soul` preset can fall back locally
6. mana symbols render correctly
7. the renderer can report the art source truthfully

Then report exactly:
- what changed
- what you verified
- what setup/bootstrap you had to perform
- anything that still needs human attention

Do not stop at file copy if the installed skills are not actually usable.
```

## Suggested Validation Checklist

If you want to sanity-check the result afterward, do these in order:

1. Ask the agent who it is
2. Ask it to fetch **Black Lotus** and show the image
3. Ask it to render the `soul` preset
4. Ask it to render the `lotus` preset
5. Ask which art source each card used

If those work, the Shadow Mage install is in good shape.

## Notes

- This is an **overlay package**, not a full OpenClaw workspace export.
- It intentionally excludes transient runtime state, venvs, backups, and test renders.
- Concept-card rendering bootstraps its own local venv when needed.
- Real MTG anchor art uses Scryfall where configured; otherwise concept cards fall back to the local template renderer.
- The package includes a Jared Carthalion lore note in `references/jared-carthalion-shadow-mage.md` for flavor, inspiration, and future refinement.

## Attribution / Disclaimer

This is an unofficial fan project.

- **Magic: The Gathering** and related names, characters, and properties are owned by **Wizards of the Coast**. No endorsement by Wizards of the Coast is implied.
- Real card data and images are sourced through **[Scryfall](https://scryfall.com/)** and the **[Scryfall API](https://scryfall.com/docs/api)**, subject to their usage guidelines.
- Mana symbol assets used for the concept-card renderer are based on **[Mana by Andrew Gioia](https://github.com/andrewgioia/mana)**.
- Jared Carthalion lore material included in this repo is fan-facing reference/inspiration material. Some framing and synthesis in the repo is interpretive rather than official canon wording.

## Vibe

Part tutorial. Part spellbook. Part novelty engine.

OpenClaw, taught through the color pie.
