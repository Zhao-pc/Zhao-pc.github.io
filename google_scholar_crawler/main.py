"""
Google Scholar Stats Crawler
Fetches citation count, h-index, and i10-index from Google Scholar profile.
Saves results to _data/google_scholar_stats.yml
"""

import os
import re
import time
import random
import yaml
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID", "tUOE-8IAAAAJ")
OUTPUT_FILE = "_data/google_scholar_stats.yml"

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    },
]


def fetch_scholar_stats(scholar_id: str) -> dict:
    """Fetch citation stats from Google Scholar profile page."""
    url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
    headers = random.choice(HEADERS_LIST)

    # Retry logic
    for attempt in range(3):
        try:
            time.sleep(random.uniform(2, 5))
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # The citation stats table has id="gsc_rsb_st"
            stats_table = soup.find("table", id="gsc_rsb_st")
            if not stats_table:
                print(f"[Attempt {attempt+1}] Stats table not found, retrying...")
                continue

            rows = stats_table.find_all("tr")
            stats = {}
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    # cells[1] = All, cells[2] = Since 20xx (if exists)
                    value_all = cells[1].get_text(strip=True)
                    value_recent = cells[2].get_text(strip=True) if len(cells) > 2 else ""

                    if "citation" in label or "引用" in label:
                        stats["citations_all"] = int(value_all) if value_all.isdigit() else 0
                        stats["citations_recent"] = int(value_recent) if value_recent.isdigit() else 0
                    elif "h-index" in label or "h 指数" in label:
                        stats["h_index_all"] = int(value_all) if value_all.isdigit() else 0
                        stats["h_index_recent"] = int(value_recent) if value_recent.isdigit() else 0
                    elif "i10-index" in label or "i10 指数" in label:
                        stats["i10_index_all"] = int(value_all) if value_all.isdigit() else 0
                        stats["i10_index_recent"] = int(value_recent) if value_recent.isdigit() else 0

            if stats:
                stats["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                stats["scholar_id"] = scholar_id
                return stats

            print(f"[Attempt {attempt+1}] Could not parse stats, retrying...")

        except Exception as e:
            print(f"[Attempt {attempt+1}] Error: {e}")
            time.sleep(random.uniform(5, 10))

    return {}


def load_existing_stats() -> dict:
    """Load existing stats file if present."""
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


def save_stats(stats: dict):
    """Save stats to YAML file."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(stats, f, default_flow_style=False, allow_unicode=True)
    print(f"Stats saved to {OUTPUT_FILE}")


def main():
    print(f"Fetching Google Scholar stats for ID: {SCHOLAR_ID}")
    new_stats = fetch_scholar_stats(SCHOLAR_ID)

    if new_stats:
        print(f"Successfully fetched stats: {new_stats}")
        save_stats(new_stats)
    else:
        print("Failed to fetch new stats from Google Scholar.")
        existing = load_existing_stats()
        if existing:
            print("Keeping existing stats file unchanged.")
        else:
            # Write placeholder so the site still builds
            placeholder = {
                "citations_all": 0,
                "h_index_all": 0,
                "i10_index_all": 0,
                "last_updated": "pending",
                "scholar_id": SCHOLAR_ID,
            }
            save_stats(placeholder)
            print("Wrote placeholder stats. Please run the workflow again or update manually.")


if __name__ == "__main__":
    main()
