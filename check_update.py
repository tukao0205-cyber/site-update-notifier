import requests
import hashlib
import os

# チェックするサイト
URL = "https://pointlessjourney.jp"

# 前回のハッシュを保存するファイル
HASH_FILE = "last_hash.txt"

# Discord Webhook URL（GitHub Secretsから取得）
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def get_site_hash(url):
    """サイトの内容を取得してハッシュ化"""
    response = requests.get(url)
    response.raise_for_status()
    return hashlib.sha256(response.text.encode("utf-8")).hexdigest()

def load_last_hash():
    """前回保存したハッシュを読み込み"""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_hash(h):
    """最新のハッシュを保存"""
    with open(HASH_FILE, "w") as f:
        f.write(h)

def send_discord_notification(message):
    """Discordに通知を送信"""
    if not DISCORD_WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK_URL is not set")
        return
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def main():
    new_hash = get_site_hash(URL)
    last_hash = load_last_hash()

    if last_hash and new_hash != last_hash:
        send_discord_notification(f"サイトが更新されました！ {URL}")

    save_last_hash(new_hash)

if __name__ == "__main__":
    どうすればいい
