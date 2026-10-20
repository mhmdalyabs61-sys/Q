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
        self.wfile.write(b"Roblox Smart Wordlist Sniper is Running!")

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
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                return username, True, "متاح حقيقي 100% 🔥"
            else:
                return username, False, "مأخوذ أو محجوز"
        else:
            return username, False, f"خطأ HTTP: {response.status_code}"
    except Exception:
        return username, False, "خطأ اتصال"

def generate_wordlist_usernames(count):
    # مقاطع ذكية وكلمات قصيرة تساعد في صيد يوزرات تنقري وتجي مرتبة
    prefixes = ["zen", "vex", "vyn", "lox", "kox", "nex", "rix", "vex", "zix", "flux", "core", "vibe", "apex", "echo", "nova", "xor", "ion", "lux"]
    suffixes = ["ai", "ix", "ox", "ex", "z", "x", "q", "9", "7", "5", "1"]
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    
    unique_set = set()
    
    while len(unique_set) < count:
        choice = random.choice([1, 2, 3, 4])
        
        if choice == 1:
            # رباعي مرتب (حرف علة بالنص)
            uname = random.choice(consonants) + random.choice(vowels) + random.choice(consonants) + random.choice(string.ascii_lowercase)
        elif choice == 2:
            # خماسي مرتب
            uname = random.choice(prefixes)
            if len(uname) > 5:
                uname = uname[:5]
            elif len(uname) < 5:
                uname += random.choice(string.ascii_lowercase)
        elif choice == 3:
            # رباعي مع رقم أو حرف مميز
            uname = "".join(random.choices(string.ascii_lowercase, k=3)) + random.choice(string.digits)
        else:
            # خماسي بدمج مقطع مع حرف وشرطة سفلية خفيفة
            uname = random.choice(consonants) + random.choice(vowels) + "_" + "".join(random.choices(string.ascii_lowercase, k=2))
            
        # تنظيف والتأكد من الطول والشروط
        uname = uname.lower().strip()
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            if len(uname) in [4, 5]:
                unique_set.add(uname)
                
    return list(unique_set)

send_discord_message("🎯 **تم تفعيل وضع (الدمج الذكي للكلمات والمقاطع)!** البوت يستهدف الرباعي والخماسي المرتب...")
print("[*] البوت شغال بنظام الدمج الذكي للرباعي والخماسي...")

total_checked = 0

while True:
    batch_usernames = generate_wordlist_usernames(40)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(future_to_user):
            total_checked += 1
            user_name, is_available, details = future.result()
            
            # تحديد هل هو رباعي أو خماسي حسب الطول
            size_type = "رباعي 💎" if len(user_name) == 4 else "خماسي 🌟"
            
            print(f"[{total_checked}] ({size_type}) يوزر: {user_name} ➔ الحالة: {details}")
            
            if is_available:
                print(f"🔥 [ صيدة حقيقية ونظيفة! ] ({size_type}) ➔ {user_name}")
                send_discord_message(f"🔥 **صيد جديد ومتاح حقيقةً!**\n نوعه: **{size_type}**\n اليوزر: `{user_name}`\n@everyone")

    if total_checked >= 120:
        send_discord_message(f"📊 **تقرير دوري:** تم فحص `{total_checked}` يوزر بذكاء... البوت شغال 🔄")
        total_checked = 0

    time.sleep(1)
