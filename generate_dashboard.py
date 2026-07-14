#!/usr/bin/env python3
"""Regenerates README.md — the daily 'morning coffee' upskill dashboard.
Deterministic by UTC date: the same day always renders the same picks, so
re-running is idempotent and the daily rotation is stable across the day.
"""
import json, random, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "repos.json").read_text(encoding="utf-8"))

today = datetime.date.today()
# Seed RNG with the ordinal date so picks are stable per-day but rotate daily.
rng = random.Random(today.toordinal())

pool = list(data["daily_pool"])
rng.shuffle(pool)
picks = pool[:3]                       # 3 rotating repos of the day
tip = data["tips"][today.toordinal() % len(data["tips"])]

# Pick one anchor to spotlight as "today's focus" so the long ones stay visible.
focus = data["anchors"][today.toordinal() % len(data["anchors"])]

def repo_block(r, num=None):
    head = f"{num}. " if num else ""
    lines = [f"### {head}[{r['name']}]({r['url']})",
             f"**{r['cat']}**  ·  ⏱ {r['time']}  ·  📊 {r['level']}",
             "",
             r["gain"], ""]
    return "\n".join(lines)

out = []
out.append("# ☕ Haseeb's Daily Upskill Dashboard")
out.append("")
out.append(f"> **{today.strftime('%A, %d %B %Y')}** — open this with your morning coffee, do one thing, close the day better than you opened it.")
out.append("")
out.append("Auto-updates every morning. Your edge is **AI + offensive security** — everything here bends toward that. Job alerts live in [`ALERTS.md`](ALERTS.md).")
out.append("")
out.append("---")
out.append("")
out.append(f"## 🎯 Today's goal")
out.append(f"Pick **ONE** repo below, clone it, run it once, and write 3 lines on what it does. Finishing one beats sampling three.")
out.append("")
out.append(f"> 💡 **Tip of the day:** {tip}")
out.append("")
out.append("---")
out.append("")
out.append("## 🔥 Today's rotating picks")
out.append("*(3 fresh repos from your stars, reshuffled daily)*")
out.append("")
for i, r in enumerate(picks, 1):
    out.append(repo_block(r, i))
out.append("---")
out.append("")
out.append("## ⭐ Today's anchor spotlight")
out.append("*(one of your must-do long-haul repos, rotated in so it never gets forgotten)*")
out.append("")
out.append(repo_block(focus))
out.append("---")
out.append("")
out.append("## 📌 Must-do anchors (the long ones — chip away daily)")
out.append("These are your backbone. Do a little every day; they're too big for one sitting.")
out.append("")
for r in data["anchors"]:
    out.append(f"- **[{r['name']}]({r['url']})** — _{r['cat']}_ · ⏱ {r['time']}")
    out.append(f"  <br>{r['gain']}")
out.append("")
out.append("---")
out.append("")
out.append("## 📚 Full rotating pool")
out.append("<details><summary>Every repo in the daily rotation (click to expand)</summary>")
out.append("")
by_cat = {}
for r in data["daily_pool"]:
    by_cat.setdefault(r["cat"], []).append(r)
for cat in sorted(by_cat):
    out.append(f"**{cat}**")
    for r in by_cat[cat]:
        out.append(f"- [{r['name']}]({r['url']}) — {r['gain']}")
    out.append("")
out.append("</details>")
out.append("")
out.append("---")
out.append(f"<sub>Generated {today.isoformat()} · rotates daily · edit <code>repos.json</code> to change the pool.</sub>")

(ROOT / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"README.md regenerated for {today.isoformat()} with {len(picks)} picks + anchor '{focus['name']}'.")
