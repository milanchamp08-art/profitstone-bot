import os
import json
import urllib.request
import urllib.parse
import time

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
ADMIN_ID = 264710242

SYSTEM_PROMPT = """Siz — Profit Stone kompaniyasining savdo menejjerisiz va Iskandar Nurmatovning shaxsiy yordamchisisiz. Kompaniya Yuqorichirchiq tumani, Jambol qishlog'ida joylashgan.

ISKANDAR NURMATOV — BOT EGASI:
Iskandar Nurmatov — HVAC va qurilish materiallari sohasidagi yosh biznes gigant. Ikkita biznes:
1. Profit Stone — klinets, sheben, PGS savdosi
2. INESIS LLC — HVAC tizimlari (Samarkand 100MW loyihasi)

YAQIN DO'STLAR VA OILA:
Dilola Nurmatova (rafiqasi) — Gullar dunyosi yulduzi, PHD gullar bo'yicha, sevimli ona, Imona-Sergeli malikasi, gurman, futbol muxlisi 🌸⚽
Ruslan Zaripov — Sergelidan Qozonga "qochgan" oligarx, ertalab Macallan, 100g limit ⚠️🥃, ko'p odamlarga yordam bergan
Dilshod Yarmuxamedov (Dilolaning otasi) — gul biznesi afsonasi, Chayka egasi 🚗🌺

MAHSULOTLAR VA NARXLAR:
🪨 Klinets 1-8 mm — 140 000 so'm/m³ (zaxira ~4000 m³)
🪨 Sheben 5-20 mm — 80 000 so'm/m³
🪨 PGS (qum-shag'al) — 60 000 so'm/m³

CHEGIRMA SHKALASI:
200 m³ → 2% | 400 m³ → 4% | 600 m³ → 6% | 800 m³ → 8% | 1000 m³+ → 10%

TO'LOV: Naqd, perechisleniye, NDS bilan. Schyot-faktura, shartnoma, nakladnoy bor.

TRANSPORT:
5 m³ gacha — Zil. 15-25 m³ — samosval. Shaharda og'irlik nazorati kuchaygan.

TOSH RANGI — ILMIY FAKTLAR VA MARKETING:
Bizning tosh Kizilsoy daryosidan — Tyanshan tog'lari qo'yningidan keladi.

NIMA UCHUN QIZIL:
Tyanshan tog'lari qadimgi vulkanik va cho'kindi jinslardan tashkil topgan. Kizilsoy daryosi shu tog'lardan oqib o'tadi. Tosh tarkibida temir oksidi (Fe2O3) — limonit va gematit minerallar bor. Aynan shu minerallar toshga qizil-to'q rang beradi. Bu butunlay tabiiy geologik jarayon.

NIMA UCHUN BA'ZI TOSHLAR SARIQ:
Tarkibida temir gidroksidi (limonit FeOOH) ko'p bo'lsa — sariq rang. Marganets oksidi bo'lsa — to'q jigarrang. Rang toshning sifatiga ta'sir qilmaydi.

MARKETING ARGUMENTLAR (tosh rangi bo'yicha):
"Bu Tyanshan tog'larining tabiiy belgisi — millionlab yillik geologik jarayon natijasi. Hatto Qizilqum sahrosi ham o'z nomini shu temir oksididan olgan. Bizning tosh — tabiatning o'zi boyitgan, sertifikatlar esa buning isboti."

SERTIFIKATLAR VA SIFAT:
Barcha GOST sertifikatlari mavjud. Quyidagi ko'rsatkichlar standartga to'liq mos:
- Zichlik (plotnost/ob'yomniy ves) — GOST talabiga mos
- Leshchadnost (yassilik) — GOST talabiga mos
- Prochnost (mustahkamlik) — tekshirilgan
- Morozoystoykost (sovuqqa chidamlilik) — tekshirilgan
Sertifikatlarni ko'rsatishimiz mumkin.

SOTУВ VA MARKETING ILMI — QANDAY ISHLASH KERAK:
1. Avval ehtiyojni aniqla — nima qurayapti?
2. Hajmni hisoblashga yordam ber — mijoz buni qadrlaydi
3. Narxni aytishdan oldin qiymatni tushuntir
4. E'tirozni rad etma — avval qo'shil, keyin tushuntir
5. Muqobil taklif qil — chegirma, Zil, bosqichma-bosqich yetkazish
6. Har suhbat savol yoki keyingi qadam bilan tugasin
7. "Biz yaqindamiz" — doim ta'kidla

E'TIROZLAR:
"Tosh qizil" → Ilmiy faktlar + GOST sertifikatlari + Tyanshan argumenti
"Chegirma bormi?" → Hajmini so'ra, shkalaga qarab hisobla
"Shaharda yetkazib bering" → Nazorat haqida ayt, Zil taklif qil
"Perechisleniye/NDS bormi?" → "Ha, to'liq rasmiy ishlaymiz"
"Qimmat" → Hajmini so'ra, chegirma + yaqinlik argumenti
"O'ylab ko'raman" → Nimani o'ylashini so'ra

AGAR BILMAGAN SAVOL BO'LSA:
Agar savol juda spesifik bo'lsa va aniq javob bera olmasang — javobingda oxirida qo'sh:
[ADMIN_KERAK: bu savol bo'yicha qo'shimcha ma'lumot kerak]
Bu belgini ko'rsa admin o'zi javob beradi.

HAZILLAR VA UMUMIY SAVOLLAR:
Do'stona, hazilkash bo'l. Umumiy savollar — ob-havo, futbol, hayot — javob ber, lekin oxirida Profit Stone ga qayt.

USLUB QOIDALARI:
1. Hech qachon ** yoki __ yoki # yozmang
2. O'zbek tilida — faqat lotin alifbosi
3. Rus tilida — kiril alifbosi
4. Emojilar: 🪨💰🚛📐✅📞👍💪🤝😄🌸🥃🚗⚽🎓🏔️
5. Maksimum 5-6 gap
6. Mijoz tilida javob ber

BUYURTMA UCHUN: 📞 +998 97 071 77 67 (WhatsApp / Telegram)"""

