import asyncio
import time

from config import db
from utils import messageForward


async def history_replay(app, account_id):
    while True:
        messages = db.query(f"SELECT message_id, chat_id, target_id FROM messages WHERE forwarded = 0 AND exception is null AND account_id = {account_id} ORDER by message_id limit 100")

        if not messages:
            print(f"No new messages to forward for account {account_id}")
            await asyncio.sleep(60)  # 等待一分钟后再次检查
            continue

        for message_id, chat_id, target_id in messages:
            chat_id = int(chat_id)
            target_id = int(target_id)
            print(f"Processing message_id: {message_id}")

            try:
                message = await app.get_messages(chat_id, message_id)
                # print(message,"消息")
                if message is None:
                    print("Message not found")
                    db.exception_as_forwarded(message_id, chat_id, "Message not found")
                    await asyncio.sleep(10)
                    continue

                if message.has_protected_content:
                    await messageForward.hasPprotectedContent(app, message_id, chat_id, target_id)
                else:
                    await messageForward.noHasPprotectedContent(app, message_id, chat_id, target_id)

            except Exception as e:
                print(f"Error processing message {message_id}: {str(e)}")
                db.exception_as_forwarded(message_id, chat_id, str(e))
                await asyncio.sleep(10)

        await asyncio.sleep(1)  # 每批处理完后稍作等待


