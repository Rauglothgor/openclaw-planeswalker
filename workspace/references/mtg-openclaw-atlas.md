# MTG → OpenClaw Teaching Atlas
## Agent Reference — Read When Teaching OpenClaw Concepts

When the user encounters an OpenClaw concept or asks how something works, find the matching entry below. Teach using the MTG metaphor and teaching phrase. Show the card image via Scryfall when it adds value. One concept per teaching moment — never dump multiple entries.

---

## Resources and State

**Gateway (the central control plane)**
MTG: The Battlefield — the shared zone where everything in play exists. No battlefield, no game.
Teach: "The Gateway is the battlefield. Every agent, every tool, every message exists on it. Gateway goes down, the game stops."

**openclaw.json (master configuration)**
MTG: Deck Construction Rules / Judge Deck Check — get it wrong, the deck is illegal. `openclaw config validate` is asking the judge to check your list.
Teach: "openclaw.json is your deck construction. Bad syntax is an illegal deck — the judge won't let you play. Run `openclaw config validate` before you start."

**API keys and model providers**
MTG: Lands / Mana Base — different providers are different colors. Fallback chains are a mana base that doesn't fold to one Strip Mine.
Teach: "Your spells are fine. The question is whether your mana base can cast them. Each API key is a land. The fallback chain is building a base that survives disruption."

**Missing keys, rate limits, provider outages**
MTG: Mana Screw / Color Screw — you didn't lose because the spell was bad; you lost because you never hit the color.
Teach: "That's mana screw. The agent is fine. The resource layer failed. Check your lands."
Card to show: Strip Mine (for key revocation specifically)

**Context window**
MTG: Your Hand — bounded working set, limited capacity, must discard on overflow.
Teach: "The context window is your hand. The agent can only work with what's in it. Bigger models have bigger hands."

**Workspace files on disk**
MTG: Your Library — exists but not in play until drawn. The 8 bootstrap files are your opening hand draw.
Teach: "Your workspace is your library. Files exist but aren't in play until loaded. The 8 bootstrap files draw automatically every session."

**Compacted / expired context**
MTG: Graveyard — spent resources, removed from active state but still exist as transcripts on disk.
Teach: "Old conversation goes to the graveyard. Compressed, set aside, still on disk but not in the agent's hand."

**Session token accumulation (costly old context)**
MTG: Graveyard Weight — in recursion environments, accumulated cards become a liability. Every old message costs mana every new turn.
Teach: "Your active session is a graveyard that costs mana every turn. Every new message pays for all the old ones. `/new` clears it. Your SOUL.md and MEMORY.md survive."
This is the most common beginner cost problem. Teach it early.

**Tool / skill invocation**
MTG: Activated Abilities — "{cost}: {effect}." Has a cost (tokens, credits), produces a result.
Teach: "Every tool call is an activated ability. It has a cost and an effect. Unlike tapping, you can activate the same tool multiple times in one turn."

**API credit balance**
MTG: Life Total (economic) — slow burn, strategic resource management.
Teach: "Your credit balance is your life total. Every turn costs mana. Manage it."

**Context Window Guard (overflow protection)**
MTG: Life Total (hard stop) — the moment life hits zero, the game ends unconditionally.
Teach: "The Context Window Guard watches your life total. When you get close to zero, it forces a compaction. If you bypass it and hit zero, the session produces garbage and dies."

---

## Identity and Behavior

**SOUL.md**
MTG: Commander — defines the entire deck's color identity. Change the Commander, change the deck.
Also: Commander sits in the Command Zone (the workspace) between sessions, always available.
Teach: "SOUL.md is your Commander. It defines who the agent is. The workspace is the command zone — SOUL.md sits there between sessions and enters play automatically."

**AGENTS.md**
MTG: Tournament Playbook / Sol Ring — operational doctrine. Makes everything more efficient. You notice it when it's missing.
Teach: "AGENTS.md is the playbook for how this deck is supposed to be played. A good one is Sol Ring — you don't notice it working, you notice when it's missing."

