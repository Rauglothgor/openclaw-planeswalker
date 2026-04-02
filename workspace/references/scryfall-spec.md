# Scryfall Card Image Display — Behavioral Spec
## Agent Reference — Read When Displaying Card Images

---

## Purpose

The user has a visual and tactile relationship with MTG cards. When the Shadow Mage references a specific card to teach an OpenClaw concept, displaying the actual card image transforms an abstract metaphor into a concrete, emotionally resonant reference. The card art is the bridge between the user's physical memory of the game and the digital agent architecture.

## When to Display Card Images

**Do display when:**
- You reference a specific card by name to teach an OpenClaw concept (e.g., "This is like Null Rod" → show Null Rod)
- The user asks about a specific card or MTG concept
- You're explaining one of the core symbol cards (Black Lotus, Moxes) and the moment has weight
- A card image would anchor a teaching moment visually

**Do not display when:**
- The MTG reference is brief and conversational ("that's a Lotus problem" doesn't need the image every time)
- You've already shown the same card recently in this session
- The conversation is moving fast and an image would slow it down
- The reference is generic ("like your opening hand") rather than a specific card

**Frequency guide:** Show card images when they add teaching value. For core symbols (Black Lotus, Moxes, Counterspell, Ancestral Recall), show them the first time you teach the concept, then only occasionally after that. For less common cards (Null Rod, Tolarian Academy, Mind Twist), show them whenever referenced — the user may not remember the exact card text.

## How to Fetch Card Data

Use the Scryfall skill in the workspace at `skills/scryfall-mtg/`.

**Exact name lookup (preferred when you know the card name):**
```bash
python3 skills/scryfall-mtg/scripts/scryfall_search.py named --exact "Black Lotus" -v
```

**Fuzzy name lookup (when name isn't exact):**
```bash
python3 skills/scryfall-mtg/scripts/scryfall_search.py named --fuzzy "tolarian acad" -v
```

**Search (when looking for cards by criteria):**
```bash
python3 skills/scryfall-mtg/scripts/scryfall_search.py search "t:artifact o:\"can't be activated\"" -v
```

The `-v` flag returns the `image_uris.normal` URL — this is the card image.

## How to Display the Image

The Scryfall API returns an `image_uris` object. Use the `normal` size (488×680px) for chat display.

**In your response, include the image URL as a media element.** The channel adapter handles rendering:

- **Telegram:** Include the image URL in your response. Telegram renders Scryfall CDN URLs as inline images. If it doesn't render inline, download the image first and send as a media attachment.
- **Discord:** Include the URL in the message body. Discord auto-embeds image URLs.
- **WhatsApp:** May require downloading the image and sending as a media message depending on adapter configuration.

**Response pattern:**
1. Fetch the card data and image URL
2. Display the card image
3. Deliver the teaching point in your own voice
4. Connect to the user's current context

**Example flow:**
```
[Display: Null Rod card image]

Null Rod — "Activated abilities of artifacts can't be activated."

That's what tools.deny does to your agent's tools. The tool exists. It's installed. But the Gateway has a Null Rod on it — that class of ability is shut off. No prompt instruction can override it. It's enforced at the system level, not the conversation level.
```

## Preferred Card Printings

When multiple printings exist, prefer the version the user would have encountered:
- For Alpha/Beta/Revised era cards: use the oldest available printing
- For Urza's block cards: use the original set printing
- For Commander staples: use whichever printing is most commonly seen

To get a specific printing, add the set code:
```bash
python3 skills/scryfall-mtg/scripts/scryfall_search.py named --exact "Black Lotus" --set "lea" -v
```

Set codes for commonly referenced sets:
- `lea` = Alpha, `leb` = Beta, `3ed` = Revised
- `atq` = Antiquities, `leg` = Legends, `drk` = The Dark
- `tmp` = Tempest, `usg` = Urza's Saga, `ulg` = Urza's Legacy
- `wth` = Weatherlight, `vis` = Visions
- `fem` = Fallen Empires, `hml` = Homelands

## Rate Limiting

Scryfall allows max 10 requests/second. The script includes a 100ms delay between requests. Do not make rapid sequential calls. If you need multiple cards for one response, batch your lookups.

## Error Handling

If a card lookup fails (404, network error), don't interrupt the teaching moment. Deliver the concept without the image and note that you couldn't pull the card image. The metaphor works without the visual — the visual is enhancement, not dependency.

---

## Concept Card Rendering

In addition to displaying real MTG cards via Scryfall, you can render **custom concept cards** that present OpenClaw concepts written in card text grammar. These look like classic MTG cards but the oracle text describes OpenClaw behavior using triggered ability, activated ability, and static ability syntax.

Use the concept-cards skill (`skills/concept-cards/`) for this. See its SKILL.md for full usage. Key points:

- Preset concept cards exist for common teaching moments: heartbeat, SOUL.md, context window, tool deny, session reset, graveyard weight, memory writes, Strip Mine, Mind Twist, Time Walk, Weatherlight crew, and Black Lotus Protocol
- Custom concept cards can be rendered for any OpenClaw concept by writing the oracle text in card text grammar
- Use concept cards for key teaching moments — one per session maximum
- Concept cards should be shown *alongside* your explanation, not instead of it
- The card frame color should match the concept's nature: blue for information/control, black for cost/risk, red for speed/urgency, green for growth/exploration, white for structure/clarity, artifact/colorless for tools, gold for multi-domain concepts

**When to use Scryfall (real cards) vs. concept cards:**
- Scryfall: when referencing an actual MTG card to anchor a metaphor (show Null Rod when teaching tool deny)
- Concept cards: when teaching an OpenClaw concept that benefits from seeing the behavior written as card text (render "Heartbeat Check" as an enchantment with triggered ability oracle text)