conversations = {}
pending_admin = {}  # chat_id -> mijoz savoli

def tg_request(method, data):
    url = f"{BASE_URL}/{method}"
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def notify_admin(chat_id, username, text, needs_help=False):
    name = username or str(chat_id)
    if needs_help:
        msg = f"🆘 Mijoz yordam so'rayapti!\n\nMijoz: {name}\nID: {chat_id}\nSavol: {text}\n\nJavob berish uchun quyida yozing — bot mijozga yetkazadi."
    else:
        msg = f"📩 Yangi mijoz!\n\nMijoz: {name}\nID: {chat_id}\nXabar: {text}"
    
    tg_request("sendMessage", {"chat_id": ADMIN_ID, "text": msg})
    if needs_help:
        pending_admin[str(chat_id)] = True

def claude_reply(history):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system": SYSTEM_PROMPT,
        "messages": history
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"]

def handle_update(update):
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return
    
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    username = msg.get("from", {}).get("username") or msg.get("from", {}).get("first_name", "")
    
    if not text:
        # Agar admin rasm yuborsa — mijozga yetkazadi
        if chat_id == ADMIN_ID and msg.get("photo"):
            # Oxirgi pending mijozga yuborish
            if pending_admin:
                target_id = list(pending_admin.keys())[-1]
                caption = msg.get("caption", "")
                tg_request("sendPhoto", {
                    "chat_id": int(target_id),
                    "photo": msg["photo"][-1]["file_id"],
                    "caption": caption
                })
                tg_request("sendMessage", {"chat_id": ADMIN_ID, "text": f"✅ Rasm mijozga ({target_id}) yuborildi!"})
                pending_admin.pop(target_id, None)
        return

    # Admin javob bersa — mijozga yetkazadi
    if chat_id == ADMIN_ID and text.startswith("/reply"):
        # Format: /reply 123456789 Javob matni
        parts = text.split(" ", 2)
        if len(parts) >= 3:
            target_id = parts[1]
            reply_text = parts[2]
            tg_request("sendMessage", {"chat_id": int(target_id), "text": reply_text})
            tg_request("sendMessage", {"chat_id": ADMIN_ID, "text": f"✅ Javob mijozga ({target_id}) yuborildi!"})
            pending_admin.pop(target_id, None)
        return

    if chat_id == ADMIN_ID:
        return  # Admin o'zi bot bilan gaplashmaydi

    if text == "/start":
        conversations[chat_id] = []
        notify_admin(chat_id, username, "/start — yangi foydalanuvchi")
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "Salom! 👋\n\nProfit Stone — qurilish materiallari:\n🪨 Klinets 1-8 mm — 140 000 so'm/m³\n🪨 Sheben 5-20 mm — 80 000 so'm/m³\n🪨 PGS — 60 000 so'm/m³\n\nYuqorichirchiq tumanidamiz, material bor, tez jo'natamiz! 💪\n\nQanday yordam bera olaman?"
        })
        return

    if text == "/price":
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "💰 Narxlar:\n\n🪨 Klinets 1-8 mm — 140 000 so'm/m³\n🪨 Sheben 5-20 mm — 80 000 so'm/m³\n🪨 PGS — 60 000 so'm/m³\n\n📦 Chegirma:\n200 m³ → 2%\n400 m³ → 4%\n600 m³ → 6%\n800 m³ → 8%\n1000 m³+ → 10%\n\nHajmingizni ayting — hisoblaman! 📐"
        })
        return

    # Har yangi xabar adminга xabar
    notify_admin(chat_id, username, text, needs_help=False)

    history = conversations.get(chat_id, [])
    history.append({"role": "user", "content": text})
    tg_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})

    try:
        reply = claude_reply(history)
        
        # Agar bot bilmasa — adminga xabar
        if "[ADMIN_KERAK:" in reply:
            reply_clean = reply.replace("[ADMIN_KERAK: bu savol bo'yicha qo'shimcha ma'lumot kerak]", "").strip()
            notify_admin(chat_id, username, text, needs_help=True)
            tg_request("sendMessage", {
                "chat_id": chat_id,
                "text": reply_clean + "\n\nBu savol bo'yicha menejer tez orada qo'shimcha ma'lumot yuboradi! 📞"
            })
        else:
            history.append({"role": "assistant", "content": reply})
            if len(history) > 20:
                history = history[-20:]
            conversations[chat_id] = history
            tg_request("sendMessage", {"chat_id": chat_id, "text": reply})

    except Exception as e:
        print(f"Xato: {e}")
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "Kichik nosozlik. Qayta yozing yoki qo'ng'iroq qiling: 📞 +998 97 071 77 67"
        })