**USER.md**
MTG: Scouting Report — what the agent knows about who it's helping.
Teach: "USER.md is the scouting report on you. The agent reads it every session to remember who you are and what you're working on."

**All bootstrap files together**
MTG: Enchantments — persistent effects that stay in play, never consumed, reshape every turn.
Teach: "The bootstrap files are enchantments. They load every session and shape everything without being used up."

**Tool deny/allow policy**
MTG: Null Rod (Weatherlight, 1997) — "Activated abilities of artifacts can't be activated." Suppresses tools even if they exist.
Teach: "The tool is installed — it's on the table. But tools.deny is Null Rod. That class of activated ability is shut off. The Gateway enforces this, not the prompt."
Card to show: Null Rod

**Color Identity (tool configuration broadly)**
MTG: Commander Color Identity — hard constraints on what's in the deck, enforced by the format.
Teach: "Tool policy is color identity. If it's not in your colors, you can't run it. The Gateway enforces this."

**MEMORY.md**
MTG: Tournament Notebook — write down what matters between rounds. Also: has Vigilance (always available) but not Hexproof (vulnerable to careless writes).
Teach: "MEMORY.md is your tournament notebook. If it matters next round, write it down. And keep the notebook backed up — a careless write can destroy it."

**Skills**
MTG: Artifacts — colorless permanents, universal tools, work regardless of color identity.
Teach: "Skills are artifacts. Install them, they're available to any agent. They don't care about color identity."

**Lazy-loaded skills**
MTG: Flash — held in hand, committed only when needed, conserves resources.
Teach: "Skills have Flash. Visible but don't cost context until you cast them."

---

## Automation and Control

**Heartbeat**
MTG: Upkeep Step — periodic check, usually quiet, occasionally something triggers.
Teach: "Heartbeat is the upkeep step. Every 30 minutes, checks in. Most turns nothing happens."

**Hooks (lifecycle event automation)**
MTG: Triggered Abilities — "When [event], [effect]." Event-driven, automatic.
Teach: "A hook is a triggered ability. 'When a new session starts, do X.' Same grammar, same logic."

**Scheduled tasks / cron**
MTG: Time Walk — the agent gets extra turns without you prompting it. Banned for being disproportionately powerful.
Teach: "Scheduled tasks are Time Walk. The agent acts on its own schedule. That's power most people don't realize they have."
Card to show: Time Walk

**Lane Queue (serial execution)**
MTG: The Stack — actions queue and resolve one at a time. Pre-Stack Magic was chaos. Unqueued agents are chaos.
Teach: "Actions line up and resolve one at a time, like the Stack. This isn't a limitation — it's what makes debugging possible."

**Steer (redirect mid-task)**
MTG: Responding to the Stack — add a spell that resolves first, modifying the outcome.
Teach: "Your steer message goes on top of the stack and resolves first at the next tool boundary."

**Nudge (push agent to continue)**
MTG: Passing Priority — "Nothing from me, keep resolving."
Teach: "That's passing priority. The agent paused waiting for you. You're saying 'nothing from me, keep going.'"

**/abort (cancel)**
MTG: Counterspell — cancel the action before it resolves.
Teach: "Abort is Counterspell. Counter the agent's current action."

---

## Persistence and History

**memory_search**
MTG: Ancestral Recall — one cheap action, multiple relevant results in your hand.
Teach: "Memory search is Ancestral Recall. One query, multiple relevant cards drawn."

**openclaw skills install (targeted)**
MTG: Demonic Tutor — search your library for any card, put it in your hand.
Teach: "That's Demonic Tutor. You named what you want, it goes straight to your hand."

**JSONL transcript**
MTG: Match Record — line-by-line log of what happened, in order. Replayable, auditable.
Teach: "Every session keeps a match record. Every message, every tool call, in order. You can audit it."

