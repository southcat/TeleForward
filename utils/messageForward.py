import os
import time

from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from config import db, config


async def noHasPprotectedContent(app, message_id, chat_id, target_id, max_retries=3):
    # 输出参数列表
    # print("app:", app)
    print("message_id:", message_id)
    print("chat_id:", chat_id)
    print("target_id:", target_id)

    for retry in range(max_retries):
        try:
            message = await app.get_messages(chat_id, message_id)
            # print(message, "消息")
            # if not hasattr(config.GroupId, str(chat_id)):
            #     config.GroupId[str(chat_id)].temp_group_id = 0
            # temp_group_id = getattr(config.GroupId, str(chat_id))
            # 判断GroupId中是否存在对应的键
            if str(chat_id) not in config.GroupId:
                config.GroupId[str(chat_id)] = 0

            # 获取 temp_group_id
            temp_group_id = config.GroupId[str(chat_id)]
            print(config.GroupId)
            print(temp_group_id, "temp_group_id")
            if message is None:
                print("Message not found")
                break
            try:
                if message.media_group_id is not None and temp_group_id is not None:
                    if message.media_group_id & message.media_group_id == temp_group_id:
                        db.mark_as_forwarded(message_id, chat_id, target_id)
                        break
                    config.GroupId[str(chat_id)] = message.media_group_id
                # print("进入复制",message.media_group_id)
                if message.media_group_id is not None:
                    await app.copy_media_group(int(target_id), int(chat_id), message_id)
                else:
                    await message.copy(int(target_id))
                # await app.forward_messages(int(target_id), int(chat_id), message_id)
                print("复制成功")
                db.mark_as_forwarded(message_id, chat_id, target_id)
                # config.GroupId[str(chat_id)] = message.media_group_id
            # 捕获洪水
            except FloodWait as e:
                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                time.sleep(e.value)  # Wait N seconds before continuing
                
            except Exception as e:
                print(e)
                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))

        except Exception as e:
            db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
            print(e, "错误信息")
            print("An error occurred, retrying...")
        else:
            break


async def hasPprotectedContent(app, message_id, chat_id, target_id, max_retries=3):
    for retry in range(max_retries):
        # print("retry:", retry)
        # print("message_id:", message_id)
        # 判断GroupId中是否存在对应的键
        if str(chat_id) not in config.GroupId:
            config.GroupId[str(chat_id)] = 0

        # 获取 temp_group_id
        temp_group_id = config.GroupId[str(chat_id)]

        print("config.temp_group_id:", temp_group_id)
        try:
            message = await app.get_messages(chat_id, message_id)
            if message.media_group_id:
                if message.media_group_id == temp_group_id:
                    db.mark_as_forwarded(message_id, chat_id, target_id)
                    break
                else:
                    # config.temp_group_id = message.media_group_id
                    # 重新赋值
                    config.GroupId[str(chat_id)] = message.media_group_id

                    messages = await app.get_media_group(chat_id, message.id)
                    media_groups = []
                    temp_path = []
                    for message in messages:
                        if message.photo:
                            if message.photo.file_id:
                                path = await app.download_media(message.photo.file_id,
                                                                file_name=message.photo.file_id + '.jpg')
                                temp_path.append(path)
                                # print(path)
                                if message.caption:
                                    media_groups.append(InputMediaPhoto(path, caption=message.caption))
                                else:
                                    media_groups.append(InputMediaPhoto(path))
                        if message.video:
                            if message.video.file_id:
                                path = await app.download_media(message.video.file_id,
                                                                file_name=message.video.file_id + '.mp4')
                                temp_path.append(path)
                                # print(path)
                                if message.caption:
                                    media_groups.append(InputMediaVideo(path, caption=message.caption))
                                else:
                                    media_groups.append(InputMediaVideo(path))
                    try:
                        await app.send_media_group(target_id, media_groups)
                        db.mark_as_forwarded(message_id, chat_id, target_id)
                        config.GroupId[str(chat_id)] = message.media_group_id
                    except FloodWait as e:
                        db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                        time.sleep(e.value)  # Wait N seconds before continuing
                        print(e)
                    except Exception as e:
                        db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                        print(e)
                        # print("An error occurred, retrying...")
                    finally:
                        #     输出消息id到exception.txt的下一行
                        with open('exception.txt', 'a') as f:
                            f.write('\n' + str(message.id))

                    for path in temp_path:
                        os.remove(path)
            else:
                if message.photo:
                    if message.photo.file_id:
                        path = await app.download_media(message.photo.file_id, file_name=message.photo.file_id + '.jpg')
                        if message.caption:
                            try:
                                await app.send_photo(target_id, path, caption=message.caption)
                                db.mark_as_forwarded(message_id, chat_id, target_id)
                            except FloodWait as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                time.sleep(e.value)  # Wait N seconds before continuing
                                print(e)
                            except Exception as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                print(e)
                                # print("An error occurred, retrying...")
                            finally:
                                #     输出消息id到exception.txt的下一行
                                with open('exception.txt', 'a') as f:
                                    f.write('\n' + str(message.id))
                        else:
                            try:
                                await app.send_photo(target_id, path)
                                db.mark_as_forwarded(message_id, chat_id, target_id)
                            except FloodWait as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                time.sleep(e.value)
                                print(e)
                            except Exception as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                print(e)
                                # print("An error occurred, retrying...")
                            finally:
                                #     输出消息id到exception.txt的下一行
                                with open('exception.txt', 'a') as f:
                                    f.write('\n' + str(message.id))
                        os.remove(path)
                if message.video:
                    if message.video.file_id:
                        path = await app.download_media(message.video.file_id, file_name=message.video.file_id + '.mp4')
                        if message.caption:
                            try:

                                await app.send_video(target_id, path, caption=message.caption)
                                db.mark_as_forwarded(message_id, chat_id, target_id)
                            except FloodWait as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                time.sleep(e.value)
                                print(e)
                            except Exception as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                print(e)
                                # print("An error occurred, retrying...")
                            finally:
                                #     输出消息id到exception.txt的下一行
                                with open('exception.txt', 'a') as f:
                                    f.write('\n' + str(message.id))
                        else:
                            try:
                                await app.send_video(target_id, path)
                                db.mark_as_forwarded(message_id, chat_id, target_id)
                            except FloodWait as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                time.sleep(e.value)
                                print(e)
                            except Exception as e:
                                db.exception_as_forwarded(message_id, chat_id, target_id, str(e))
                                print(e)
                                # print("An error occurred, retrying...")
                            finally:
                                #     输出消息id到exception.txt的下一行
                                with open('exception.txt', 'a') as f:
                                    f.write('\n' + str(message.id))
                        os.remove(path)
        except Exception as e:

            print(e)
            # print("An error occurred, retrying...")
        else:
            break  # 如果没有异常，退出循环
        if retry == max_retries - 1:
            # print("Max retries reached, giving up.")
            break
