from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pyrogram import errors, Client
import pyrogram
from pyrogram.enums import ChatType
from pyrogram.errors import ChannelPrivate


from config import db
from config.config import ClientMap, api_id, api_hash

from telegram import Userbot

router = APIRouter()


class PhoneNumberRequest(BaseModel):
    phone_number: str


class CodeRequest(BaseModel):
    phone_number: str
    code: str
    phone_code_hash: str
    pass_word: str


# 从这里开始编写路由
@router.get("/get-account-pool")
async def get_account_pool():
    poolList = []
    if not ClientMap:
        return {"account_pool": []}
    for client in ClientMap.values():
        try:
            me = await client.get_me()
            phone_number = me.phone_number
            connected = client.is_connected
            username = me.username
            poolList.append({"phone_number": phone_number, "connected": connected, "username": username})
        except Exception as e:
            ClientMap.pop(phone_number)
    return {"account_pool": poolList}


@router.post("/send-code")
async def send_code(request: PhoneNumberRequest):
    clientt = Client(name=request.phone_number, api_id=api_id, api_hash=api_hash, in_memory=True)
    ClientMap[request.phone_number] = clientt
    await clientt.connect()
    try:
        result = await clientt.send_code(request.phone_number)
        return {"phone_code_hash": result.phone_code_hash}
    except errors.RPCError as e:
        raise HTTPException(status_code=400, detail=f"Failed to send code: {e}")


@router.get("/get-session-string")
async def get_session_string():
    string_session = await Userbot.export_session_string()
    text = "**{} sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n`{}` \n\ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @Alexa_Help".format(
        "ᴘʏʀᴏɢʀᴀᴍ", string_session
    )
    print(text)
    # Userbot.send_message("me", text)

    return {"session_string": ""}


@router.post("/sign-in")
async def sign_in(request: CodeRequest):
    client = ClientMap[request.phone_number]
    if request.phone_number not in ClientMap:
        raise HTTPException(status_code=400, detail="该账号不存在账号池中")
    try:
        # 判断是否存在于账号池中
        user = await client.sign_in(request.phone_number, request.phone_code_hash, request.code)
        string_session = await client.export_session_string()
        db.save_accounts(request.phone_number, string_session)
        return {"status": "登录成功", "user": string_session}
    except errors.SessionPasswordNeeded:
        try:
            user = await client.check_password(request.pass_word)
            string_session = await client.export_session_string()
            db.save_accounts(request.phone_number, string_session)
            return {"status": "使用密码登录成功", "user": string_session}
        except errors.RPCError as e:
            raise HTTPException(status_code=400, detail=f"Password needed but failed to log in: {e}")
    except errors.RPCError as e:
        raise HTTPException(status_code=400, detail=f"登陆失败: {e}")


@router.get("/getStatus")
async def getStatus():
    me = await Userbot.get_me()
    print(me)

    return {"status": me.status}


# 编写结束
@router.get("/getAllgroup")
async def getAllgroup():
    dialogs = Userbot.get_dialogs(limit=100)
    dialogs_info = []

    async for dialog in dialogs:
        # 对每个对话进行处理，例如获取对话的标题和其他信息
        dialog_info = {
            "title": dialog.chat.title,
            "chat_id": dialog.chat.id,
            # 其他信息
        }
        dialogs_info.append(dialog_info)

    return {"dialogs": dialogs_info}


# 接收一个手机号参数
@router.get("/insertGroup")
async def insertGroup(phone_number: str):
    phone_number = phone_number.replace(" ", "+")
    if phone_number not in ClientMap:
        raise HTTPException(status_code=400, detail="该账号不存在账号池中")
    client = ClientMap[phone_number]
    dialogs = client.get_dialogs()
    accounts = db.get_accounts_by_phone_number(phone_number)
    account_id, phone_number, session_string = accounts[0]
    # 删除掉所有相关的
    sql = f"DELETE FROM groups WHERE account_id = {account_id}"
    db.delete(sql)
    inserted_count = 0
    error_count = 0
    
    try:
        async for dialog in dialogs:
            # print(dialog)
            try:
                if dialog.chat.type in [ChatType.GROUP, ChatType.CHANNEL, ChatType.SUPERGROUP]:
                    try:
                        db.insert_group(account_id, dialog.chat.id, str(dialog.chat.type), dialog.chat.title)
                        inserted_count += 1
                    except Exception as e:
                        print(f"插入群组时出错: {e}")
                        error_count += 1
            except ChannelPrivate:
                print(f"无法访问私有频道或群组: {getattr(dialog.chat, 'id', 'Unknown')}")
                error_count += 1
            except Exception as e:
                print(f"处理对话时出错: {e}")
                error_count += 1
    except Exception as e:
        print(f"获取对话列表时出错: {e}")
        
        # raise HTTPException(status_code=500, detail=f"获取对话列表失败: {str(e)}")

    return {
        "status": "success",
        "inserted_count": inserted_count,
        "error_count": error_count
    }


@router.get("/get-group-phone")
async def getGroupPhone(phone_number: str):
    phone_number = phone_number.replace(" ", "+")
    if phone_number not in ClientMap:
        raise HTTPException(status_code=400, detail="该账号不存在账号池中")
    accounts = db.get_accounts_by_phone_number(phone_number)
    account_id, phone_number, session_string = accounts[0]
    groups = db.get_all_group(account_id)
    # id,type,account_id,group_name,group_id
    groups = [
        {"id": group[0], "group_type": group[1], "account_id": group[2], "group_name": group[3], "group_id": group[4]}
        for group in groups]
    # 直接返回groups会丢失字段名，所以需要转换一下

    return {"groups": groups}


@router.get("/get-task-by-id")
async def getTaskById(phoneNumber: str):
    print(phoneNumber)
    phone_number = phoneNumber.replace(" ", "+")

    accounts = db.get_accounts_by_phone_number(phone_number)

    accountId, phone_number, session_string = accounts[0]
    result = db.get_accounts_task_by_id(accountId)
    tasks = [{"id": task[0], "account_id": task[1], "chat_id": task[2], "target_id": task[3]} for task in result]
    return {"tasks": tasks}


@router.get("/create-task")
async def createTask(phoneNumber: str, chatId: str, targetId: str):
    phone_number = phoneNumber.replace(" ", "+")
    accounts = db.get_accounts_by_phone_number(phone_number)
    accountId, phone_number, session_string = accounts[0]

    db.insert_task(accountId, chatId, targetId)
    return {"status": "success"}


@router.get("/delete-task-by-id")
async def deleteTaskById(id: str):
    db.delete_task_by_id(id)
    return {"status": "success"}
