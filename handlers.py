from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ChatPermissions
from aiogram.filters import Command, CommandStart, and_f
from buttons.reply import menu, check
from buttons.inline import job
from aiogram.fsm.context import FSMContext
from config import ADMIN, GROUP_ID
from states import SignupStates, check_phone, users, GetUserName, get_user_ball

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # htts://t.me/bot_name?start=17781273 --> /start 127877997
    if message.text[7:].isdigit():
        if users.get(str(message.from_user.id)):
            if int(message.text[7:]) == message.from_user.id:
                await message.answer("Siz o'zingizga referal bo'lolmaysiz")
            else:
                await message.answer("Siz botdan ro'yhatdan o'tgansiz")
        else:
            refer_id = message.text[7:]
            users[str(message.from_user.id)] = {'refer_id': refer_id, 'flag': False}
            await state.set_state(GetUserName.name)
            await message.answer("ismingizni kiriting")
    else:
        if users.get(str(message.from_user.id)):
            if users.get(str(message.from_user.id)).get('flag'):
                await message.answer("Asosiy menyu", reply_markup=menu)
            else:
                await state.set_state(GetUserName.name)
                await message.answer("ismingizni kiriting")
        else:
            users[str(message.from_user.id)] = {'refer_id': None, 'flag': False}
            await state.set_state(GetUserName.name)
            await message.answer("ismingizni kiriting")


@router.message(GetUserName.name)
async def state_name(message: Message, state: FSMContext):
    if 4 <= len(message.text) <= 30:
        if not any(digit in message.text for digit in '0123456789'):
            users[str(message.from_user.id)]['user_name'] = message.text
            users[str(message.from_user.id)]['flag'] = True
            await message.answer(f"✅Malumotlaringiz\n\n {users[str(message.from_user.id)]}\n\n", reply_markup=menu)
            await state.clear()
        else:
            await message.answer("❌ Ismda raqamlar bo\'lishi mukunemas")
    else:
        await message.answer("❌ Ismda usunligi xato")


@router.message(F.text == 'Referal havola')
async def havola(message: Message, state: FSMContext):
    if users.get(str(message.from_user.id)):
        ref_link = f'https://t.me/for_testtbot?start={message.from_user.id}'
        await message.answer(f"Sizning referal havolangiz\n\n{ref_link}", reply_markup=menu)
    else:
        users[str(message.from_user.id)] = {'refer_id': None, 'flag': False}
        await state.set_state(GetUserName.name)
        await message.answer("ismingizni kiriting")


@router.message(F.text == 'Mening ballarim')
async def ballar(message: Message, state: FSMContext):
    if users.get(str(message.from_user.id)):
        user_ball = get_user_ball(str(message.from_user.id))
        await message.answer(f"Sizning Ballingiz:\n\n{user_ball}", reply_markup=menu)
    else:
        users[str(message.from_user.id)] = {'refer_id': None, 'flag': False}
        await state.set_state(GetUserName.name)
        await message.answer("ismingizni kiriting")


@router.message(Command('help'))
async def start(message: Message):
    text = f"🤖Hello {message.from_user.full_name}\nFor help https://t.me/diyorbek_backend"
    await message.answer(text)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@router.message(F.text == 'SignUP')
async def signup(message: Message, state: FSMContext):
    await message.answer(f'Salom Ariza qoldirish uchun \n Ismingizni kiriting')
    await state.set_state(SignupStates.name)


@router.message(Command("stop"))
async def state_name(message: Message, state: FSMContext):
    curent = await state.get_state()  # signuostates:name None
    if curent == None:
        await message.answer('State mavjud emas')
    else:
        await message.answer(f"Jarayon bekor qilindi {curent}")
        await state.clear()


@router.message(Command("new"))
async def state_name(message: Message, state: FSMContext):
    curent = await state.get_state()  # signuostates:name None
    if curent == None:
        await message.answer(f'Salom Ariza qoldirish uchun \n Ismingizni kiriting ')
        await state.set_state(SignupStates.name)
    else:
        await state.clear()
        await message.answer(f'Salom Ariza qoldirish uchun \n Ismingizni kiriting ')
        await state.set_state(SignupStates.name)


@router.message(SignupStates.name)
async def state_name(message: Message, state: FSMContext):
    if 4 <= len(message.text) <= 30:
        if not any(digit in message.text for digit in '0123456789'):
            await state.update_data(name=message.text)
            await message.answer(f"✅Ism qabul qilindi\n{message.text}\n\n Yoshingizni kiriting ")
            await state.set_state(SignupStates.age)
        else:
            await message.answer("❌ Ismda raqamlar bo\'lishi mukunemas")
    else:
        await message.answer("❌ Ismda usunligi xato")


