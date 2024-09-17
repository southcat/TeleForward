import time

from config import db
from utils import messageForward
from config.config import *

app = Client("my_account", api_id, api_hash, phone_number=phone_number, device_model='PC')


def remove_after_newline(s):
    if "\n" in s:
        return s.split("\n", 1)[0]
    return s


from pyrogram import utils


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new


async def history_replay():
    await app.start()
    while True:
        messages = db.get_unforwarded_messages_for_lasts()
        if not messages:
            print("No new messages to forward")
            break
        for message_id, chatId in messages:
            # print(type(chatId))
            chatId = int(chatId)
            print(message_id,"message_id")

            message = await app.get_messages(chatId, message_id)
            if message is None:
                print("Message not found")
                db.exception_as_forwarded(message_id, chatId, "Message not found")
                time.sleep(10)
                continue
            else:
                print(chatId)
                if message.has_protected_content:
                    await messageForward.hasPprotectedContent(app, message_id, chatId, replay_id)
                else:
                    await messageForward.noHasPprotectedContent(app, message_id, chatId, replay_id)


if __name__ == '__main__':
    max_retries = 3  # 设置最大重试次数
    app.run(history_replay())
