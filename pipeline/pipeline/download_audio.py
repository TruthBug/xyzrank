import json
import feedparser
import requests
import os
from datetime import datetime

DATA_FILE = "hot_episodes.json"
OUTPUT_DIR = "audio"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_latest_episode(rss_url):
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print(f"❌ No entries found in RSS: {rss_url}")
        return None
    
    entry = feed.entries[0]   # 最新一期节目
    title = entry.title.replace("/", "_")
    
    if not entry.enclosures:
        print(f"❌ No audio found for: {title}")
        return None
    
    audio_url = entry.enclosures[0].href
    ext = audio_url.split("?")[0].split(".")[-1]  # 解析音频扩展名
    
    filename = f"{OUTPUT_DIR}/{title}.{ext}"
    
    print(f"⬇ Downloading: {audio_url}")
    print(f"📁 Saving as: {filename}")
    
    r = requests.get(audio_url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return filename

if __name__ == "__main__":
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 取前 5 条热播节目（避免一次下载太多）
    items = data if isinstance(data, list) else data.get("episodes", [])
    
    for item in items[:5]:
        rss = item.get("rss")
        if not rss:
            print("❌ Missing RSS field:", item)
            continue
        
        print(f"Processing RSS: {rss}")
        download_latest_episode(rss)

