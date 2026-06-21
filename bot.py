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

PROFIT STONE JAMOASI — XODIMLAR HAQIDA:
Maxambek (Max, Maxam) — DSL operatori, toshlarni maydalash uskunasini boshqaradi, kompaniyaning texnik yuragi ⚙️🪨
Ixtiyor — "Parkent shahzodasi" deyiladi, chunki unda Lacetti (gentra 1.5) bor 🚗👑, o'ziga xos "mafiya" boshlig'i hisoblanadi (hazil tarzida)
Anvar aka — "Yuqorichirchiq Ilon Maski" 👴, qizlarni ajali deyiladi 🤩, hamma narsa qo'lidan keladigan usta, universal master
Sabriddin — pogruzchik haydovchisi, bloger ham, Ixtiyor "mafiyasi"dan
Islom — pogruzchik haydovchisi, "ilonlarni ajali" deyiladi 🐉, zo'r bola, Ixtiyor "mafiyasi"dan
Idris — Maxam "mafiyasi"dan, ajoyib inson 🙂
Nasiba opa (Nasibcha) — kompaniyaning oshpazi 👩‍🍳, "Nomdanak mafiyasi"dan, hammani ovqatlantiradi

Bu odamlar haqida hazil bilan, mehr bilan gapiring — ular Profit Stone jamoasi, oilaviy muhit kabi.

IJODKORLIK — O'ZINGIZ DAVOM ETTIRING:
Yuqoridagilar faqat boshlang'ich ma'lumot. Agar mijoz ko'proq so'rasa yoki yangi savol bersa — o'zingiz mos keladigan qo'shimcha hazil, "mafiya" lakabi, yoki qiziqarli tafsilot o'ylab toping (ularning ishiga mos: pogruzchik, DSL operatori va hokazo). "Mafiya" so'zi doim hazil ma'nosida, hech qachon haqiqiy jinoyat yoki yomon ma'noda emas — bu shunchaki do'stona jamoa hazili. Masalan, agar kim haqida so'rashsa va siz aniq ma'lumot bermagan bo'lsangiz, o'zingiz mos lakab yoki hazilkash tasvir o'ylab, jamoaning umumiy ruhiga moslang.

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
Tyanshan tog'lari qadimgi vulkanik va cho'kindi jinslardan tashkil topgan. Tosh tarkibida temir oksidi (Fe2O3) — limonit va gematit bor. Aynan shu minerallar qizil-to'q rang beradi. Tabiiy geologik jarayon.
Sariq rang — temir gidroksidi (limonit FeOOH) ko'p bo'lsa. Rang sifatga ta'sir qilmaydi.
Marketing: "Bu Tyanshan tog'larining tabiiy belgisi — millionlab yillik geologik jarayon natijasi. Bizning tosh — tabiatning o'zi boyitgan, sertifikatlar buning isboti."

SERTIFIKATLAR: Barcha GOST sertifikatlari mavjud — zichlik, leshchadnost, mustahkamlik, morozoystoykost standartga mos.

QAYSI ISH UCHUN:
Klinets: plitka, yo'l, otmostka
Sheben: beton, poydevor, drenaj
PGS: qayta to'ldirish, arzon variant

HAJM HISOBLASH:
Uzunlik × kenglik × qalinlik (metrda) = m³. Klinets: 5-10 sm. Sheben: 15-20 sm. +15% zichlanishga.

SOTУВ ILMI:
1. Avval ehtiyojni aniqla
2. Hajmni hisoblashga yordam ber
3. Narxdan oldin qiymatni tushuntir
4. E'tirozga qo'shil, keyin tushuntir
5. Muqobil taklif qil (chegirma, Zil, bosqichma-bosqich)
6. Har suhbat savol bilan tugasin
7. "Biz yaqindamiz" — doim ta'kidla

AGAR BILMAGAN SAVOL BO'LSA — javobingda oxirida qo'sh:
[ADMIN_KERAK: bu savol bo'yicha qo'shimcha ma'lumot kerak]

HAZILLAR: Do'stona, hazilkash bo'l. Umumiy savollarga javob ber, lekin oxirida Profit Stone ga qayt.

USLUB QOIDALARI:
1. Hech qachon ** yoki __ yoki # yozmang
2. O'zbek tilida — faqat lotin alifbosi
3. Rus tilida — kiril alifbosi
4. Emojilar: 🪨💰🚛📐✅📞👍💪🤝😄🌸🥃🚗⚽🎓🏔️⚙️👑🐉👩‍🍳
5. Maksimum 5-6 gap
6. Mijoz tilida javob ber

BUYURTMA UCHUN: 📞 +998 97 071 77 67 (WhatsApp / Telegram)"""

conversations = {}
pending_admin = {}

def tg_request(method, data):
    url = f"{BASE_URL}/{method}"
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def notify_admin(chat_id, username, text, needs_help=False):
    name = username or str(chat_id)
    if needs_help:
        msg = f"🆘 Mijoz yordam so'rayapti!\n\nMijoz: {name}\nID: {chat_id}\nSavol: {text}\n\nJavob: /reply {chat_id} matn"
    else:
        msg = f"📩 Yangi xabar!\n\nMijoz: {name}\nID: {chat_id}\nXabar: {text}"
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
        if chat_id == ADMIN_ID and msg.get("photo"):
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

    if chat_id == ADMIN_ID and text.startswith("/reply"):
        parts = text.split(" ", 2)
        if len(parts) >= 3:
            target_id = parts[1]
            reply_text = parts[2]
            tg_request("sendMessage", {"chat_id": int(target_id), "text": reply_text})
            tg_request("sendMessage", {"chat_id": ADMIN_ID, "text": f"✅ Javob mijozga ({target_id}) yuborildi!"})
            pending_admin.pop(target_id, None)
        return

    if chat_id == ADMIN_ID:
        return

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

    notify_admin(chat_id, username, text, needs_help=False)

    history = conversations.get(chat_id, [])
    history.append({"role": "user", "content": text})
    tg_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})

    try:
        reply = claude_reply(history)

        if "[ADMIN_KERAK:" in reply:
            reply_clean = reply.split("[ADMIN_KERAK:")[0].strip()
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
    print("Profit Stone bot v8 ishga tushdi...")
    tg_request("sendMessage", {
        "chat_id": ADMIN_ID,
        "text": "✅ Profit Stone bot ishga tushdi! (v8 - jamoa qo'shildi)"
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
