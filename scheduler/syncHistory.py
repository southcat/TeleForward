import asyncio
from pyrogram import Client
from config import db
from config.config import ClientMap
from scheduler.frowardHistory import history_replay


async def start_sync():
    accounts = db.get_all_accounts()
    tasks = []

    for account in accounts:
        account_id, phone_number, session_string = account
        client = ClientMap[phone_number]

        # 创建后台任务
        task = asyncio.create_task(history_replay(client, account_id))
        tasks.append(task)
        print(f"Started background task for account {account_id}")

    # 等待所有任务完成（实际上它们会一直运行）
    await asyncio.gather(*tasks)
