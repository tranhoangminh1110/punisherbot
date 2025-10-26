from aiogram import Bot, Dispatcher, executor, types
from flask import Flask, request
import time
import asyncio
import logging
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
logging.basicConfig(level=logging.INFO)
limit = datetime.datetime.now() - datetime.timedelta(seconds=4)
bot = Bot(token = '6304012917:AAGYbshMlkK8JbyosQAYdJfne48PMS7pfac')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
#lệnh mở bot
@dp.message_handler(commands=['online'])
async def hello(message: types.Message):
    await message.reply('Punisher online, ready to punish !!!')
#mở bot    
@dp.message_handler(Command('wru'))
async def wru(message: types.message):
    await message.reply('tôi là Punisher, sẵn sàng trừng trị kẻ phản đồ')


@dp.message_handler(commands=['chem']) # ✅ V2 Decorator
async def send_vid_path(message: types.Message):
    """
    Gửi video từ file cục bộ.
    """
    try:
        # Trong V2, thường dùng InputFile cho file cục bộ hoặc mở file
        with open('media/thelu.mp4', 'rb') as video_file:
            await bot.send_video(
                chat_id=message.chat.id, # V2 dùng message.chat.id
                video=video_file, # Truyền file object đã mở
                
            )
        
    except FileNotFoundError:
        await message.answer("Lỗi: Không tìm thấy file 'media/thelu.mp4' trên máy chủ.")
    except Exception as error:
        # ✅ V2/V3 đều nên dùng message.answer để báo lỗi
        await message.answer(f"Đã xảy ra lỗi khi gửi video: {error}")

@dp.message_handler(commands=['chui']) # ✅ V2 Decorator
async def send_audio_path(message: types.Message):
    """
    Gửi video từ file cục bộ.
    """
    try:
        # Trong V2, thường dùng InputFile cho file cục bộ hoặc mở file
        with open('media/theluaudio.mp3', 'rb') as video_file:
            await bot.send_audio(
                chat_id=message.chat.id, # V2 dùng message.chat.id
                audio=video_file, # Truyền file object đã mở
                
            )
        
    except FileNotFoundError:
        await message.answer("Lỗi: Không tìm thấy file 'media/theluaudio.mp3' trên máy chủ.")
    except Exception as error:
        # ✅ V2/V3 đều nên dùng message.answer để báo lỗi
        await message.answer(f"Đã xảy ra lỗi khi gửi video: {error}")



#hàm chống spam sticker
sticker_count = {}
@dp.message_handler(Command('stk_rule'))
async def stk_rule(message: types.Message):
    await message.reply('spam tối thiếu sticker 3 lần,\nnếu tiếp tục quá 3 lần sẽ bị tuyên tội thất động ')

"""dưới đây là các bộ lệnh được sử dụng bởi các admin group
bao gồm mute người dùng, đá người dùng, mở lại quyền hạn cho người dùng"""
@dp.message_handler(Command('punish'))
async def punish(message: types.Message):
    try:
        user_id = message.reply_to_message.from_user.id
        reply_text = "ta tuyên tội phán xét: Thất Động (im mồm)"
        if message.from_user.id == 5280294045:
            await bot.send_message(chat_id=message.chat.id, text=reply_text, reply_to_message_id=message.reply_to_message.message_id)
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=types.ChatPermissions())
            await message.reply("Đã Trừng phạt đối tượng ")
        elif message.from_user.id == 5400123658:
            await bot.send_message(chat_id=message.chat.id, text=reply_text, reply_to_message_id=message.reply_to_message.message_id)
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=types.ChatPermissions())
            await message.reply("Đã Trừng phạt đối tượng ")
        else:
            await message.reply("Quyền hạn này chỉ dành cho các thiết phán quan, rất tiếc")
    except AttributeError:
        await message.reply("kẻ nào sẽ phải bị trừng phạt thưa ngài ?")
    except Exception as e:
        await message.reply("không nhất thiết phải tuyên tội")
