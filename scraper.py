import json
import requests

# আপনার মূল টফি ডেটা সোর্স বা API লিংকটি এখানে বসান
TOFFEE_SOURCE_API = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/main/toffee_data.json"

def fetch_and_update():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # ১. সোর্স থেকে লেটেস্ট ডেটা ফেচ করা
        response = requests.get(TOFFEE_SOURCE_API, headers=headers, timeout=15)
        response.raise_for_status()
        channels = response.json()

        # ২. toffee_data.json আপডেট ও সেভ করা
        with open("toffee_data.json", "w", encoding="utf-8") as jf:
            json.dump(channels, jf, indent=4, ensure_ascii=False)
        print("✅ toffee_data.json successfully updated.")

        # ৩. toffee_playlist.m3u ফরম্যাট তৈরি ও সেভ করা
        m3u_lines = ["#EXTM3U\n"]
        for ch in channels:
            name = ch.get("name", "Unknown Channel")
            logo = ch.get("logo", "")
            group = ch.get("category", ch.get("group", "Toffee"))
            url = ch.get("link", ch.get("url", ""))

            if url:
                line = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n'
                m3u_lines.append(line)

        with open("toffee_playlist.m3u", "w", encoding="utf-8") as mf:
            mf.writelines(m3u_lines)
        print("✅ toffee_playlist.m3u successfully updated.")

    except Exception as e:
        print(f"❌ Error during scrape/update: {e}")

if __name__ == "__main__":
    fetch_and_update()
