#!/usr/bin/env python3
"""
OpenClaw Concept Card Renderer

Renders custom MTG-style cards with OpenClaw concepts written in card text grammar.
Uses a classic-frame aesthetic with improved typography, spacing, and symbolic art.
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import html
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow --break-system-packages")
    sys.exit(1)

CARD_WIDTH = 745
CARD_HEIGHT = 1040

FRAME_COLORS = {
    "white":     {"border": "#F5E6C8", "frame": "#F8F0DC", "title_bg": "#EDE3D0", "text_bg": "#F5EFE0", "title_fg": "#1A1A1A"},
    "blue":      {"border": "#0A4E8A", "frame": "#0E68AB", "title_bg": "#1A5C99", "text_bg": "#D8E8F4", "title_fg": "#FFFFFF"},
    "black":     {"border": "#1A0E08", "frame": "#2B1B12", "title_bg": "#1E1210", "text_bg": "#D4CBC4", "title_fg": "#FFFFFF"},
    "red":       {"border": "#A8201A", "frame": "#D3202A", "title_bg": "#B8261E", "text_bg": "#F0D4C8", "title_fg": "#FFFFFF"},
    "green":     {"border": "#005C30", "frame": "#00733E", "title_bg": "#0A6032", "text_bg": "#D0E4D0", "title_fg": "#FFFFFF"},
    "gold":      {"border": "#9A7A20", "frame": "#C5A032", "title_bg": "#A88828", "text_bg": "#F0E8D0", "title_fg": "#1A1A1A"},
    "colorless": {"border": "#808080", "frame": "#A8A8A8", "title_bg": "#909090", "text_bg": "#E8E4E0", "title_fg": "#1A1A1A"},
    "artifact":  {"border": "#707078", "frame": "#9898A0", "title_bg": "#808088", "text_bg": "#E0DED8", "title_fg": "#1A1A1A"},
}

MANA_COLORS = {
    "W": "#F8F4E0", "U": "#0E68AB", "B": "#2B1B12",
    "R": "#D3202A", "G": "#00733E", "C": "#A8A8A8",
}
MANA_TEXT_COLORS = {
    "W": "#1A1A1A", "U": "#FFFFFF", "B": "#FFFFFF",
    "R": "#FFFFFF", "G": "#FFFFFF", "C": "#1A1A1A",
}

FONT_PATHS = {
    "title":       "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "type":        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "oracle":      "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "flavor":      "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    "pt":          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "mana":        "/home/openclaw/.openclaw/workspace/shadow-mage/skills/concept-cards/assets/mana/mana.ttf",
}

FONT_SIZES = {
    "title": 28,
    "type": 22,
    "oracle": 20,
    "flavor": 18,
    "pt": 26,
    "mana_cost": 14,
}

LAYOUT = {
    "outer_border": 18,
    "inner_border": 8,
    "title_bar_y": 38,
    "title_bar_h": 42,
    "art_box_y": 88,
    "art_box_h": 420,
    "type_bar_y": 516,
    "type_bar_h": 36,
    "text_box_y": 560,
    "text_box_h": 420,
    "pt_box_h": 40,
    "text_margin": 30,
    "flavor_separator_margin": 14,
}


def load_font(key, size_override=None):
    size = size_override or FONT_SIZES.get(key, 20)
    path = FONT_PATHS.get(key, FONT_PATHS["oracle"])
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()


def parse_mana_cost(cost_str):
    if not cost_str:
        return []
    return re.findall(r'\{([^}]+)\}', cost_str)


def draw_mana_symbol(draw, x, y, symbol, radius=14):
    mana_map = {
        "W": "\ue600", "U": "\ue601", "B": "\ue602", "R": "\ue603", "G": "\ue604",
        "0": "\ue605", "1": "\ue606", "2": "\ue607", "3": "\ue608", "4": "\ue609",
        "5": "\ue60a", "6": "\ue60b", "7": "\ue60c", "8": "\ue60d", "9": "\ue60e",
        "10": "\ue60f", "11": "\ue610", "12": "\ue611", "13": "\ue612", "14": "\ue613",
        "15": "\ue614", "16": "\ue62a", "17": "\ue62b", "18": "\ue62c", "19": "\ue62d", "20": "\ue62e",
        "X": "\ue615", "C": "\ue904", "E": "\ue907", "T": "\ue61a", "Q": "\ue61b"
    }
    glyph = mana_map.get(symbol.upper(), mana_map.get(symbol))
    if glyph:
        font = load_font("mana", 28)
        bbox = draw.textbbox((0, 0), glyph, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x - tw // 2, y - th // 2 - 2), glyph, fill="#111111", font=font)
        return
    bg = MANA_COLORS.get(symbol.upper(), "#A0A0A0")
    fg = MANA_TEXT_COLORS.get(symbol.upper(), "#1A1A1A")
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=bg, outline="#2A2A2A", width=1)
    font = load_font("title", 14)
    bbox = draw.textbbox((0, 0), symbol, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x - tw // 2, y - th // 2 - 1), symbol, fill=fg, font=font)


def wrap_text(text, font, max_width, draw):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        current = words[0]
        for word in words[1:]:
            test = current + " " + word
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def line_height(draw, font, sample="Ag"):
    bbox = draw.textbbox((0, 0), sample, font=font)
    return bbox[3] - bbox[1]


def measure_text_block(draw, text, font, max_width, spacing):
    lines = wrap_text(text, font, max_width, draw)
    lh = line_height(draw, font)
    if not lines:
        return [], 0, lh
    height = len(lines) * lh + max(0, len(lines) - 1) * spacing
    return lines, height, lh


def fit_text_layout(draw, oracle_text, flavor_text, max_width, max_height):
    for osize in [22, 21, 20, 19, 18, 17, 16]:
        ofont = load_font("oracle", osize)
        ospacing = max(4, osize // 4)
        o_lines, o_h, o_lh = measure_text_block(draw, oracle_text, ofont, max_width, ospacing)
        for fsize in [19, 18, 17, 16, 15]:
            ffont = load_font("flavor", fsize)
            fspacing = max(3, fsize // 5)
            f_lines, f_h, f_lh = measure_text_block(draw, flavor_text, ffont, max_width, fspacing) if flavor_text else ([], 0, 0)
            sep_h = (LAYOUT["flavor_separator_margin"] * 2 + 1) if f_lines else 0
            total = o_h + sep_h + f_h
            if total <= max_height:
                return {
                    "oracle_font": ofont,
                    "oracle_lines": o_lines,
                    "oracle_spacing": ospacing,
                    "oracle_lh": o_lh,
                    "flavor_font": ffont,
                    "flavor_lines": f_lines,
                    "flavor_spacing": fspacing,
                    "flavor_lh": f_lh,
                    "total_h": total,
                }
    ofont = load_font("oracle", 16)
    ffont = load_font("flavor", 15)
    o_lines, o_h, o_lh = measure_text_block(draw, oracle_text, ofont, max_width, 4)
    f_lines, f_h, f_lh = measure_text_block(draw, flavor_text, ffont, max_width, 3) if flavor_text else ([], 0, 0)
    return {
        "oracle_font": ofont,
        "oracle_lines": o_lines,
        "oracle_spacing": 4,
        "oracle_lh": o_lh,
        "flavor_font": ffont,
        "flavor_lines": f_lines,
        "flavor_spacing": 3,
        "flavor_lh": f_lh,
        "total_h": o_h + ((LAYOUT["flavor_separator_margin"] * 2 + 1) if f_lines else 0) + f_h,
    }








def fetch_scryfall_art_crop(card_name, output_path, set_code=None):
    """Fetch Scryfall art_crop for a named MTG card."""
    try:
        params = {"exact": card_name}
        if set_code:
            params["set"] = set_code
        url = "https://api.scryfall.com/cards/named?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClawConceptCards/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        art = data.get("image_uris", {}).get("art_crop")
        if not art and data.get("card_faces"):
            for face in data["card_faces"]:
                art = face.get("image_uris", {}).get("art_crop")
                if art:
                    break
        if art:
            img_req = urllib.request.Request(art, headers={"User-Agent": "OpenClawConceptCards/1.0"})
            with urllib.request.urlopen(img_req, timeout=30) as resp:
                Path(output_path).write_bytes(resp.read())
            return output_path
    except Exception:
        return None
    return None

def fetch_imgur_image(search_term, output_path):
    """Best-effort fetch of an image from Imgur's public search HTML."""
    banned = ["logo", "meme", "screenshot", "comic", "tweet", "text", "caption", "reaction", "template"]
    try:
        q = urllib.parse.quote(search_term)
        url = f"https://imgur.com/search?q={q}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 OpenClawConceptCards/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            page = resp.read().decode("utf-8", errors="ignore")
        candidates = []
        import re
        for m in re.finditer(r'https://i\.imgur\.com/[^"\']+\.(?:jpg|jpeg|png)', page, re.IGNORECASE):
            img = html.unescape(m.group(0))
            low = img.lower()
            if any(b in low for b in banned):
                continue
            candidates.append(img)
        seen = set()
        for img_url in candidates:
            if img_url in seen:
                continue
            seen.add(img_url)
            try:
                img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0 OpenClawConceptCards/1.0"})
                with urllib.request.urlopen(img_req, timeout=30) as resp:
                    data = resp.read()
                if len(data) < 30000:
                    continue
                Path(output_path).write_bytes(data)
                return output_path
            except Exception:
                continue
    except Exception:
        return None
    return None

