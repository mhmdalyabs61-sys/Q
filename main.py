import urllib.request
import json
import urllib.parse
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://auth.roblox.com/v1/usernames/validation"

def check_username(username):
    params = urllib.parse.urlencode({
        'request.username': username,
        'request.birthday': '2000-01-01'
    })
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get('code') == 0:
                    return username, True
    except Exception:
        pass
    return username, False

def generate_unique_usernames(count):
    chars = string.ascii_lowercase + string.digits + "_"
    unique_set = set()
    while len(unique_set) < count:
        uname = "".join(random.choices(chars, k=4))
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            unique_set.add(uname)
    return list(unique_set)

batch_size = 250
attempt_round = 1

print("[*] البوت شغال صامت الآن.. يفر ويحفظ الصيد وبس!")

while True:
    usernames = generate_unique_usernames(batch_size)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_username, user): user for user in usernames}
        
        for future in as_completed(futures):
            user, is_available = future.result()
            if is_available:
                # يطبع بس إذا لقى صيد!
                print(f"\n🔥 [صيد متاح!]: {user}")
                with open("found.txt", "a", encoding="utf-8") as f:
                    f.write(user + "\n")

    attempt_round += 1
    time.sleep(1)
