#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"
ARCHIVE_PATH = ROOT / "archive.html"
TEMPLATE_PATH = ROOT / "reviews" / "template.html"
REVIEWS_DIR = ROOT / "reviews"
SITE_TITLE = "St. James’ Dispatch"

LATEST_START = "<!-- LATEST_REVIEW_START -->"
LATEST_END = "<!-- LATEST_REVIEW_END -->"
ARCHIVE_START = "<!-- ARCHIVE_LIST_START -->"
ARCHIVE_END = "<!-- ARCHIVE_LIST_END -->"


def _prompt(label: str, default: str | None = None) -> str:
    if default:
        value = input(f"{label} [{default}]: ").strip()
        return value or default
    return input(f"{label}: ").strip()


def _prompt_paragraphs() -> list[str]:
    print("Enter review paragraphs. Finish by typing END on its own line.")
    paras: list[str] = []
    current: list[str] = []
    while True:
        line = input().rstrip()
        if line == "END":
            if current:
                paras.append(" ".join(current).strip())
            break
        if line == "":
            if current:
                paras.append(" ".join(current).strip())
                current = []
            continue
        current.append(line)
    return [p for p in paras if p]


def _load_template() -> str:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Missing template: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def _write_review_page(values: dict) -> Path:
    slug = values["date_slug"]
    output_path = REVIEWS_DIR / f"{slug}.html"
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)

    template = _load_template()
    body_html = "\n            ".join([f"<p>{p}</p>" for p in values["paragraphs"]])
    template = template.replace("{{BODY_PARAGRAPHS}}", body_html)

    replacements = {
        "{{SITE_TITLE}}": SITE_TITLE,
        "{{MATCH_TITLE}}": values["match_title"],
        "{{EDITION}}": values["edition"],
        "{{COMPETITION}}": values["competition"],
        "{{VENUE}}": values["venue"],
        "{{DISPLAY_DATE}}": values["display_date"],
        "{{GOALSCORERS_HOME}}": values["goalscorers_home"],
        "{{GOALSCORERS_AWAY}}": values["goalscorers_away"],
        "{{PLAYER_OF_MATCH}}": values["player_of_match"],
        "{{PRINT_DATE}}": values["print_date"],
    }

    for key, value in replacements.items():
        template = template.replace(key, value)

    output_path.write_text(template, encoding="utf-8")
    return output_path


def _replace_block(text: str, start: str, end: str, new_block: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{new_block}\n{end}"
    if not pattern.search(text):
        raise ValueError(f"Missing marker block: {start} ... {end}")
    return pattern.sub(replacement, text)


def _update_index(values: dict) -> None:
    index = INDEX_PATH.read_text(encoding="utf-8")

    article_html = f"""<article id=\"latest\" class=\"mt-12\">
          <header class=\"space-y-4\">
            <p class=\"font-mono text-[11px] uppercase tracking-[0.4em]\">Edition {values['edition']} — {values['competition']} — {values['venue']}</p>
            <h2 class=\"text-4xl md:text-5xl font-extrabold leading-tight\">{values['match_title']}</h2>
            <p class=\"text-sm font-mono uppercase tracking-[0.2em]\">{values['display_date']}</p>
          </header>
          <div class=\"mt-8 space-y-6 text-lg leading-relaxed print-body\">
            {"".join([f"<p>{p}</p>" for p in values['paragraphs']])}
          </div>
          <div class=\"mt-10 space-y-6 text-sm font-mono uppercase tracking-[0.2em]\">
            <div class=\"space-y-2\">
              <p class=\"text-[10px] tracking-[0.35em] text-neutral-600 font-semibold\">Goalscorers</p>
              <p>{values['goalscorers_home']}</p>
              <p>{values['goalscorers_away']}</p>
            </div>
            <div class=\"space-y-2\">
              <p class=\"text-[10px] tracking-[0.35em] text-neutral-600 font-semibold\">Player of the Match</p>
              <p>{values['player_of_match']}</p>
            </div>
          </div>
        </article>"""

    index = _replace_block(index, LATEST_START, LATEST_END, article_html)

    index = re.sub(
        r"<title>.*?</title>",
        f"<title>{SITE_TITLE} — {values['match_title']}</title>",
        index,
        flags=re.DOTALL,
    )

    index = re.sub(
        r"<div class=\"hidden sm:block stamp\">Edition .*?</div>",
        f"<div class=\"hidden sm:block stamp\">Edition {values['edition']}</div>",
        index,
    )

    index = re.sub(
        r"St\. James’ Dispatch • Edition .*?</p>",
        f"{SITE_TITLE} • Edition {values['edition']}</p>",
        index,
    )

    index = re.sub(
        r"Printed in Newcastle • .*? • ISSN .*?</p>",
        f"Printed in Newcastle • {values['print_date']} • ISSN {values['edition']}-NUFC</p>",
        index,
    )

    INDEX_PATH.write_text(index, encoding="utf-8")


def _update_archive(values: dict) -> None:
    archive = ARCHIVE_PATH.read_text(encoding="utf-8")

    list_html = f"""<ul class=\"mt-4 space-y-3 text-sm leading-relaxed\">
                <li>
                  <span class=\"font-mono uppercase tracking-[0.2em]\">{values['display_date']}</span> —
                  <a class=\"hover:underline\" href=\"reviews/{values['date_slug']}.html\">{values['match_title']}</a>
                </li>
              </ul>"""

    archive = _replace_block(archive, ARCHIVE_START, ARCHIVE_END, list_html)
    ARCHIVE_PATH.write_text(archive, encoding="utf-8")


def main() -> None:
    today = _dt.date.today().strftime("%B %-d, %Y")

    edition = _prompt("Edition number (e.g., 01)")
    competition = _prompt("Competition (e.g., Premier League)")
    venue = _prompt("Venue (e.g., St James’ Park)")
    match_title = _prompt("Match title (e.g., Man City 3–1 Newcastle United)")
    display_date = _prompt("Display date (e.g., February 4, 2026)")
    date_slug = _prompt("Date slug (YYYY-MM-DD)")
    print_date = _prompt("Print date", today)
    goalscorers_home = _prompt("Goalscorers home line (e.g., Man City: ...)")
    goalscorers_away = _prompt("Goalscorers away line (e.g., Newcastle United: ...)")
    player_of_match = _prompt("Player of the Match")
    paragraphs = _prompt_paragraphs()

    if not paragraphs:
        raise SystemExit("No paragraphs entered.")

    values = {
        "edition": edition,
        "competition": competition,
        "venue": venue,
        "match_title": match_title,
        "display_date": display_date,
        "date_slug": date_slug,
        "print_date": print_date,
        "goalscorers_home": goalscorers_home,
        "goalscorers_away": goalscorers_away,
        "player_of_match": player_of_match,
        "paragraphs": paragraphs,
    }

    output_path = _write_review_page(values)
    _update_index(values)
    _update_archive(values)

    print(f"Created review: {output_path}")
    print("Updated index.html and archive.html")


if __name__ == "__main__":
    main()