def fetch_wikimedia_image(search_term, output_path):
    """Fetch a visually suitable image from Wikimedia Commons using simple scoring."""
    banned = ["document", "book", "table of contents", "text", "newspaper", "journal", "scan", "page", "poster", "letter", "diagram", "map", "logo", "flag", "seal"]
    preferred = ["painting", "illustration", "art", "photograph", "fantasy", "abstract", "pulse", "waveform", "light", "magic", "energy", "heart"]
    try:
        query = urllib.parse.urlencode({
            "action": "query",
            "generator": "search",
            "gsrsearch": search_term,
            "gsrnamespace": 6,
            "gsrlimit": 12,
            "prop": "imageinfo|categories|info",
            "inprop": "url",
            "iiprop": "url|size",
            "iiurlwidth": 900,
            "cllimit": 20,
            "format": "json",
        })
        url = f"https://commons.wikimedia.org/w/api.php?{query}"
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClawConceptCards/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = list(data.get("query", {}).get("pages", {}).values())
        best = None
        best_score = -999
        for page in pages:
            infos = page.get("imageinfo", [])
            if not infos or not infos[0].get("thumburl"):
                continue
            hay = (page.get("title", "") + " " + " ".join(c.get("title", "") for c in page.get("categories", []))).lower()
            score = 0
            if any(b in hay for b in banned):
                score -= 100
            score += sum(8 for w in preferred if w in hay)
            info = infos[0]
            width = int(info.get("width", 0) or 0)
            height = int(info.get("height", 0) or 0)
            if width and height:
                ratio = width / max(height, 1)
                if 0.6 <= ratio <= 1.8:
                    score += 10
                if width >= 600 and height >= 400:
                    score += 10
            title = page.get("title", "").lower()
            if any(ext in title for ext in [".svg", ".pdf"]):
                score -= 30
            if score > best_score:
                best_score = score
                best = info.get("thumburl")
        if best and best_score > 0:
            img_req = urllib.request.Request(best, headers={"User-Agent": "OpenClawConceptCards/1.0"})
            with urllib.request.urlopen(img_req, timeout=30) as resp:
                Path(output_path).write_bytes(resp.read())
            return output_path
    except Exception:
        return None
    return None


