#!/usr/bin/env python3
import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


def build_url(image_url: str, api_key: str, gl: str, hl: str, safe: str, no_cache: bool) -> str:
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": api_key,
        "gl": gl,
        "hl": hl,
        "safe": safe,
    }
    if no_cache:
        params["no_cache"] = "true"
    return "https://serpapi.com/search?" + urllib.parse.urlencode(params)


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def iter_images(folder: Path):
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            yield path.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Reverse image search via SerpAPI (Google Reverse Image).")
    parser.add_argument("--dir", default="photos", help="Folder of images (default: photos)")
    parser.add_argument("--base-url", required=True, help="Public base URL where images are hosted, e.g. https://ramoti.com/photos/")
    parser.add_argument("--out", default="serpapi-matches.csv", help="Output CSV file")
    parser.add_argument("--env-var", default="SERPAPI_KEY", help="Env var for SerpAPI key")
    parser.add_argument("--max-results", type=int, default=5, help="Max matches to record per image")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to sleep between requests")
    parser.add_argument("--gl", default="us", help="Country code for Google results")
    parser.add_argument("--hl", default="en", help="Language code for Google results")
    parser.add_argument("--safe", default="active", help="SafeSearch: active/off")
    parser.add_argument("--no-cache", action="store_true", help="Force fresh results (no SerpAPI cache)")
    args = parser.parse_args()

    api_key = os.getenv(args.env_var)
    if not api_key:
        print(f"Missing API key. Set ${args.env_var}.", file=sys.stderr)
        return 1

    folder = Path(args.dir)
    if not folder.is_dir():
        print(f"Folder not found: {folder}", file=sys.stderr)
        return 1

    base = args.base_url.rstrip("/") + "/"

    out_path = Path(args.out)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename",
            "image_url",
            "result_rank",
            "result_title",
            "result_link",
            "result_source",
        ])

        for name in iter_images(folder):
            image_url = base + urllib.parse.quote(name)
            url = build_url(image_url, api_key, args.gl, args.hl, args.safe, args.no_cache)
            try:
                data = fetch_json(url)
            except Exception as exc:
                writer.writerow([name, image_url, "", f"ERROR: {exc}", "", ""])
                print(f"ERROR: {name}: {exc}")
                continue

            results = data.get("image_results") or []
            if not results:
                writer.writerow([name, image_url, "", "NO_RESULTS", "", ""])
                print(f"NO_RESULTS: {name}")
            else:
                for idx, item in enumerate(results[: args.max_results], start=1):
                    writer.writerow([
                        name,
                        image_url,
                        idx,
                        item.get("title", ""),
                        item.get("link", ""),
                        item.get("source", ""),
                    ])
                print(f"OK: {name} ({min(len(results), args.max_results)} results)")

            if args.sleep > 0:
                time.sleep(args.sleep)

    print(f"Done. Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
