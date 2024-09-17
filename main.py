import asyncio
import json
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from api import accountRouter, groupRouter
from config import db
from config.config import api_id, api_hash, ClientMap
from scheduler.syncHistory import start_sync
from telegram import Userbot

app = FastAPI()

# Token验证中间件
@app.middleware("http")
async def token_validator(request: Request, call_next):
    # 排除不需要验证token的路径,比如登录接口
    if request.url.path in ["/login", "/docs", "/openapi.json"]:
        return await call_next(request)

    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "未提供token"})
    
    # 去掉 "Bearer " 前缀
    token = token.replace("Bearer ", "")
    
    if token != "aabbddcc":
        return JSONResponse(status_code=401, content={"detail": "无效的token"})
    
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源。你可以指定特定的域名，例如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(accountRouter.router,prefix='/account',tags=['账户管理'])
app.include_router(groupRouter.router,prefix='/group',tags=['群组管理'])
from pyrogram import Client, errors, utils


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new


# 使用 pydantic 定义请求体






# @Userbot.on_message(filters.all)
# async def my_handler(client, message):
#     print("接收到群组消息")
#     print(f"群组ID: {message.chat.id}")
#     print(f"群组名称: {message.chat.title}")
#     print(f"消息ID: {message.message_id}")
#     print(f"消息内容: {message.text}")


# 异步函数来启动Pyrogram客户端
async def start_tg_client():
    accounts = db.get_all_accounts()
    # print(accounts)
    for account in accounts:
        # print(accounts)
        account_id,phone_number,session_string = account
        client = Client(name=phone_number, api_id=api_id, api_hash=api_hash, session_string=session_string)
        ClientMap[phone_number] = client
        await client.start()
        print(f"账号 {phone_number} 登陆成功")
        print(ClientMap)
    # 账号全部登陆成功之后创建转发任务
    # Todo 同步消息任务什么时候做
    asyncio.create_task(start_sync())







# 异步函数来停止Pyrogram客户端
async def stop_tg_client():
    for client in ClientMap.values():
        await client.stop()
        print(f"账号 {client.name} 已经退出")




# 在每个请求之前启动Pyrogram客户端
@app.on_event("startup")
async def on_startup():
    await asyncio.create_task(start_tg_client())


async def job():
    await Userbot.send_message("me", "Hi!")


# 在每个请求之后停止Pyrogram客户端
@app.on_event("shutdown")
async def on_shutdown():
    await stop_tg_client()



class chatGroup(BaseModel):
    chat_id: str
@app.post("/getGroup")
async def getGroup(chat: chatGroup):
    chat_id = chat.chat_id
    print(chat_id, "123123")
    chatInfo = await Userbot.get_chat(chat_id=chat_id)
    return json.loads(str(chatInfo))


# @app.on_event("lifespan")
async def lifespan_handler(app: FastAPI):
    await start_tg_client()
    yield
    await stop_tg_client()