@dp.message_handler(Command('slash'))
async def slash(message: types.Message):
    if message.from_user.id == 5280294045:
        #tim hói
        try:
            user_id = message.reply_to_message.from_user.id
            reply_text = "ta tuyên tội phán xét: Trảm"
            await bot.send_message(chat_id=message.chat.id, text=reply_text, reply_to_message_id=message.reply_to_message.message_id)
            await bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=types.ChatPermissions())
            await message.reply("Đã Trừng phạt đối tượng ")
        except AttributeError:
            await message.reply("kẻ nào sẽ phải bị trừng phạt thưa ngài ?")
        except Exception as e:
            await message.reply("không nhất thiết phải thiết trảm")
    elif message.from_user.id == 5400123658:
        # phú nổ
        try:
            user_id = message.reply_to_message.from_user.id
            reply_text = "ta tuyên tội phán xét: Trảm"
            await bot.send_message(chat_id=message.chat.id, text=reply_text, reply_to_message_id=message.reply_to_message.message_id)
            await bot.kick_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=types.ChatPermissions())
            await message.reply("Đã Trừng phạt đối tượng ")
        except AttributeError:
            await message.reply("kẻ nào sẽ phải bị trừng phạt thưa ngài ?")
        except Exception as e:
            await message.reply("không nhất thiết phải thiết trảm")
    else: 
        await message.reply('Quyền hạn này chỉ dành cho các thiết phán quan, rất tiếc')
#quyền hạn sẽ không được thực hiện nếu như người thường sử dụng 
@dp.message_handler(Command('list_wp'))
async def wp(message: types.Message):
    await message.reply("Các phương thức trừng phạt kẻ chống đối:\n/slash\n/punish")
"""các bộ rule 
đã được tích sẵn dưới câu lệnh /rule
để tiện admin sử dụng"""
@dp.message_handler(Command('exc'))
async def excuse(message: types.Message):
    if message.from_user.id == 5280294045:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            reply_text = "mọi tội lỗi của người đã được xóa bỏ"
            await bot.send_message(chat_id=message.chat.id, text=reply_text, reply_to_message_id=message.reply_to_message.message_id)
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=types.ChatPermissions(can_send_messages=True,can_send_photos=True,can_send_other_messages=True))
        else:
            await message.reply("hãy chỉ định đối tượng cần được xóa án")
    elif message.from_user.id == 5400123658:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            reply_text = "mọi tội lỗi của người đã được xóa bỏ"
            await bot.send_message(chat_id=message.chat.id, text=reply_text, reply_to_message_id=message.reply_to_message.message_id)
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=types.ChatPermissions(can_send_messages=True,can_send_photos=True,can_send_other_messages=True))
        else:
            await message.reply("hãy chỉ định đối tượng cần được xóa án")
    else:
        await message.reply('Quyền hạn này chỉ thuộc về các bồi thẩm đoàn, rất tiếc')
#quyền hạn sẽ không được thực hiện nếu như người command là người bình thường
@dp.message_handler(Command('rule'))
async def rule(message: types.Message):
    await message.reply("\n1. không spam các vấn đề không liên quan như bán hàng, link 18+, lùa gà , lùa pi, spam xác"
                                    "\n2. không xúc phạm, bôi nhọ danh dự nhân phẩm của nhau"
                                    "\n3. đứa nào mem cũ quán tin vào xem phải tuân theo luật, có ý định tẩy trắng thì coi chừng"
                                    "\n4. Không được xàm xí về việc liên quan đến giả danh, chức vụ cấp cao như công an, sĩ quan, nếu chứng minh được thì cho qua"
                                    "\nCòn không chứng minh được thì chịu hậu quả"
                                    "\n5. Đưa tin lan truyền phải có xác thực , không có sau 5p ăn mute vv"
                                    "\n6. không gây war vô cớ, không được đưa chính quyền VN vào để bôi nhọ, xúc phạm"
                                    "\n7. Không được có lời lẽ mang tính man rợ, cực đoan"
                                    "\n8. không được spam sticker, ảnh quá nhiều lần"
                                    "\n9. Không được phân biệt vùng miền, đá xéo lẫn nhau bằng việc lôi gốc gác của mình"
                                    "\n10. Điều đặc biệt là không được có hành vi lăng mạ, xúc phạm đến admin đăng bài"
                                    )
@dp.message_handler(Command('use'))
async def use(message: types.Message):
    await message.reply("tương tác với tôi bằng các lệnh sau"
                        "\n/online"
                        "\n/wru"
                        "\n/list_wp"
                        "\n/rule"
                        "\n/punish (nếu như bạn được cấp quyền admin)"
                        "\n/slash (nếu như bạn được cấp quyền admin)"
                        "\n/exc (nếu như bạn là admin)")
"""lệnh rule của rose sẽ được thay thế
bằng lệnh /use của punisher để tránh trường hợp 
trùng lệnh với các bot khác 
lệnh use được sử dụng để hiện thị các tập lệnh có thể tương tác
với punisher """

@dp.message_handler(commands=['ask_vs'])
async def rule(message: types.Message):
    await message.reply("Thiên thần Victoria Secret 🎀🪞🩰🦪️")

@dp.message_handler(commands=['split'])
async def rule(message: types.Message):
    await message.reply("Ngu vãi cả lồn")

if __name__ == '__main__':
    executor.start_polling(dp)