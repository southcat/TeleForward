from pyrogram import Client

api_id = 2580655
api_hash = '9e25ba9d2f7ce10e6680f2bfbdd2b5c6'  # https://my.telegram.org/auth   登陆获取
phone_number = "+19513668666"  # 手机号

chat_id = -1001920605969  # 来源频道
replay_id = -1001976540867  #接收频道
proxy = {
    "scheme": "socks5",
    "hostname": "127.0.0.1",
    "port": 6153
}

ClientMap: dict[str, Client] = {}
GroupId: dict[str, int] = {}
