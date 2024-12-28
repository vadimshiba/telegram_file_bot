import telebot
from database import *
from config import *
import random
import time

bot = telebot.TeleBot(BOT_TOKEN)
bot_info = bot.get_me()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Received /start command with message: {message.text}")
    
    # Проверяем наличие команды после пробела
    if ' ' in message.text:
        command = message.text.split(' ', 1)[-1].strip()
        print(f"Extracted command: {command}")
        if command:
            handle_command(message, command)
            return

    welcome_text = (
        "Привет! 👋 Я *Бот*, здесь, чтобы помочь вам.\n\n"
        "Вы можете использовать следующие команды для взаимодействия со мной:\n\n"
        "📚 `/help` - Получить список доступных команд.\n"
        "🔍 Отправьте команду в формате `/<команда>` для получения специфических файлов.\n\n"
        "_Если вы столкнетесь с какими-либо проблемами или у вас есть вопросы, не стесняйтесь использовать команду_ `/help`."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

def handle_command(message, command):
    print(f"Handling command: {command}")
    file_ids = get_files_by_command(command)
    if file_ids:
        captcha = str(random.randint(1000, 9999))
        captcha_state[message.from_user.id] = (captcha, file_ids)
        print(f"Generated captcha: {captcha} for user: {message.from_user.id}")
        bot.send_message(message.from_user.id, f"🔒 Для получения файлов введите капчу *{captcha}* в чате ", parse_mode='Markdown')
    else:
        print(f"Command not found: {command}")
        bot.reply_to(message, "⚠️ Команда не найдена. Пожалуйста, проверьте правильность ввода команды.", parse_mode='Markdown')




@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.from_user.id
    
    if is_admin(user_id):
        # Сообщение для администраторов
        help_text_admin = (
            "🛠 *Команды для администраторов:*\n\n"
            "➕ `/addadmin <user_id>` - Добавить администратора.\n"
            "➖ `/removeadmin <user_id>` - Удалить администратора.\n"
            "📁 `/addfile` - Добавить файлы и связать их с командой.\n"
            "🗑 `/removefile <команда>` - Удалить файлы, связанные с указанной командой.\n\n"
            "_Чтобы добавить файлы, используйте команду /addfile, затем отправьте файлы и укажите команду для доступа с помощью_ `/command <ваша_команда>`."
        )
        bot.send_message(message.chat.id, help_text_admin, parse_mode='Markdown')
    else:
        # Сообщение для обычных пользователей
        help_text_user = (
            "📚 *Команды для пользователей:*\n\n"
            "🔑 Отправьте команду в формате `/<команда>` для получения файлов.\n"
            "🔐 Если файлы защищены капчей, следуйте инструкциям для их получения."
        )
        bot.send_message(message.chat.id, help_text_user, parse_mode='Markdown')

# Глобальный словарь для хранения состояний добавления файлов администраторами
admin_file_addition_state = {}

@bot.message_handler(commands=['addadmin'])
def handle_add_admin(message):
    if message.from_user.id == ADMIN_IDS[0]:  # Предполагаем, что главный админ - первый в списке
        try:
            user_id = int(message.text.split()[1])
            if add_admin(user_id):
                bot.reply_to(message, "✅ Администратор добавлен.", parse_mode='Markdown')
            else:
                bot.reply_to(message, "⚠️ Этот пользователь уже является администратором.", parse_mode='Markdown')
        except (IndexError, ValueError):
            bot.reply_to(message, "🚨 Пожалуйста, используйте команду в формате: `/addadmin <user_id>`", parse_mode='Markdown')
    else:
        bot.reply_to(message, "🛑 У вас нет прав для выполнения этой команды.", parse_mode='Markdown')

@bot.message_handler(commands=['removeadmin'])
def handle_remove_admin(message):
    if message.from_user.id == ADMIN_IDS[0]:  # Проверка на главного админа
        try:
            user_id = int(message.text.split()[1])
            if remove_admin(user_id):
                bot.reply_to(message, "✅ Администратор удален.", parse_mode='Markdown')
            else:
                bot.reply_to(message, "⚠️ Администратор с таким ID не найден.", parse_mode='Markdown')
        except (IndexError, ValueError):
            bot.reply_to(message, "🚨 Пожалуйста, используйте команду в формате: `/removeadmin <user_id>`", parse_mode='Markdown')
    else:
        bot.reply_to(message, "🛑 У вас нет прав для выполнения этой команды.", parse_mode='Markdown')

@bot.message_handler(commands=['addfile'])
def initiate_file_addition(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🛑 У вас нет прав для выполнения этой команды.", parse_mode='Markdown')
        return

    admin_file_addition_state[message.from_user.id] = {'files': [], 'waiting_for_command': True}
    bot.reply_to(message, "📤 Отправьте мне файлы. Когда закончите, отправьте команду для этих файлов в формате: `/command ваша_команда`", parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    if user_id in admin_file_addition_state and admin_file_addition_state[user_id]['waiting_for_command']:
        current_time = time.time()
        last_reply_time = admin_file_addition_state[user_id].get('last_reply_time', 0)
        admin_file_addition_state[user_id]['files'].append(message.document.file_id)
        
        # Отправляем подтверждение не чаще, чем раз в 30 секунд
        if current_time - last_reply_time > 30:  # 30 секунд
            bot.reply_to(message, "📥 Файл получен. Отправьте еще, или укажите команду для доступа.", parse_mode='Markdown')
            admin_file_addition_state[user_id]['last_reply_time'] = current_time

@bot.message_handler(func=lambda message: message.text.startswith('/command '))
def finalize_file_addition(message):
    user_id = message.from_user.id
    if user_id in admin_file_addition_state and admin_file_addition_state[user_id]['waiting_for_command']:
        command = message.text.split('/command ', 1)[1].strip()
        if command:
            # Проверяем, существует ли уже такая команда
            if command_exists(command):  # Предполагается, что эта функция проверяет наличие команды в БД
                bot.reply_to(message, f"⚠️ Команда `{command}` уже существует. Пожалуйста, выберите другое имя команды.", parse_mode='Markdown')
                return

            file_ids = admin_file_addition_state[user_id]['files']
            if add_command_with_files(command, file_ids):
                bot.reply_to(message, f"✅ Все файлы добавлены с командой: `{command}`.\n"
                                      f"Вы можете получить файлы по ссылке: [{bot_info.username}](https://t.me/{bot_info.username}?start={command})", parse_mode='Markdown')
            else:
                bot.reply_to(message, "⚠️ Произошла ошибка при добавлении файлов.", parse_mode='Markdown')
            del admin_file_addition_state[user_id]
        else:
            bot.reply_to(message, "🚨 Пожалуйста, укажите команду после `/command`.", parse_mode='Markdown')
    else:
        bot.reply_to(message, "🔙 Сначала отправьте файлы.")

from telebot.types import InputMediaDocument

@bot.message_handler(commands=['removefile'])
def handle_remove_file(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🚫 У вас нет прав для выполнения этой команды.")
        return
    
    # Извлекаем текст команды из сообщения
    try:
        command_id = message.text.split(maxsplit=1)[1]
    except IndexError:
        bot.reply_to(message, "⚠ Пожалуйста, укажите команду для удаления в формате: /removefile <команда>")
        return
    
    # Пытаемся удалить файлы, связанные с этой командой
    if remove_file(command_id):
        bot.reply_to(message, f"✅ Файлы, связанные с командой `{command_id}`, были успешно удалены.", parse_mode='Markdown')
    else:
        bot.reply_to(message, f"⚠ Файлы для команды `{command_id}` не найдены.", parse_mode='Markdown')

# Словарь для хранения состояния капчи: {user_id: (captcha_value, file_ids)}
captcha_state = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_id = message.from_user.id

        # Обработка сообщений в чате капчи
        if message.chat.id == CAPTCHA_CHAT_ID:
            if user_id in captcha_state and message.text == captcha_state[user_id][0]:
                # Удаляем сообщение с капчей
                bot.delete_message(CAPTCHA_CHAT_ID, message.message_id)
                # Отправка файлов порциями
                send_files_in_chunks(user_id, captcha_state[user_id][1])
                # Очистка состояния капчи для пользователя
                del captcha_state[user_id]
                # Отправляем подтверждение пользователю
                bot.send_message(user_id, "✅ Ваши файлы успешно отправлены!", parse_mode='Markdown')
                return

        # Генерация и отправка капчи для запроса на файлы
        command_text = message.text.strip('/')
        file_ids = get_files_by_command(command_text)
        if file_ids:
            captcha = str(random.randint(1000, 9999))
            captcha_state[user_id] = (captcha, file_ids)
            bot.send_message(user_id, f"🔒 Для получения файлов введите капчу *{captcha}* в чате ", parse_mode='Markdown')
    
    except Exception as e:
        print(f"Возникла ошибка: {e}")

def handle_command(message, command):
    file_ids = get_files_by_command(command)
    if file_ids:
        captcha = str(random.randint(1000, 9999))
        captcha_state[message.from_user.id] = (captcha, file_ids)
        bot.send_message(message.from_user.id, f"🔒 Для получения файлов введите капчу *{captcha}* в чате ", parse_mode='Markdown')
    else:
        bot.reply_to(message, "⚠️ Команда не найдена. Пожалуйста, проверьте правильность ввода команды.", parse_mode='Markdown')

def send_files_in_chunks(user_id, file_ids, chunk_size=10, pause=1.5):
    for i in range(0, len(file_ids), chunk_size):
        chunk = file_ids[i:i+chunk_size]
        media_group = [telebot.types.InputMediaDocument(f) for f in chunk]
        bot.send_media_group(user_id, media_group)
        time.sleep(pause)  # Пауза между отправками для предотвращения спама


