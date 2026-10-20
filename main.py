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
        self.wfile.write(b"Roblox Instant Sniper is Running!")

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
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception:
        pass

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validation?request.username={username}&request.birthday=2000-01-01"
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return username, response.status_code, response.text
    except Exception as e:
        return username, 500, str(e)

checked_history = set()

def generate_unique_batch(count=40):
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u']
    rare_chars = ['q', 'x', 'z', '1', '7', '9', '0', '5']
    
    batch = set()
    attempts = 0
    
    while len(batch) < count and attempts < count * 10:
        attempts += 1
        length = random.choice([4, 5])
        use_underscore = random.choice([True, False])
        
        if length == 4:
            if use_underscore:
                pos = random.choice([1, 2])
                chars = random.choices(string.ascii_lowercase + string.digits, k=3)
                chars.insert(pos, '_')
                uname = "".join(chars)
            else:
                uname = random.choice(consonants) + random.choice(vowels) + random.choice(consonants) + random.choice(rare_chars)
        else:
            if use_underscore:
                pos = random.choice([1, 2, 3])
                chars = random.choices(string.ascii_lowercase + string.digits, k=4)
                chars.insert(pos, '_')
                uname = "".join(chars)
            else:
                uname = random.choice(consonants) + random.choice(vowels) + random.choice(consonants) + "".join(random.choices(string.ascii_lowercase, k=2))
                
        uname = uname.lower().strip()
        
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            if len(uname) in [4, 5]:
                if uname not in checked_history:
                    checked_history.add(uname)
                    batch.add(uname)
                    
    return list(batch)

send_discord_message("⚡ **تم تفعيل البوت (الفحص الفوري المباشر):** يبث الحالات أول بأول...")
print("[*] البوت شغال الآن ويرسل كل شي فوراً...")

total_checked = 0

while True:
    batch_usernames = generate_unique_batch(40)
    if not batch_usernames:
        time.sleep(1)
        continue
        
    found_hit = False
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(future_to_user):
            total_checked += 1
            user_name, status_code, raw_response = future.result()
            
            # طباعة الإرسال باللوغز
            print(f"[{total_checked}] يوزر: {user_name} | الحالة: {raw_response}")
            
            # إرسال حالة الفحص للديسكورد (اختياري، لو تبيه يرسل كل شي أو فقط الصيد. هنا يرسل الملخص للروم)
            # send_discord_message(f"فحص: `{user_name}` ➔ `{raw_response}`")
            
            # التحقق لو اليوزر متاح فعلاً
            if status_code == 200 and '"code":0' in raw_response:
                found_hit = True
                print(f"🔥 [ صيدة حقيقية فوريّة! ] ➔ {user_name}")
                send_discord_message(f"🔥 **صيد أسطوري ومتاح حقيقةً!**\n اليوزر: `{user_name}`\n الاستجابة: `{raw_response}`\n@everyone")
                break # أول ما يلقى صيدة يطلع من اللفة فوراً بدون ما يكمل الباقي

    if found_hit:
        # لو صاد يوزر يقدر يرتاح شوي أو يكمل فوراً
        time.sleep(1)
    else:
        time.sleep(0.3)
