#!/usr/bin/env python3
"""Rank videos by viral score (velocity * engagement rate).

Accepts JSON from instagramcli, tiktokcli, or youtubecli via stdin.
Auto-detects platform, normalizes data, filters by freshness and views,
calculates viral score, returns top-K.

Usage:
    bin/instagramcli search reels -q "keyword" | python3 scripts/rank_videos.py --top-k 3
    bin/tiktokcli keyword search -q "keyword" --period 7 | python3 scripts/rank_videos.py --days 14
    bin/youtubecli search -q "keyword" | python3 scripts/rank_videos.py --min-views 100000

Environment:
    No API keys required — pure data processing.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone


def detect_and_extract(data):
    """Auto-detect platform from JSON structure and extract normalized video list."""
    videos = []

    # Instagram — instagramcli search reels
    if isinstance(data, dict) and "reels_serp_modules" in data:
        for module in data.get("reels_serp_modules", []):
            for clip in module.get("clips", []):
                media = clip.get("media", {})
                user = media.get("user", {})
                taken_at = media.get("taken_at", 0)
                code = media.get("code", "")
                videos.append({
                    "platform": "instagram",
                    "url": f"https://www.instagram.com/reel/{code}/" if code else "",
                    "username": user.get("username", "?"),
                    "views": media.get("play_count", 0),
                    "likes": media.get("like_count", 0),
                    "comments": media.get("comment_count", 0),
                    "posted_ts": taken_at,
                    "description": (media.get("caption", {}) or {}).get("text", "")[:150],
                })

    # Instagram — instagramcli hashtag clips (list of media objects)
    elif isinstance(data, list) and data and "pk" in data[0] and "code" in data[0]:
        for item in data:
            user = item.get("user", {})
            taken_at_str = item.get("taken_at", "")
            try:
                if isinstance(taken_at_str, str) and taken_at_str:
                    posted_ts = int(datetime.fromisoformat(taken_at_str.replace("Z", "+00:00")).timestamp())
                elif isinstance(taken_at_str, (int, float)):
                    posted_ts = int(taken_at_str)
                else:
                    posted_ts = 0
            except (ValueError, OSError):
                posted_ts = 0
            code = item.get("code", "")
            videos.append({
                "platform": "instagram",
                "url": f"https://www.instagram.com/reel/{code}/" if code else "",
                "username": user.get("username", "?"),
                "views": item.get("play_count", 0),
                "likes": item.get("like_count", 0),
                "comments": item.get("comment_count", 0),
                "posted_ts": posted_ts,
                "description": (item.get("caption_text", "") or "")[:150],
            })

    # TikTok — tiktokcli explore (itemList) / search (item_list) / other (data)
    elif isinstance(data, dict) and ("itemList" in data or "item_list" in data or "data" in data):
        items = data.get("itemList") or data.get("item_list") or data.get("data") or []
        for item in items:
            stats = item.get("statistics") or item.get("stats") or {}
            author = item.get("author", {})
            created = item.get("createTime", 0)
            try:
                posted_ts = int(created) if created else 0
            except (ValueError, TypeError):
                posted_ts = 0
            vid_id = item.get("id", "")
            username = author.get("uniqueId") or author.get("unique_id") or "?"
            videos.append({
                "platform": "tiktok",
                "url": f"https://www.tiktok.com/@{username}/video/{vid_id}" if vid_id else "",
                "username": username,
                "views": stats.get("playCount") or stats.get("play_count", 0),
                "likes": stats.get("diggCount") or stats.get("digg_count", 0),
                "comments": stats.get("commentCount") or stats.get("comment_count", 0),
                "posted_ts": posted_ts,
                "description": (item.get("desc", "") or "")[:150],
            })

    # YouTube — youtubecli search
    elif isinstance(data, dict) and ("videos" in data or "organic_results" in data):
        items = data.get("videos") or data.get("organic_results") or []
        for item in items:
            views = item.get("views", 0)
            if isinstance(views, str):
                views = int(views.replace(",", "").replace(" views", "").replace(" ", "")) if views else 0
            vid_id = item.get("id", "")
            videos.append({
                "platform": "youtube",
                "url": f"https://www.youtube.com/watch?v={vid_id}" if vid_id else item.get("link", ""),
                "username": item.get("channel", {}).get("name", "?") if isinstance(item.get("channel"), dict) else str(item.get("channel", "?")),
                "views": views,
                "likes": item.get("likes", 0),
                "comments": item.get("comments", 0),
                "posted_ts": 0,  # YouTube search doesn't always give exact timestamp
                "description": (item.get("description", "") or "")[:150],
            })

    return videos


def rank(videos, days, min_views, top_k):
    """Filter, score, and rank videos."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    cutoff_ts = int(cutoff.timestamp())

    filtered = []
    for v in videos:
        # Filter by freshness (skip if no timestamp — YouTube search)
        if v["posted_ts"] > 0 and v["posted_ts"] < cutoff_ts:
            continue
        # Filter by minimum views
        if v["views"] < min_views:
            continue
        # Filter out empty URLs
        if not v["url"]:
            continue
        filtered.append(v)

    # Calculate scores
    for v in filtered:
        if v["posted_ts"] > 0:
            age_days = max(1, (now - datetime.fromtimestamp(v["posted_ts"], tz=timezone.utc)).days)
        else:
            age_days = days  # Fallback: assume middle of window
        v["age_days"] = age_days
        v["velocity"] = round(v["views"] / age_days)
        views = max(v["views"], 1)
        v["engagement_rate"] = round((v["likes"] + v["comments"]) / views * 100, 2)
        v["score"] = round(v["velocity"] * v["engagement_rate"])

    # Sort by score descending
    filtered.sort(key=lambda v: v["score"], reverse=True)

    # Top-K
    results = filtered[:top_k]

    # Add rank
    for i, v in enumerate(results, 1):
        v["rank"] = i

    return results