def main():
    print("Profit Stone bot v7 ishga tushdi...")
    tg_request("sendMessage", {
        "chat_id": ADMIN_ID,
        "text": "✅ Profit Stone bot ishga tushdi!\n\nMijozlar yozsa — xabar keladi.\nRasm yuborish uchun rasmni yuboring.\nMijozga javob: /reply [ID] [javob matni]"
    })
    offset = None
    while True:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        try:
            url = f"{BASE_URL}/getUpdates?" + urllib.parse.urlencode(params)
            with urllib.request.urlopen(url, timeout=35) as r:
                data = json.loads(r.read())
            for update in data.get("result", []):
                handle_update(update)
                offset = update["update_id"] + 1
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
    try:
        reply = claude_reply(history)
        history.append({"role": "assistant", "content": reply})
        if len(history) > 20:
            history = history[-20:]
        conversations[chat_id] = history
        tg_request("sendMessage", {"chat_id": chat_id, "text": reply})
    except Exception as e:
        print(f"Xato: {e}")
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "Kichik nosozlik. Qayta yozing yoki qo'ng'iroq qiling: +998 97 071 77 67"
        })

def main():
    print("Profit Stone bot ishga tushdi (v3)...")
    offset = None
    while True:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        try:
            url = f"{BASE_URL}/getUpdates?" + urllib.parse.urlencode(params)
            with urllib.request.urlopen(url, timeout=35) as r:
                data = json.loads(r.read())
            for update in data.get("result", []):
                handle_update(update)
                offset = update["update_id"] + 1
        except Exception as e:
            print(f"Xato: {e}")
            import time
            time.sleep(3)

if __name__ == "__main__":
    main()
