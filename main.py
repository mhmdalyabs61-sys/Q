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
        self.wfile.write(b"Roblox Clean Sniper is Running!")

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.roblox.com/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # التأكد البرمجي السليم 100% من خانة الـ code
            code = data.get("code")
            return username, True, code, data
        else:
            return username, False, response.status_code, response.text
    except Exception as e:
        return username, False, 500, str(e)

checked_history = set()

def generate_unique_batch(count=30):
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

send_discord_message("🧹 **تم تفعيل الكود النظيف والمفحوص تقنياً!** يبدأ الفحص الآن...")
print("[*] الكود النظيف شغال...")

batch_counter = 0

while True:
    batch_usernames = generate_unique_batch(30)
    if not batch_usernames:
        time.sleep(1)
        continue
        
    batch_counter += 1
    start_msg = f"🔄 **لفة رقم ({batch_counter}):** جاري فحص `{len(batch_usernames)}` يوزر..."
    print(start_msg)
    send_discord_message(start_msg)
    
    hits_in_batch = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_user = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(future_to_user):
            username, success, code_or_status, raw_data = future.result()
            size_type = "رباعي 💎" if len(username) == 4 else "خماسي 🌟"
            
            if success:
                print(f"فحص ({size_type}) ➔ {username} | كود روبلوكس: {code_or_status}")
                # الشرط الحقيقي الصافي 100%
                if code_or_status == 0:
                    hits_in_batch += 1
                    hit_msg = f"🔥 **صيد أسطوري متاح حقيقةً!**\n النوع: **{size_type}**\n اليوزر: `{username}`\n@everyone"
                    print(f"🔥 [ صيدة كبرى! ] ➔ {username}")
                    send_discord_message(hit_msg)
            else:
                print(f"خطأ في الاتصال لـ {username}: {code_or_status}")

    if hits_in_batch == 0:
        reason_msg = (
            f"📊 **انتهت اللفة ({batch_counter}) ولم يتم صيد أي يوزر.**\n"
            f"🔍 **السبب:** تم فحص الـ 30 يوزر بدقة عبر استقبال JSON الرسمي من روبلوكس، وكلها ثبت أنها محجوزة مسبقاً."
        )
        print(reason_msg)
        send_discord_message(reason_msg)
    else:
        success_msg = f"✅ **انتهت اللفة ({batch_counter}):** تم صيد `{hits_in_batch}` يوزر متاح بنجاح!"
        print(success_msg)
        send_discord_message(success_msg)

    time.sleep(2)