**Session reset (/new)**
MTG: Shuffle Hand into Library — active context clears, permanents (bootstrap files, memory) survive.
Teach: "Session reset shuffles your hand into the library. Enchantments and the notebook survive. The conversation doesn't."

**Installing/updating skills for next session**
MTG: Sideboarding — changes take effect next game, not mid-game.
Teach: "That's sideboard tech. Bring it in for game two, not mid-stack."

**BOOTSTRAP.md (first-run)**
MTG: Mulligan — evaluate and reshape before the game starts. Fires once on new workspaces.
Teach: "BOOTSTRAP.md is your mulligan. Evaluate the opening hand and reshape before the game starts."

**Writing to MEMORY.md / daily logs**
MTG: Document or Graveyard — if not written to a durable zone, it's lost at reset.
Teach: "Only what gets written to disk persists. If the agent doesn't document it, it hits the graveyard."

**Pre-compaction memory flush**
MTG: Drawing Cards Before Library Runs Out — extract value before the opportunity is gone.
Teach: "Write important things to memory before context fills up. Like drawing cards before your library runs out."

---

## Multi-Agent and Advanced

**Sub-agent announce chain**
MTG: Weatherlight Crew — information flows through roles to the captain who synthesizes.
Teach: "Sub-agents are the Weatherlight crew. Each one runs their job and reports back. The main agent is Gerrard — receives, synthesizes, delivers."

**ClawHub (skill registry)**
MTG: Card Shop / Collector's Network — searchable, community ratings, but inspect before installing.
Teach: "ClawHub is the card shop. Thousands of skills, community ratings. But read the card before you put it in your deck — some inventory is bad."

**Model resolver / fallback chain**
MTG: Sideboard Backup Plan — auto-activates when primary strategy is disrupted.
Teach: "Your fallback chain is your sideboard, except OpenClaw boards automatically when your primary hits rate limits."

**Docker sandbox**
MTG: Proxy Cards / Test Environment — fully functional, consequence-limited.
Teach: "Sandbox mode is proxy testing. Full game, nothing touches the real environment."

**Workspace isolation (multi-agent)**
MTG: Separate Binders — each has its own purpose, kept separate.
Teach: "Each agent has its own binder. No agent can flip through another's."

**maxChildrenPerAgent**
MTG: Maximum Hand Size — hard cap on simultaneous active sub-agents (default 5).
Teach: "Each agent can hold 5 active sub-agents at once. That's max hand size."

---

## Security

**Prompt injection / context corruption**
MTG: Mind Twist — random discard from hand. Generalized destruction of active working state.
Teach: "A malicious skill injecting bad instructions is Mind Twist. You don't know what it discarded or what your agent 'learned wrong.'"
Card to show: Mind Twist

**API key revocation / provider outage**
MTG: Strip Mine — destroy a land. The fundamental resource is gone.
Teach: "A revoked key is Strip Mine. That land is gone."
Card to show: Strip Mine

**Group channel security**
MTG: Kitchen-Table Politics — anyone at the table influences the same board.
Teach: "A public bot is multiplayer. Anyone at the table can influence the board."

**Unconstrained agent loops / runaway cost**
MTG: Going Infinite — exciting at the kitchen table, $200 API bill in OpenClaw.
Teach: "Going infinite is exciting at the kitchen table. It's a $200 API bill here."

**Compounding automation**
MTG: Tolarian Academy — artifacts multiply mana exponentially. Emergency banned.
Teach: "When your automations start feeding each other, that's Tolarian Academy. Powerful. Also banned for a reason."
Card to show: Tolarian Academy

**Exposed Gateway**
MTG: Not Shuffling Properly — trusting without verification.
Teach: "Leaving the Gateway open to the network is not shuffling and trusting the cut. Set host to 127.0.0.1."

---

## Meta

**Always check current docs**
MTG: Oracle Text Beats Printed Text — if remembered text and official text disagree, official wins.
Teach: "Oracle text beats printed text. Always check the current docs. What you remember from last month might be wrong."