@router.message(SignupStates.age)
async def state_name(message: Message, state: FSMContext):
    if message.text.isdigit():
        if 20 <= int(message.text) <= 50:
            await state.update_data(age=message.text)
            await message.answer(f"✅Yosh qabul qilindi\n{message.text}\n\n Telefon raqamingizni kiriting ")
            await state.set_state(SignupStates.phone)
        else:
            await message.answer("❌ Yosh to\'g\'ri kelmaydi")
    else:
        await message.answer("❌ Sonli malumot kiriting")


@router.message(SignupStates.phone)
async def state_name(message: Message, state: FSMContext):
    phone = check_phone(message.text)
    if phone == "phone":
        await state.update_data(phone=message.text)
        await message.answer(f"✅Telefon raqam qabul qilindi\n{message.text}\n\n Kasbingizni kiriting ",
                             reply_markup=job)
        await state.set_state(SignupStates.job)
    else:
        await message.answer("❌ Telefon raqam kiriting")


@router.callback_query(SignupStates.job)
async def state_name(call: CallbackQuery, state: FSMContext):
    await state.update_data(job=call.data)
    await call.message.answer(f"✅Kasb qabul qilindi\n{call.data}\n\n Maqsadingizni kiriting ")
    await state.set_state(SignupStates.goal)


@router.message(SignupStates.goal)
async def state_name(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer(f"✅Maqsadingiz qabul qilindi\n{message.text}\n\n ")
    data = await state.get_data()
    ariza = (f"Ariza Beruvchi: {data.get('name')}\n"
             f"Yosh: {data.get('age')}\n"
             f"User name: @{message.from_user.username}\n"
             f"Telefon raqam: {data.get('phone')}\n"
             f"Kasb: {data.get('job')}\n"
             f"Maqsad: {data.get('goal')}")
    await message.answer(f"Arizani tasdiqlaysizmi\n\n{ariza} \n\nHa yoki /new ni tanlang", reply_markup=check)
    await state.set_state(SignupStates.verify)


@router.message(SignupStates.verify)
async def state_name(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == 'ha':
        data = await state.get_data()
        ariza = (f"Ariza Beruvchi: {data.get('name')}\n"
                 f"Yosh: {data.get('age')}\n"
                 f"User name: @{message.from_user.username}\n"
                 f"Telefon raqam: {data.get('phone')}\n"
                 f"Kasb: {data.get('job')}\n"
                 f"Maqsad: {data.get('goal')}")
        await message.answer(ariza + f"\n\n📝Malumotlaringiz adminga yuborildi", reply_markup=menu)
        await bot.send_message(ADMIN, f"📝Yangi malumot:\n\n{ariza}")
        await state.clear()
    else:
        txt = (f"Arizani tasdiqlash: Ha \n"
               f"Arizani bekor qilish: /stop \n"
               f"Arizani boshidan boshlash: /new \n")
        await message.answer(txt, reply_markup=check)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@router.message(and_f(F.chat.id == -1002256449828, F.text == 'info'))
async def get_info(message: Message):
    text = (f"Chat ma\'lumotlari:\n"
            f"Chat turi: {message.chat.type} \n"
            f"Chat nomi: {message.chat.title} \n"
            f"Chat id: {message.chat.id}")
    await message.answer(text)


@router.message(and_f(F.chat.id == -1002256449828, F.new_chat_members))
async def get_info(message: Message):
    for new_chat_member in message.new_chat_members:
        await message.answer(f"Hi {new_chat_member.full_name}")
        await message.delete()


@router.message(and_f(F.chat.id == -1002256449828, F.left_chat_member))
async def get_info(message: Message):
    await message.answer(f"Bye {message.left_chat_member.full_name}")
    await message.delete()


@router.message(and_f(F.chat.id == -1002256449828, and_f(F.text == "/mute", F.reply_to_message)))
async def get_info(message: Message):
    user_id = message.reply_to_message.from_user.id
    permissions = ChatPermissions(can_send_messages=False)
    await message.chat.restrict(user_id, permissions)
    await message.answer(f"{message.reply_to_message.from_user.mention_html()} yoshidan cheklani", parse_mode='HTML')


@router.message(and_f(F.chat.id == -1002256449828, and_f(F.text == "/unmute", F.reply_to_message)))
async def get_info(message: Message):
    user_id = message.reply_to_message.from_user.id
    permissions = ChatPermissions(can_send_messages=True)
    await message.chat.restrict(user_id, permissions)
    await message.answer(f"{message.reply_to_message.from_user.mention_html()} yosha oladi", parse_mode='HTML')


@router.message(and_f(F.chat.id == -1002256449828, and_f(F.text == "/ban", F.reply_to_message)))
async def get_info(message: Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.ban_sender_chat(user_id)
    await message.answer(f"❗{message.reply_to_message.from_user.mention_html()} guruhdan chetlatildi",
                         parse_mode='HTML')


@router.message(and_f(F.chat.id == -1002256449828, and_f(F.text == "/unban", F.reply_to_message)))
async def get_info(message: Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.unban_sender_chat(user_id)
    await message.answer(f"❗{message.reply_to_message.from_user.mention_html()} Blockdan chiqarildi",
                         parse_mode='HTML')
