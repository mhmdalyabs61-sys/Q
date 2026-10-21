import json
import random
import string
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# 1. سيرفر ويب وهمي لمنع نوم السيرفر على Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Roblox Proxy Sniper is Running!")

    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. إعدادات الديسكورد
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1562019919128698990/doPV-DBGiDRIsIq-e-y7hrRH8sgpwr58nN4USQJ8254JW5HuNHngz8AwCke-FgptzNjg"

def send_discord_message(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=3)
    except Exception:
        pass

# قائمة بروكسيات (يمكنك استبدالها بروكسيات حقيقية ونظيفة لضمان أفضل نتيجة)
PROXIES_LIST = [
    # أمثلة: "http://IP:Port",
    # إذا لم تتوفر بروكسيات، سيعمل الكود بدونها ولكن قد يعود لحالة الحظر
]

def get_random_proxy():
    if not PROXIES_LIST:
        return None
    proxy = random.choice(PROXIES_LIST)
    return {"http": proxy, "https": proxy}

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validation?request.username={username}&request.birthday=2000-01-01"
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.roblox.com/'
    }
    
    proxy = get_random_proxy()
    
    try:
        # إرسال الطلب مع البروكسي إن وجد لتجنب الحظر
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return username, True, data.get("code")
        return username, False, response.status_code
    except Exception:
        return username, False, 500

checked_history = set()

def generate_batch(count=50):
    chars_pool = string.ascii_lowercase + string.digits + "_"
    batch = set()
    attempts = 0
    
    while len(batch) < count and attempts < count * 5:
        attempts += 1
        length = random.choice([4, 5])
        uname = "".join(random.choices(chars_pool, k=length))
        
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            if uname not in checked_history:
                checked_history.add(uname)
                batch.add(uname)
                
    return list(batch)

send_discord_message("🛡️ **تم تفعيل السنايبر مع نظام تجاوز الحظر والبروكسيات!**")
print("[*] السنايبر يعمل الآن مع نظام حماية الاتصال...")

batch_counter = 0

while True:
    batch_usernames = generate_batch(50)
    if not batch_usernames:
        continue
        
    batch_counter += 1
    print(f"⚡ [لفة {batch_counter}] جاري فحص 50 يوزر...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(futures):
            username, success, code = future.result()
            size_type = "رباعي 💎" if len(username) == 4 else "خماسي 🌟"
            
            if success:
                print(f"فحص: {username} | كود: {code}")
                if code == 0:
                    hit_msg = f"🔥 **صيد أسطوري متاح!**\n النوع: **{size_type}**\n اليوزر: `{username}`\n@everyone"
                    print(f"🔥 صيدة نارية: {username}")
                    send_discord_message(hit_msg)
            else:
                print(f"خطأ اتصال أو حظر لـ {username}")

    time.sleep(1)