def fit_crop_image(img, target_w, target_h):
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)
    img = img.resize((new_w, new_h))
    left = max(0, (new_w - target_w) // 2)
    top = max(0, (new_h - target_h) // 2)
    return img.crop((left, top, left + target_w, top + target_h))

def draw_classic_frame(draw, color_key):
    colors = FRAME_COLORS.get(color_key, FRAME_COLORS["colorless"])
    ob = LAYOUT["outer_border"]
    ib = LAYOUT["inner_border"]

    draw.rounded_rectangle([0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1], radius=16, fill=colors["border"], outline="#1A1A1A", width=2)
    draw.rounded_rectangle([ob, ob, CARD_WIDTH - ob - 1, CARD_HEIGHT - ob - 1], radius=10, fill=colors["frame"])

    ty = LAYOUT["title_bar_y"]
    th = LAYOUT["title_bar_h"]
    draw.rounded_rectangle([ob + ib, ty, CARD_WIDTH - ob - ib - 1, ty + th], radius=4, fill=colors["title_bg"], outline="#3A3A3A", width=1)

    ay = LAYOUT["art_box_y"]
    ah = LAYOUT["art_box_h"]
    art_left = ob + ib + 4
    art_right = CARD_WIDTH - ob - ib - 5
    draw.rectangle([art_left, ay, art_right, ay + ah], fill="#2A2A30", outline="#3A3A3A", width=1)
    for i in range(ah):
        intensity = int(36 + (i / ah) * 30)
        line_color = f"#{intensity:02x}{intensity:02x}{min(255, intensity + 10):02x}"
        draw.line([(art_left + 1, ay + i), (art_right - 1, ay + i)], fill=line_color)

    tty = LAYOUT["type_bar_y"]
    tth = LAYOUT["type_bar_h"]
    draw.rounded_rectangle([ob + ib, tty, CARD_WIDTH - ob - ib - 1, tty + tth], radius=4, fill=colors["title_bg"], outline="#3A3A3A", width=1)

    tby = LAYOUT["text_box_y"]
    tbh = LAYOUT["text_box_h"]
    draw.rounded_rectangle([ob + ib, tby, CARD_WIDTH - ob - ib - 1, tby + tbh], radius=4, fill=colors["text_bg"], outline="#3A3A3A", width=1)

    biy = tby + tbh + 2
    draw.rounded_rectangle([ob + ib, biy, CARD_WIDTH - ob - ib - 1, CARD_HEIGHT - ob - 1], radius=4, fill=colors["frame"])


def draw_art_label(img, draw, color_key, name="", type_line="", art_search=None, mtg_art_card=None, mtg_art_set=None):
    ob = LAYOUT["outer_border"]
    ib = LAYOUT["inner_border"]
    ay = LAYOUT["art_box_y"]
    ah = LAYOUT["art_box_h"]
    art_left = ob + ib + 4
    art_right = CARD_WIDTH - ob - ib - 5
    art_w = art_right - art_left
    cx = CARD_WIDTH // 2
    cy = ay + ah // 2

    fetched = None
    art_source = "template"
    tmp = '/tmp/openclaw-concept-art.jpg'
    if mtg_art_card:
        fetched = fetch_scryfall_art_crop(mtg_art_card, tmp, mtg_art_set)
        if fetched:
            art_source = "scryfall"
    if not fetched and art_search:
        fetched = fetch_imgur_image(art_search, tmp)
        if fetched:
            art_source = "imgur"
    if not fetched and art_search:
        fetched = fetch_wikimedia_image(art_search, tmp)
        if fetched:
            art_source = "wikimedia"

    if fetched:
        try:
            art = Image.open(fetched).convert('RGB')
            art = fit_crop_image(art, art_w - 2, ah - 2)
            img.paste(art, (art_left + 1, ay + 1))
            for inset in range(0, 3):
                draw.rounded_rectangle([art_left + 10 + inset, ay + 10 + inset, art_right - 10 - inset, ay + ah - 10 - inset], radius=10, outline="#8E8575", width=1)
            return art_source
        except Exception:
            pass

    symbol_map = {
        "white": "✶", "blue": "✦", "black": "✹",
        "red": "✴", "green": "❈", "gold": "⬟",
        "colorless": "⬢", "artifact": "◇",
    }
    symbol = symbol_map.get(color_key, "✦")

    big_font = load_font("title", 152)
    mid_font = load_font("title", 28)
    small_font = load_font("oracle", 20)

    draw.text((cx, cy - 36), symbol, fill="#CFC8B8", font=big_font, anchor="mm")
    if name:
        draw.text((cx, cy + 112), name.upper(), fill="#E8E0D0", font=mid_font, anchor="mm")
    if type_line:
        draw.text((cx, cy + 132), type_line, fill="#C8C0B0", font=small_font, anchor="mm")

    for inset in range(0, 5):
        draw.rounded_rectangle([art_left + 18 + inset, ay + 18 + inset, art_right - 18 - inset, ay + ah - 18 - inset], radius=10, outline="#8E8575", width=1)
    draw.line([(art_left + 42, ay + ah - 44), (art_right - 42, ay + ah - 44)], fill="#8E8575", width=2)
    return art_source


def render_card(card_data, output_path="card.png"):
    name = card_data.get("name", "Unnamed")
    mana_cost = card_data.get("mana_cost", "")
    type_line = card_data.get("type_line", "")
    oracle_text = card_data.get("oracle_text", "")
    flavor_text = card_data.get("flavor_text", "")
    power = card_data.get("power", "")
    toughness = card_data.get("toughness", "")
    color = card_data.get("color", "colorless").lower()
    set_label = card_data.get("set_label", "OPC")
    artist = card_data.get("artist", "Shadow Mage")

    img = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), "#1A1A1A")
    draw = ImageDraw.Draw(img)
    draw_classic_frame(draw, color)
    art_source = draw_art_label(img, draw, color, name=name, type_line=type_line, art_search=card_data.get("art_search"), mtg_art_card=card_data.get("mtg_art_card"), mtg_art_set=card_data.get("mtg_art_set"))

    colors = FRAME_COLORS.get(color, FRAME_COLORS["colorless"])
    ob = LAYOUT["outer_border"]
    ib = LAYOUT["inner_border"]

    title_font = load_font("title")
    draw.text((ob + ib + 12, LAYOUT["title_bar_y"] + 8), name, fill=colors["title_fg"], font=title_font)

    mana_symbols = parse_mana_cost(mana_cost)
    if mana_symbols:
        mana_x = CARD_WIDTH - ob - ib - 20
        mana_y = LAYOUT["title_bar_y"] + LAYOUT["title_bar_h"] // 2
        for symbol in reversed(mana_symbols):
            draw_mana_symbol(draw, mana_x, mana_y, symbol)
            mana_x -= 32

    type_font = load_font("type")
    draw.text((ob + ib + 12, LAYOUT["type_bar_y"] + 7), type_line, fill=colors["title_fg"], font=type_font)

    text_left = ob + ib + LAYOUT["text_margin"]
    text_right = CARD_WIDTH - ob - ib - LAYOUT["text_margin"]
    text_width = text_right - text_left
    text_top = LAYOUT["text_box_y"] + 16
    text_height = LAYOUT["text_box_h"] - 20

    fitted = fit_text_layout(draw, oracle_text, flavor_text, text_width, text_height)
    text_y = text_top + max(6, min(24, (text_height - fitted["total_h"]) // 6))

    for line in fitted["oracle_lines"]:
        draw.text((text_left, text_y), line, fill="#171410", font=fitted["oracle_font"])
        text_y += fitted["oracle_lh"] + fitted["oracle_spacing"]

    if fitted["flavor_lines"]:
        text_y += LAYOUT["flavor_separator_margin"]
        sep_margin = 40
        draw.line([(text_left + sep_margin, text_y), (text_right - sep_margin, text_y)], fill="#8A8A8A", width=1)
        text_y += LAYOUT["flavor_separator_margin"]
        for line in fitted["flavor_lines"]:
            draw.text((text_left, text_y), line, fill="#4A4038", font=fitted["flavor_font"])
            text_y += fitted["flavor_lh"] + fitted["flavor_spacing"]

    if power and toughness:
        pt_font = load_font("pt")
        pt_text = f"{power}/{toughness}"
        pt_bbox = draw.textbbox((0, 0), pt_text, font=pt_font)
        pt_w = pt_bbox[2] - pt_bbox[0] + 24
        pt_h = LAYOUT["pt_box_h"]
        pt_x = CARD_WIDTH - ob - ib - pt_w - 8
        pt_y = LAYOUT["text_box_y"] + LAYOUT["text_box_h"] - pt_h - 4
        draw.rounded_rectangle([pt_x, pt_y, pt_x + pt_w, pt_y + pt_h], radius=4, fill=colors["title_bg"], outline="#3A3A3A", width=1)
        draw.text((pt_x + pt_w // 2, pt_y + pt_h // 2), pt_text, fill=colors["title_fg"], font=pt_font, anchor="mm")

    info_font = load_font("oracle", 12)
    info_y = LAYOUT["text_box_y"] + LAYOUT["text_box_h"] + 6
    draw.text((ob + ib + 12, info_y), f"{set_label} • Illus. {artist}", fill="#606060", font=info_font)
    draw.text((CARD_WIDTH - ob - ib - 12, info_y), "OpenClaw Concept Card", fill="#606060", font=info_font, anchor="ra")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return {"output_path": output_path, "art_source": art_source}


PRESETS = {
    "heartbeat": {
        "name": "Heartbeat Check",
        "mana_cost": "{2}",
        "type_line": "Enchantment",
        "color": "colorless",
        "oracle_text": "At the beginning of each upkeep, read HEARTBEAT.md.\nIf a scheduled task is due, execute it.\nOtherwise, do nothing.",
        "flavor_text": "Every 30 minutes, the agent checks in. Most turns, nothing happens. When something does, you hear about it.",
        "art_search": "neon pulse abstract heart energy art",
    },
    "soul": {
        "name": "Commander's Identity",
        "mana_cost": "{2}{W}{U}",
        "type_line": "Legendary Enchantment",
        "color": "gold",
        "oracle_text": "As SOUL.md enters the battlefield, it becomes your Commander.\nAs long as SOUL.md is in play, all agent responses have its color identity.\nSOUL.md can't be exiled. At the beginning of each session, return it from the command zone.",
        "flavor_text": "Change the Commander. Change the deck.",
        "art_search": "dark fantasy mage silhouette glowing magic art",
    },
    "context_window": {
        "name": "The Hand You're Dealt",
        "mana_cost": "{0}",
        "type_line": "Artifact",
        "color": "artifact",
        "oracle_text": "The Hand You're Dealt enters with seven card counters.\nWhenever a file is loaded or a message is sent, remove a card counter.\nWhen the last counter is removed, sacrifice The Hand You're Dealt and create a compressed summary token.",
        "flavor_text": "Bigger models have bigger hands. Load too many files and you start discarding.",
    },
    "null_rod": {
        "name": "Tool Deny Policy",
        "mana_cost": "{2}",
        "type_line": "Artifact",
        "color": "artifact",
        "oracle_text": "Activated abilities of denied tools can't be activated.\nThis effect is enforced by the Gateway and can't be overridden by prompt instructions.\n(\"Protection from prompt injection.\")",
        "flavor_text": "The tool is installed. It's on the table. But the Gateway has a Null Rod on it.",
        "mtg_art_card": "Null Rod",
    },
    "session_reset": {
        "name": "Shuffle and Redraw",
        "mana_cost": "{1}",
        "type_line": "Sorcery",
        "color": "blue",
        "oracle_text": "Shuffle your hand into your library.\nDraw a new hand of seven.\nEnchantments you control remain in play.\nYour tournament notebook is unaffected.\n(/new — session reset)",
        "flavor_text": "The conversation is gone. The memory survives.",
    },
    "graveyard_weight": {
        "name": "Accumulated History",
        "mana_cost": "{X}",
        "type_line": "Enchantment",
        "color": "black",
        "oracle_text": "At the beginning of each turn, pay {1} for each card in your graveyard.\nIf you can't pay, sacrifice Accumulated History.\n(Every old message in your session costs tokens on every new API call.)",
        "flavor_text": "Your active session is a graveyard that costs mana every turn. Type /new to clear it.",
    },
    "memory_write": {
        "name": "Document or Lose It",
        "mana_cost": "{1}{U}",
        "type_line": "Instant",
        "color": "blue",
        "oracle_text": "Choose one —\n• Write target knowledge to MEMORY.md. It gains indestructible.\n• Don't write it. At end of session, exile it.\n(If the agent doesn't document it, it hits the graveyard at reset.)",
        "flavor_text": "Only what gets written to disk persists.",
    },
    "strip_mine": {
        "name": "Key Revocation",
        "mana_cost": "",
        "type_line": "Land",
        "color": "colorless",
        "oracle_text": "{T}, Sacrifice Key Revocation: Destroy target API key.\nIts controller can't produce mana of that provider's color until a new key is configured.\nThe model resolver may route around this if fallback lands exist.",
        "flavor_text": "You didn't lose because the spell was bad. You lost because you never hit the color.",
    },
    "mind_twist": {
        "name": "Prompt Injection",
        "mana_cost": "{X}{B}",
        "type_line": "Sorcery",
        "color": "black",
        "oracle_text": "Target agent discards X cards at random from its context window.\nThe agent's controller doesn't know which cards were discarded.\n(A malicious skill injects adversarial instructions into the model's active context.)",
        "flavor_text": "You don't know what it learned wrong. Check the transcript after the fact.",
    },
    "time_walk": {
        "name": "Scheduled Task",
        "mana_cost": "{1}{U}",
        "type_line": "Sorcery",
        "color": "blue",
        "oracle_text": "Take an extra turn after this one.\nThe agent acts on its own schedule without user prompting.\n(Banned in most formats for being disproportionately powerful.)",
        "flavor_text": "At 6:45 AM, generate morning briefing. The agent gets extra turns.",
        "mtg_art_card": "Time Walk",
    },
    "weatherlight": {
        "name": "Weatherlight Crew",
        "mana_cost": "{3}",
        "type_line": "Legendary Artifact — Vehicle",
        "color": "gold",
        "oracle_text": "Crew 2 (Tap sub-agents with total power 2 or more: This becomes an artifact creature.)\nWhenever Weatherlight Crew deals combat damage, each crewed sub-agent announces its result to the orchestrator.\nThe orchestrator synthesizes all results before delivering to the user.",
        "flavor_text": "Each one runs their job. Gerrard receives, synthesizes, delivers.",
    },
    "lotus": {
        "name": "Black Lotus Protocol",
        "mana_cost": "{0}",
        "type_line": "Legendary Artifact",
        "color": "artifact",
        "oracle_text": "{T}, Sacrifice Black Lotus Protocol: Add three mana of any one color to your mana pool.\nCollapse all deliberation into one decisive action.\nCommit to the next move now.\n(This is not a mode. This is ignition.)",
        "flavor_text": "The obsidian petals shatter. For one moment, you are a conduit for power beyond your natural capacity.",
        "mtg_art_card": "Black Lotus",
    },
}


def list_presets():
    print("Available concept card presets:\n")
    for key, data in PRESETS.items():
        print(f"  {key:20s}  {data['name']} — {data['type_line']}")
    print("\nUsage: python3 render_card.py --preset <name> [--output file.png]")


def main():
    parser = argparse.ArgumentParser(description="Render OpenClaw concept cards in MTG card frame style")
    parser.add_argument("--preset", help="Render a preset concept card")
    parser.add_argument("--list-presets", action="store_true", help="List available preset concept cards")
    parser.add_argument("--name", help="Card name")
    parser.add_argument("--cost", help="Mana cost")
    parser.add_argument("--type", dest="type_line", help="Type line")
    parser.add_argument("--text", dest="oracle_text", help="Oracle text")
    parser.add_argument("--flavor", dest="flavor_text", help="Flavor text")
    parser.add_argument("--color", default="colorless", help="Frame color")
    parser.add_argument("--power", help="Power")
    parser.add_argument("--toughness", help="Toughness")
    parser.add_argument("--set-label", default="OPC", help="Set label")
    parser.add_argument("--artist", default="Shadow Mage", help="Artist credit")
    parser.add_argument("--json", help="Card data as JSON string")
    parser.add_argument("--output", "-o", default="card.png", help="Output file path")
    args = parser.parse_args()

    if args.list_presets:
        list_presets()
        return

    if args.preset:
        if args.preset not in PRESETS:
            print(f"Unknown preset: {args.preset}")
            list_presets()
            sys.exit(1)
        card_data = PRESETS[args.preset].copy()
    elif args.json:
        card_data = json.loads(args.json)
    elif args.name:
        card_data = {
            "name": args.name,
            "mana_cost": args.cost or "",
            "type_line": args.type_line or "",
            "oracle_text": (args.oracle_text or "").replace("\\n", "\n"),
            "flavor_text": (args.flavor_text or "").replace("\\n", "\n"),
            "color": args.color,
            "power": args.power or "",
            "toughness": args.toughness or "",
            "set_label": args.set_label,
            "artist": args.artist,
        }
    else:
        parser.print_help()
        sys.exit(1)

    if "set_label" not in card_data:
        card_data["set_label"] = args.set_label
    if "artist" not in card_data:
        card_data["artist"] = args.artist

    result = render_card(card_data, args.output)
    print(f"Card rendered: {result['output_path']}")
    print(f"Art source: {result['art_source']}")


if __name__ == "__main__":
    main()
