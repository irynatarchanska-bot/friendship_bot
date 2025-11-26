import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 ТВОЙ ТОКЕН И ИМЯ БОТА
TOKEN = "7693727104:AAEMFmscssBNsORqWF4yBOV3S6m3-VR2Cqc"         # сюда вставь токен из BotFather
BOT_USERNAME = "WhatFriendship_test_bot"     # сюда имя бота без @, например: WhatFriendshiptestbot
OWNER_CHAT_ID = 7267765504               # твой chat_id (мы его уже знаем)

bot = telebot.TeleBot(TOKEN)

# 🖼 Картинки (можешь потом поменять на красивые)
START_IMAGE_URL = "https://telegram.org/img/t_logo.png"
QUESTION_IMAGE_URL = "https://telegram.org/img/t_logo.png"
DIPLOMA_IMAGE_URL = "https://telegram.org/img/t_logo.png"

# 📝 Вопросы теста
QUESTIONS = [
    {
        "text": "📅 В каком году ты родился/-лась?",
        "options": ["🎈 2008", "🎈 2009", "🎈 2010", "🎈 2011", "🎈 2012", "🎈 Раньше/позже"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "👏 Сколько у тебя братьев/сестёр?",
        "options": ["🗿 0", "💍 1", "✌️ 2", "🎀 3", "🧸 4", "👀 Больше 4"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "🐾 У тебя есть домашнее животное?",
        "options": ["🐶 Собака", "🐱 Кошка", "🐹 Хомяк", "🐢 Рептилия", "🐠 Рыбки", "🚫 Нет"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "📚 Какой предмет в школе тебе даётся лучше всего?",
        "options": ["📘 Английский", "📐 Математика", "📚 Языки", "🔬 Биология", "🧪 Химия", "🏃 Физкультура"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "📖 Как ты обычно готовишься к контрольной?",
        "options": ["📘 Учу заранее", "📕 В последний момент", "✏️ Списываю", "🤞 На удачу", "😅 Как получится", "🧘 Не переживаю"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "❓ Какой ты тип людей?",
        "options": ["👁 Реалист", "💭 Мечтатель", "✨ Оптимист", "⚫ Пессимист", "😎 По настроению", "🤷 Пока не знаю"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "💘 Влюблён(а) ли ты сейчас?",
        "options": ["💕 Да", "💔 Нет", "🤔 Не уверен(а)", "😶 Сложно сказать", "👀 Тайна", "😏 Возможно..."],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "🥤 Какой у тебя любимый напиток?",
        "options": ["🥤 Лимонад", "🧃 Сок", "🫖 Чай", "☕ Кофе", "🥛 Молоко", "💧 Вода"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "🏠 Как ты любишь отдыхать?",
        "options": ["🏠 Дома", "🌳 На природе", "🎮 Играю", "🎧 Музыка/видео", "👫 С друзьями", "🧳 Путешествую"],
        "image": QUESTION_IMAGE_URL,
    },
    {
        "text": "✨ Веришь ли ты в дружбу между девушкой и парнем?",
        "options": ["✨ Конечно", "✨ Да", "🤔 Не уверен(а)", "❌ Нет", "😏 Иногда", "👀 Зависит"],
        "image": QUESTION_IMAGE_URL,
    }
]

# 🧠 Память в ОЗУ
creator_state = {}    # user_id -> {"q_index": int}
creator_answers = {}  # user_id -> [int, ...]
quizzes = {}          # owner_id -> {"answers": [...], "name": str}
taker_state = {}      # chat_id -> {"owner_id": int, "q_index": int, "answers": []}


def make_options_keyboard(prefix, owner_id, q_index, options):
    markup = InlineKeyboardMarkup()
    row = []
    for idx, text in enumerate(options):
        if prefix == "c":
            data = f"c:{q_index}:{idx}"
        else:
            data = f"t:{owner_id}:{q_index}:{idx}"
        btn = InlineKeyboardButton(text, callback_data=data)
        row.append(btn)
        if len(row) == 2:
            markup.row(*row)
            row = []
    if row:
        markup.row(*row)
    return markup


def send_creator_question(user_id):
    state = creator_state.get(user_id)
    if not state:
        return
    q_index = state["q_index"]
    if q_index >= len(QUESTIONS):
        return
    q = QUESTIONS[q_index]
    text = f"Вопрос {q_index + 1}/{len(QUESTIONS)}:\n{q['text']}"
    kb = make_options_keyboard("c", None, q_index, q["options"])
    image_url = q.get("image")
    if image_url:
        bot.send_photo(user_id, photo=image_url, caption=text, reply_markup=kb)
    else:
        bot.send_message(user_id, text, reply_markup=kb)


def send_taker_question(chat_id):
    state = taker_state.get(chat_id)
    if not state:
        return
    q_index = state["q_index"]
    owner_id = state["owner_id"]
    if q_index >= len(QUESTIONS):
        return
    q = QUESTIONS[q_index]
    text = f"Вопрос {q_index + 1}/{len(QUESTIONS)}:\n{q['text']}"
    kb = make_options_keyboard("t", owner_id, q_index, q["options"])
    image_url = q.get("image")
    if image_url:
        bot.send_photo(chat_id, photo=image_url, caption=text, reply_markup=kb)
    else:
        bot.send_message(chat_id, text, reply_markup=kb)


@bot.message_handler(commands=['start'])
def start(message):
    parts = message.text.split()
    chat_id = message.chat.id

    # если пришли по ссылке с owner_id (друг проходит чужой тест)
    if len(parts) > 1:
        owner_id_str = parts[1]
        try:
            owner_id = int(owner_id_str)
        except ValueError:
            bot.send_message(chat_id, "Некорректная ссылка на тест.")
            return

        if owner_id not in quizzes:
            bot.send_message(chat_id, "Тест не найден или ещё не создан.")
            return

        quiz_owner = quizzes[owner_id]
        owner_name = quiz_owner["name"]

        taker_state[chat_id] = {
            "owner_id": owner_id,
            "q_index": 0,
            "answers": []
        }

        intro_text = (
            f"🙌 Привет!\n"
            f"Ты проходишь тест на дружбу про {owner_name}. "
            f"Отвечай честно — посмотрим, как хорошо ты его/её знаешь 😉"
        )

        bot.send_photo(chat_id, photo=START_IMAGE_URL, caption=intro_text)
        send_taker_question(chat_id)
        return

    # обычный /start — создание своего теста
    text = (
        "🙌 Привет!\n"
        "Здесь ты можешь создать свой тест, чтобы узнать, насколько хорошо тебя знают друзья "
        "и получить ДИПЛОМ ДРУЖБЫ! ❤️\n\n"
        "Просто нажми на кнопку ниже:"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✨ Создать свой тест", callback_data="create_start"))
    bot.send_photo(chat_id, photo=START_IMAGE_URL, caption=text, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    data = call.data
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # удаляем сообщение с вопросом, чтобы не засорять чат
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass

    # старт создания теста (создатель)
    if data == "create_start":
        creator_state[user_id] = {"q_index": 0}
        creator_answers[user_id] = [None] * len(QUESTIONS)
        quizzes.pop(user_id, None)
        bot.answer_callback_query(call.id)
        bot.send_message(
            chat_id,
            "📝 Сейчас ты будешь отвечать на вопросы про себя.\n"
            "Потом я дам ссылку, и друзья смогут пройти твой тест."
        )
        send_creator_question(user_id)
        return

    parts = data.split(":")

    # ответы создателя теста
    if parts[0] == "c":
        if len(parts) != 3:
            return
        q_index = int(parts[1])
        opt_index = int(parts[2])

        if user_id not in creator_state:
            bot.answer_callback_query(call.id, "Сначала начни создание теста.")
            return

        answers = creator_answers.get(user_id)
        if answers is None:
            return
        answers[q_index] = opt_index

        state = creator_state[user_id]
        state["q_index"] += 1
        bot.answer_callback_query(call.id)

        if state["q_index"] < len(QUESTIONS):
            send_creator_question(user_id)
        else:
            # создатель завершил свой тест
            owner_name = call.from_user.first_name or "Друг"
            quizzes[user_id] = {
                "answers": answers,
                "name": owner_name
            }
            creator_state.pop(user_id, None)

            # формируем список его ответов
            lines = ["📋 Твои ответы в твоём тесте:\n"]
            for i, q in enumerate(QUESTIONS):
                ai = answers[i]
                try:
                    answer_text = q["options"][ai]
                except Exception:
                    answer_text = "—"
                q_num = i + 1
                question = q["text"]
                lines.append(f"{q_num}. {question}\n▶ {answer_text}\n")

            answers_text = "\n".join(lines)

            # сообщение создателю + ссылка
            link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
            text = (
                "🎉 Поздравляю! Ты создал(а) свой тест.\n\n"
                f"📜 Имя в дипломе: *{owner_name}*\n\n"
                f"Твоя ссылка:\n{link}\n\n"
                "Отправь её друзьям и узнай, насколько хорошо они тебя знают 😉"
            )
            bot.send_message(chat_id, text, parse_mode="Markdown")
            bot.send_message(chat_id, answers_text)

            # те же ответы отправляем владельцу бота (тебе)
            try:
                user_tag = f"@{call.from_user.username}" if call.from_user.username else f"id:{call.from_user.id}"
                owner_text = (
                    "🔔 Кто-то создал новый тест!\n"
                    f"Автор: {user_tag}\n"
                    f"Имя в дипломе: {owner_name}\n\n"
                    f"{answers_text}"
                )
                bot.send_message(OWNER_CHAT_ID, owner_text)
            except Exception:
                pass

        return

    # ответы друга, который проходит чужой тест
    if parts[0] == "t":
        if len(parts) != 4:
            return
        owner_id = int(parts[1])
        q_index = int(parts[2])
        opt_index = int(parts[3])

        if chat_id not in taker_state:
            bot.answer_callback_query(call.id, "Сначала начни тест по ссылке.")
            return

        state = taker_state[chat_id]
        if state["owner_id"] != owner_id:
            bot.answer_callback_query(call.id, "Что-то пошло не так. Попробуй ещё раз.")
            return

        state["answers"].append(opt_index)
        state["q_index"] += 1
        bot.answer_callback_query(call.id)

        if state["q_index"] < len(QUESTIONS):
            send_taker_question(chat_id)
        else:
            quiz = quizzes.get(owner_id)
            if not quiz:
                bot.send_message(chat_id, "Тест больше не доступен.")
                return

            correct = quiz["answers"]
            owner_name = quiz["name"]
            given = state["answers"]

            # считаем процент совпадений
            total = min(len(correct), len(given))
            same = 0
            for i in range(total):
                if correct[i] == given[i]:
                    same += 1
            percent = round(same * 100 / len(correct))

            # список ответов этого друга
            lines = ["📋 Твои ответы:\n"]
            for i, q in enumerate(QUESTIONS):
                if i >= len(given):
                    break
                ai = given[i]
                try:
                    answer_text = q["options"][ai]
                except Exception:
                    answer_text = "—"
                q_num = i + 1
                question = q["text"]
                lines.append(f"{q_num}. {question}\n▶ {answer_text}\n")

            answers_text = "\n".join(lines)

            # диплом другу
            caption = (
                f"✅ Ты прошёл(а) тест про {owner_name}!\n\n"
                f"Совпадение ответов: *{percent}%* дружбы 😎\n\n"
                "Твои ответы отправлены ниже 👇"
            )
            bot.send_photo(chat_id, photo=DIPLOMA_IMAGE_URL, caption=caption, parse_mode="Markdown")
            bot.send_message(chat_id, answers_text)

            # эти же ответы — только владельцу бота (автор теста их не получает)
            try:
                user_tag = f"@{call.from_user.username}" if call.from_user.username else f"id:{call.from_user.id}"
                owner_text = (
                    "🔔 Кто-то прошёл чей-то тест!\n"
                    f"Про: {owner_name}\n"
                    f"От: {user_tag}\n\n"
                    f"{answers_text}\n"
                    f"Совпадение: {percent}%"
                )
                bot.send_message(OWNER_CHAT_ID, owner_text)
            except Exception:
                pass

            taker_state.pop(chat_id, None)
        return


print("Bot is running with images...")
bot.infinity_polling()

