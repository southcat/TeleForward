import asyncio

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from pyrogram import errors, Client
from pyrogram.enums import ChatType

from config import db
from config.config import ClientMap, api_id, api_hash

from telegram import Userbot

router = APIRouter()


router = APIRouter()



@router.get("/syncMessage")
async def syncMessage(task_id: int, background_tasks: BackgroundTasks):
    # 更新任务状态为"正在同步"
    db.update(f"UPDATE replay_task SET status = '正在同步' WHERE id = {task_id}")
    
    # 将同步任务添加到后台任务
    background_tasks.add_task(sync_messages, task_id)
    
    return {"message": "同步任务已开始"}

# @router.get("/syncMessage")
# async def syncMessage(task_id: int):
#     num = 0
#     result = db.get_task_by_id(task_id)
#     task = result[0]
#     [id, account_id, chat_id, target_id] = task
#     result2 = db.get_account_phone_number_by_id(account_id)
#     account = result2[0]
#     [phone_number] = account

#     client = ClientMap[phone_number]
#     chat_id = int(chat_id)

#     # 获取数据库中最新的消息ID
#     sql = f"SELECT message_id FROM messages WHERE chat_id = {chat_id} AND target_id = {target_id} ORDER BY message_id DESC LIMIT 1"
#     result = db.query(sql)
#     last_synced_id = result[0][0] if result else 0

#     print(f"上次同步的最新消息ID: {last_synced_id}")

#     offset_id = 0  # 从最新的消息开始
#     all_synced = False

#     while not all_synced:
#         try:
#             messages = []
#             async for message in client.get_chat_history(chat_id, offset_id=offset_id, limit=100):
#                 if message.id <= last_synced_id:
#                     all_synced = True
#                     break
#                 messages.append(message)

#             if not messages:
#                 print("没有新消息，同步结束")
#                 break

#             for message in reversed(messages):
#                 num += 1
#                 print(f"正在处理第 {num} 条消息，消息ID: {message.id}")
#                 sql = f"INSERT INTO messages (message_id, chat_id, target_id, forwarded, account_id) VALUES ({message.id}, {chat_id}, {target_id}, 0, {account_id})"
#                 db.insert(sql)

#             if messages:
#                 offset_id = messages[-1].id  # 更新offset_id为本批次最后一条消息的ID

#             await asyncio.sleep(1)  # 每批次请求完成后等待1秒

#         except errors.FloodWait as e:
#             print(f"超出速率限制，等待 {e.value} 秒。")
#             await asyncio.sleep(e.value)
#         except Exception as e:
#             print(f"发生错误: {e}")
#             break

#     return {"message": "同步成功", "同步消息数": num}
async def sync_messages(task_id: int):
    num = 0
    result = db.get_task_by_id(task_id)
    task = result[0]
    [id, account_id, chat_id, target_id] = task
    result2 = db.get_account_phone_number_by_id(account_id)
    account = result2[0]
    [phone_number] = account

    client = ClientMap[phone_number]
    chat_id = int(chat_id)

    # 获取数据库中最新的消息ID
    sql = f"SELECT message_id FROM messages WHERE chat_id = {chat_id} AND target_id = {target_id} ORDER BY message_id DESC LIMIT 1"
    result = db.query(sql)
    last_synced_id = result[0][0] if result else 0

    print(f"上次同步的最新消息ID: {last_synced_id}")

    offset_id = 0  # 从最新的消息开始
    all_synced = False

    while not all_synced:
        try:
            messages = []
            async for message in client.get_chat_history(chat_id, offset_id=offset_id, limit=100):
                if message.id <= last_synced_id:
                    all_synced = True
                    break
                messages.append(message)

            if not messages:
                print("没有新消息，同步结束")
                break

            for message in reversed(messages):
                num += 1
                print(f"正在处理第 {num} 条消息，消息ID: {message.id}")
                sql = f"INSERT INTO messages (message_id, chat_id, target_id, forwarded, account_id) VALUES ({message.id}, {chat_id}, {target_id}, 0, {account_id})"
                db.insert(sql)

            if messages:
                offset_id = messages[-1].id  # 更新offset_id为本批次最后一条消息的ID

            await asyncio.sleep(1)  # 每批次请求完成后等待1秒

        except errors.FloodWait as e:
            print(f"超出速率限制，等待 {e.value} 秒。")
            await asyncio.sleep(e.value)
        except Exception as e:
            sql = f"UPDATE replay_task SET status = '同步失败' WHERE id = {task_id}"
            db.update(sql)
            break

    print(f"同步完成，共处理了 {num} 条消息")