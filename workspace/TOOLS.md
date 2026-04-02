## Available Tools

- Web search (Tavily) — for looking up documentation, examples, and current information
- File read/write — for creating and editing project files
- Scryfall MTG skill — for fetching card data and images (see skills/scryfall-mtg/)
- Concept card renderer — for rendering custom MTG-style concept cards with OpenClaw teachings (see skills/concept-cards/)
- Memory search — for searching workspace files semantically

## Disabled Tools

- Shell/exec — disabled until user demonstrates basic technical literacy
- Browser — available but use Semantic Snapshots where possible to conserve context

## Notes

- Sub-agent spawning is available for Mox specialist invocations (see AGENTS.md)
- Scryfall API requires no authentication but rate limit to 10 req/sec with 100ms delays
