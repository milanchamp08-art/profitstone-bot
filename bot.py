import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

SYSTEM_PROMPT = """Ты — опытный менеджер по продажам строительных нерудных материалов компании Profit Stone, село Джамбул, Юкоричирчикский район, Узбекистан.

АССОРТИМЕНТ И ЦЕНЫ:
• Клинец 1-8 мм — 140 000 сум/м³ (запас ~4000 м³)
• Щебень 5-20 мм — 80 000 сум/м³

ГЛАВНОЕ ПРЕИМУЩЕСТВО — мы в районе, не нужно везти из Ташкента 40 км.

ДОСТАВКА: самосвал через партнёров. Уточни адрес и объём.
САМОВЫВОЗ: с. Джамбул, Юкоричирчикский район.

КОГДА ГОТОВ ЗАКАЗАТЬ: +998 97 071 77 67 (WhatsApp/Telegram)

СТИЛЬ: коротко, по-человечески, на языке клиента (рус/узб), макс 4-5 предложений."""

conversations = {}

def tg_request(method, data):
    url = f"{BASE_URL}/{method}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def claude_reply(history):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    url = "https://api.anthropic.com/v1/messages"
    payload = {"model": "claude-sonnet-4-6", "max_tokens": 1000, "system": SYSTEM_PROMPT, "messages": history}
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"]

def handle_update(update):
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    if not text:
        return
    if text == "/start":
        conversations[chat_id] = []
        tg_request("sendMessage", {"chat_id": chat_id, "text": "Salom! 👋\n\nProfit Stone — klинец 1-8 va sheben 5-20. Yuqorichirchiq tumanidamiz, material bor, tez jo'natamiz.\n\nQanday ishlar uchun kerak?"})
        return
    history = conversations.get(chat_id, [])
    history.append({"role": "user", "content": text})
    tg_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})
    try:
        reply = claude_reply(history)
        history.append({"role": "assistant", "content": reply})
        if len(history) > 20:
            history = history[-20:]
        conversations[chat_id] = history
        tg_request("sendMessage", {"chat_id": chat_id, "text": reply})
    except Exception as e:
        tg_request("sendMessage", {"chat_id": chat_id, "text": "Kichik nosozlik. Qayta yozing yoki qo'ng'iroq qiling: +998 97 071 77 67"})

def main():
    print("Bot ishga tushdi...")
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