def format_number(n):
    """Format number as human-readable: 1.5M, 300K, etc."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def main():
    parser = argparse.ArgumentParser(description="Rank videos by viral score")
    parser.add_argument("--days", type=int, default=7, help="Freshness window in days (default: 7)")
    parser.add_argument("--min-views", type=int, default=50000, help="Minimum views threshold (default: 50000)")
    parser.add_argument("--top-k", type=int, default=3, help="Return top K videos (default: 3)")
    args = parser.parse_args()

    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: no data on stdin", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    videos = detect_and_extract(data)
    if not videos:
        print("Error: no videos found in input", file=sys.stderr)
        sys.exit(1)

    print(f"Parsed {len(videos)} videos from {videos[0]['platform']}", file=sys.stderr)

    results = rank(videos, args.days, args.min_views, args.top_k)

    if not results:
        print(f"No videos passed filters (days={args.days}, min_views={args.min_views})", file=sys.stderr)
        print("Falling back to top by raw views...", file=sys.stderr)
        # Fallback: ignore freshness, just sort by views
        videos.sort(key=lambda v: v["views"], reverse=True)
        results = videos[:args.top_k]
        for v in results:
            views = max(v["views"], 1)
            v["age_days"] = args.days
            v["velocity"] = round(v["views"] / args.days)
            v["engagement_rate"] = round((v["likes"] + v["comments"]) / views * 100, 2)
            v["score"] = round(v["velocity"] * v["engagement_rate"])
        for i, v in enumerate(results, 1):
            v["rank"] = i

    # Print human-readable to stderr
    for v in results:
        print(
            f"#{v['rank']} @{v['username']} | {format_number(v['views'])} views | "
            f"{v['age_days']}d | vel={format_number(v['velocity'])}/d | "
            f"ER={v['engagement_rate']}% | score={format_number(v['score'])} | "
            f"{v['platform']}",
            file=sys.stderr,
        )

    # Print JSON to stdout
    # Clean output: remove posted_ts (internal)
    output = []
    for v in results:
        output.append({
            "rank": v["rank"],
            "platform": v["platform"],
            "url": v["url"],
            "username": v["username"],
            "views": v["views"],
            "likes": v["likes"],
            "comments": v["comments"],
            "age_days": v["age_days"],
            "velocity": v["velocity"],
            "engagement_rate": v["engagement_rate"],
            "score": v["score"],
            "description": v["description"],
        })

    print(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n# Top {len(results)} videos ranked by viral score (velocity × ER)", file=sys.stderr)


if __name__ == "__main__":
    main()
