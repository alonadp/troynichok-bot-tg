import time
import requests
import schedule
import json
import os
import logging
from datetime import datetime
from typing import Dict, Optional, Union, List, Any

# Импорты
from config import TOKEN, BOT_USERNAME, ALLOWED_CHAT_IDS
from oracul import get_random_quote as get_prediction
from oracul_ai import generate_reply

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация
class Config:
    URL = f"https://api.telegram.org/bot{TOKEN}/"
    API_TIMEOUT = 30
    SLEEP_INTERVAL = 1
    KNOWN_CHATS_FILE = "known_chats.json"
    REPORT_FILE = "report.txt"
    PREDICTION_TIME = "09:00"

class TelegramBot:
    def __init__(self):
        self.offset = None
        self.bot_id = self._get_bot_id()
        logger.info(f" Bot is starting with ID: {self.bot_id}")

    def _get_bot_id(self) -> str:
        try:
            response = requests.get(f"{Config.URL}getMe", timeout=Config.API_TIMEOUT)
            response.raise_for_status()
            return str(response.json()["result"]["id"])
        except Exception as e:
            logger.error(f"Error getting ID bot: {e}")
            exit(1)

    def load_known_chats(self) -> Dict[str, str]:
        if os.path.exists(Config.KNOWN_CHATS_FILE):
            with open(Config.KNOWN_CHATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_known_chat(self, chat_id: Union[int, str], title: str):
        chats = self.load_known_chats()
        if str(chat_id) not in chats:
            chats[str(chat_id)] = title
            with open(Config.KNOWN_CHATS_FILE, "w", encoding="utf-8") as f:
                json.dump(chats, f, indent=2)

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(Config.REPORT_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{now}]  Bot is admin in chat: {chat_id} ({title})\n")

            logger.info(f" New chat is save: {chat_id} ({title})")

    def send_message(self, chat_id: Union[int, str], text: str, reply_markup: Optional[Dict] = None):
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            data["reply_markup"] = reply_markup
        try:
            res = requests.post(Config.URL + "sendMessage", json=data)
            res.raise_for_status()
            return res.json().get("result", {}).get("message_id")
        except Exception as e:
            logger.error(f" Error send message in chat {chat_id}: {e}")

    def get_updates(self) -> List[Dict]:
        try:
            params = {"timeout": Config.API_TIMEOUT, "offset": self.offset}
            res = requests.get(Config.URL + "getUpdates", params=params)
            res.raise_for_status()
            data = res.json()
            updates = data.get("result", [])
            if updates:
                self.offset = updates[-1]["update_id"] + 1
            return updates
        except Exception as e:
            logger.error(f" Error get updates: {e}")
            return []

    def leave_chat(self, chat_id: Union[int, str]):
        """"Leave the chat if it is not allowed."""
        try:
            requests.post(f"{Config.URL}leaveChat", json={"chat_id": chat_id}, timeout=Config.API_TIMEOUT)
            logger.warning(f"The bot left the disallowed chat {chat_id}")
        except Exception as e:
            logger.error(f" Error exiting the chat {chat_id}: {e}")

    def send_daily_prediction(self):
        prediction = get_prediction()
        chats = self.load_known_chats()
        for chat_id in chats:
            self.send_message(chat_id, f"<b>Prediction of the day:</b>\n\n{prediction}")

    def handle_message(self, message: Dict[str, Any]):
        try:
            chat_id = message["chat"]["id"]
            chat_title = message["chat"].get("title", "Без названия")
            self.save_known_chat(chat_id, chat_title)

            # Защита от чужих чатов
            if chat_id not in ALLOWED_CHAT_IDS:
                logger.warning(f" The bot detected itself in a foreign chat {chat_id}. Уходим!")
                self.leave_chat(chat_id)
                return

            user = message["from"]
            user_id = str(user["id"])
            username = user.get("username", user.get("first_name", "NoName"))

            if user_id == self.bot_id:
                return


            if "text" in message:
                text = message["text"]

                if text == "/start" and not user.get("is_bot"):
                    self.send_message(chat_id, "The bot is activated. Ready to work!")
                    self.save_known_chat(chat_id, chat_title)

                elif text in ["/prediction"]:
                    self.send_message(chat_id, get_prediction())

                elif (
                    f"@{BOT_USERNAME}" in text.lower()
                    or message.get("reply_to_message", {}).get("from", {}).get("id") == int(self.bot_id)
                ):
                    self.send_message(chat_id, generate_reply(text))

        except Exception as e:
            logger.error(f" Error in handle_message: {e}")

    def run(self):
        logger.info("Bot is starting")
        schedule.every().day.at(Config.PREDICTION_TIME).do(self.send_daily_prediction)

        while True:
            updates = self.get_updates()
            for update in updates:
                if "message" in update:
                    self.handle_message(update["message"])

            schedule.run_pending()
            time.sleep(Config.SLEEP_INTERVAL)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
