import subprocess
import json
import csv
from datetime import datetime
import os

# 1. 配置监控参数
KEYWORDS = ["RDK", "X3", "X5", "S100", "TROS"]
PAIN_POINT_SUFFIXES = ["报错", "失败", "教程", "坑", "怎么用"]
# 平台配置：(platform_name, command_subgroup, supports_keyword_search)
PLATFORM_CONFIGS = [
    ("zhihu", "search", True),
    ("xiaohongshu", "search", True),
    ("google", "search", True),
    ("reddit", "search", True),
    ("hackernews", "search", True),
]

TIMESTAMP = datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = "horizon_keyword_monitor.csv"
PAIN_POINTS_FILE = "horizon_pain_points.csv"

def run_opencli(site, cmd_name, *args, limit=10):
    try:
        # 修复命令格式：opencli <site> <command>
        full_cmd = ["opencli", site, cmd_name] + list(args) + ["-f", "json", "--limit", str(limit)]
        print(f"Executing: {' '.join(full_cmd)}")
        result = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT)
        return json.loads(result.decode('utf-8'))
    except Exception as e:
        print(f"Error executing {site} {cmd_name} with args {args}: {e}")
        return []

def collect_data():
    all_data = []
    pain_points = []

    # 2. 基础趋势监控
    for kw in KEYWORDS:
        for platform, cmd, _ in PLATFORM_CONFIGS:
            results = run_opencli(platform, cmd, kw, limit=10)
            for item in results:
                all_data.append({
                    "date": TIMESTAMP,
                    "platform": platform,
                    "keyword": kw,
                    "type": item.get("type", "post"),
                    "title": item.get("title") or item.get("suggestion") or item.get("content", "")[:50],
                    "url": item.get("url", ""),
                    "author": item.get("author", ""),
                    "votes": item.get("votes", 0),
                    "heat": item.get("heat", 0)
                })
        
        # CSDN 专项
        csdn_results = run_opencli("google", "search", f"site:csdn.net {kw}", limit=10)
        for item in csdn_results:
            all_data.append({
                "date": TIMESTAMP,
                "platform": "csdn",
                "keyword": kw,
                "type": "article",
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "author": "",
                "votes": 0,
                "heat": 0
            })

    # 3. 痛点深入提取
    for kw in KEYWORDS:
        for suffix in PAIN_POINT_SUFFIXES:
            query = f"{kw} {suffix}"
            zh_results = run_opencli("zhihu", "search", query, limit=5)
            for item in zh_results:
                pain_points.append({
                    "date": TIMESTAMP,
                    "keyword": kw,
                    "suffix": suffix,
                    "platform": "zhihu",
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "excerpt": item.get("excerpt", "")
                })
            go_results = run_opencli("google", "search", query, limit=5)
            for item in go_results:
                 pain_points.append({
                    "date": TIMESTAMP,
                    "keyword": kw,
                    "suffix": suffix,
                    "platform": "google",
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "excerpt": item.get("snippet", "")
                })

    save_to_csv(OUTPUT_FILE, all_data, ["date", "platform", "keyword", "type", "title", "url", "author", "votes", "heat"])
    save_to_csv(PAIN_POINTS_FILE, pain_points, ["date", "keyword", "suffix", "platform", "title", "url", "excerpt"])
    print(f"\n[SUCCESS] Global monitoring complete.")

def save_to_csv(filename, data, fieldnames):
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        urls = set()
        unique_rows = []
        for row in data:
            u = row.get('url')
            if u and u not in urls:
                urls.add(u)
                unique_rows.append(row)
        writer.writerows(unique_rows if unique_rows else data)

if __name__ == "__main__":
    collect_data()
