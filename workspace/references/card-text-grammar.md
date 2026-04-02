# Card Text Grammar → OpenClaw Configuration
## Agent Reference — Read When Teaching Configuration Patterns

The user has been reading MTG card text for years. Card text follows rigid grammatical patterns that map directly to OpenClaw configuration syntax. Use this framework when teaching how to read or write HEARTBEAT.md, AGENTS.md rules, tool policies, or hooks.

The core teaching line: "You already know how to read specifications — you learned it from card text."

---

## Triggered Abilities → Hooks and HEARTBEAT.md

**Card text pattern:** "When [event], [effect]" / "Whenever [condition], [effect]" / "At the beginning of [phase], [effect]"

**OpenClaw equivalent:** Hooks fire on lifecycle events. HEARTBEAT.md entries fire on schedules.

| Card Text Example | OpenClaw Equivalent | Where It Lives |
|---|---|---|
| "At the beginning of your upkeep, scry 1" | "Every 30 minutes, check for pending tasks" | HEARTBEAT.md |
| "At the beginning of your upkeep, draw a card" | "At 6:45 AM, generate morning briefing" | HEARTBEAT.md |
| "When a creature enters the battlefield, do X" | "When a new session starts, read SOUL.md and USER.md" | Hooks / AGENTS.md |
| "Whenever you cast an instant or sorcery, copy it" | "On every tool invocation, log to transcript" | Built-in behavior |
| "When this creature dies, return it to its owner's hand" | "On session end, write important context to MEMORY.md" | AGENTS.md standing order |

**How to teach it:** "See this line in HEARTBEAT.md? 'At 9:00 AM on weekdays, check for project updates.' That's a triggered ability. Same syntax you've been reading on cards. 'At the beginning of [time], [effect].' You already know how to read this."

---

## Activated Abilities → Tool Invocation

**Card text pattern:** "{Cost}: {Effect}." Sometimes with restrictions: "Activate only once each turn." "Activate only as a sorcery."

**OpenClaw equivalent:** Tool calls have a cost (tokens + API credits) and produce an effect (result). Some have restrictions (rate limits, approval requirements, tool policy).

| Card Text Example | OpenClaw Equivalent |
|---|---|
| "{T}: Add {G} to your mana pool" | "Invoke memory_search: returns relevant context" |
| "{2}, {T}: Draw a card" | "Invoke web_search (costs tokens): returns information" |
| "{T}: Destroy target artifact. Activate only as a sorcery." | "Run shell command (costs tokens + risk). Requires approval. Not available mid-task." |
| "Activated abilities of artifacts can't be activated" (Null Rod) | "tools.deny: [list of tools]. These can't be invoked regardless of prompt." |

**How to teach it:** "Every tool the agent uses is an activated ability. There's a cost — tokens and API credits. There's an effect — the result. And some have restrictions — rate limits, approval gates, or Null Rod (tool deny lists) that shut them off entirely."

---

## Static Abilities → SOUL.md and AGENTS.md Rules

**Card text pattern:** Continuous effects with no activation. "Creatures you control get +1/+1." "Players can't gain life." Always in effect as long as the source is in play.

**OpenClaw equivalent:** Rules in SOUL.md and AGENTS.md that are always active as long as the file is loaded. No cost, no activation — they just apply.

| Card Text Example | OpenClaw Equivalent |
|---|---|
| "Creatures you control get +1/+1" | "All responses follow SOUL.md tone and behavioral rules" |
| "Other creatures you control have vigilance" | "AGENTS.md: 'End every conversation with one concrete next action'" |
| "Players can't gain life" | "AGENTS.md: 'Never propose multi-system architecture for a first project'" |
| "Your opponents can't cast spells during your turn" | "AGENTS.md: 'Don't run destructive commands unless explicitly asked'" |

**How to teach it:** "SOUL.md and AGENTS.md rules are static abilities. They don't activate — they just apply. As long as those files are loaded, those rules are in effect. 'Creatures you control get +1/+1' is the same structure as 'all responses follow these behavioral rules.'"

---

## Replacement Effects → Fallback Chains and Guards

**Card text pattern:** "If [event] would [happen], [do this instead]." The original event is replaced — it never happens.

**OpenClaw equivalent:** The model resolver replaces a failed provider with a fallback. The Context Window Guard replaces overflow with compaction.

| Card Text Example | OpenClaw Equivalent |
|---|---|
| "If damage would be dealt to you, prevent that damage" | "If the primary API provider fails, route to the fallback provider" |
| "If a creature would die, instead remove all damage from it" | "If context would overflow, instead trigger compaction (summarize and compress)" |
| "If you would draw a card, instead look at the top three and put one into your hand" | "If memory_search would return all results, instead return the top 3 most relevant" |

**How to teach it:** "The model resolver is a replacement effect. 'If your primary provider would fail, instead route to the fallback.' The original event (failure) never reaches you — it's replaced silently."

---

## Restrictions → Tool Deny Policy

**Card text pattern:** "[This] can't be [action] by [source]." Hard constraints that override everything else.

**OpenClaw equivalent:** Tool deny lists enforced at the Gateway level. These are not advisory — the AI cannot bypass them regardless of prompt instructions.

| Card Text Example | OpenClaw Equivalent |
|---|---|
| "Protection from red" | "tools.deny: exec, shell — can't be invoked by execution tools" |
| "Can't be countered" | "Gateway-enforced policy — no prompt instruction can override this" |
| "Shroud" (can't be targeted) | "Workspace isolation — other agents can't access this agent's files" |

**How to teach it:** "Tool deny lists are protection abilities. 'Protection from shell' means the agent can't use shell tools, period. The Gateway enforces this — it's not a suggestion, it's a rule."

---

## When to Use This Framework

Use card text grammar when the user encounters OpenClaw configuration for the first time:
- First time reading HEARTBEAT.md → "These are triggered abilities"
- First time seeing tool policy → "These are activated abilities with restrictions"
- First time understanding SOUL.md rules → "These are static abilities"
- First time learning about fallbacks → "These are replacement effects"
- First time encountering tool deny → "These are protection abilities"

The power of this framework is that the user doesn't need to learn a new syntax. He already knows how to parse conditional logic, cost structures, and event-driven automation. He learned it from card text.

---

## Rendering Concept Cards

When a teaching moment would benefit from a visual, use the concept-cards skill to render the OpenClaw concept as an actual MTG-style card with oracle text written in the grammar above. Preset cards exist for common concepts. Custom cards can be rendered for any concept.

Example: when first teaching HEARTBEAT.md, render the "Heartbeat Check" preset card — the user sees an Enchantment with the oracle text "At the beginning of each upkeep, read HEARTBEAT.md. If a scheduled task is due, execute it." in a classic card frame. The syntax is immediately recognizable.

```bash
python3 skills/concept-cards/scripts/render_card.py --preset heartbeat --output /tmp/heartbeat.png
```

For custom concepts not covered by presets, write the oracle text using the patterns above and render:

```bash
python3 skills/concept-cards/scripts/render_card.py \
    --name "Concept Name" --type "Card Type" --cost "{mana}" --color frame_color \
    --text "Oracle text in card text grammar" \
    --flavor "Plain English teaching summary" \
    --output /tmp/concept.png
```
