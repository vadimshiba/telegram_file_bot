# Telegram Bot <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg" alt="Python 3.7+"/>


## :zap: Описание
Данный Telegram-бот, созданный на базе **PyTelegramBotAPI** и **SQLAlchemy**, позволяет:
- Управлять капчей в указанном чате
- Работать с базой данных SQLite для хранения и обработки информации
- Обеспечивать удобный доступ администраторов к настройкам

---

## :sparkles: Основные возможности
1. **Лёгкая установка**  
2. **Удобная система конфигурации**  
3. **Гибкая работа с базой данных** (SQLite + SQLAlchemy)  
4. **Простая расширяемость функционала**


---

## :rocket: Установка и запуск

### Шаг 1: Клонирование репозитория
```bash
git clone <URL_репозитория>
cd <папка_проекта>
```

### Шаг 2: Настройка виртуального окружения

# Создайте виртуальное окружение
```
python3 -m venv venv
```

# Активируйте виртуальное окружение (Linux/MacOS)
```
source venv/bin/activate
```

# Или для Windows
```
venv\Scripts\activate
```

# Установите зависимости
```
pip install -r requirements.txt
```

### Шаг 3: Настройка конфигурации
# Откройте файл config.py и заполните параметры:

```python
BOT_TOKEN = 'ваш_токен_бота'  # Токен вашего Telegram-бота
ADMIN_IDS = [ваш_id]  # Список ID администраторов
CAPTCHA_CHAT_ID = ваш_id_чата  # ID чата для капчи
```

### Шаг 4: Запуск бота

# Создайте сессию screen
```
screen -S bot_session
```

# Запустите бота
```
python bot.py
```

# Выйдите из сессии screen
Ctrl+A, затем D

# Чтобы вернуться к сессии:
```
screen -r bot_session
```

# Используемые технологии
- PyTelegramBotAPI – взаимодействие с Telegram Bot API.
- SQLAlchemy – работа с базой данных SQLite.
