
import random
import requests
import time
from datetime import datetime

# 🔑 توکن ربات ایتا
TOKEN = 'bot396241:2270f433-81b0-4bee-aaef-4ad13fd42933'

# آدرس API ربات
url = f'https://api.eitaa.me/bot{TOKEN}/'

def send_message(chat_id, text):
    params = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url + 'sendMessage', data=params)

resources = {
    "grammar": [
        "https://www.englishgrammar.org/",
        "https://learnenglish.britishcouncil.org/grammar",
        "https://www.grammarly.com/blog/",
        "https://americanenglishfile.com/grammar-bank"
    ],
    "vocabulary": [
        "https://www.vocabulary.com/",
        "https://learnenglish.britishcouncil.org/vocabulary",
        "https://www.merriam-webster.com/word-of-the-day",
        "https://americanenglishfile.com/vocabulary"
    ],
    "conversation": [
        "https://www.talkenglish.com/",
        "https://learnenglish.britishcouncil.org/speaking",
        "https://americanenglishfile.com/conversation-practice",
        "https://www.englishclub.com/speaking/"
    ]
}

exercises = {
    "grammar": [
        {"question": "I ___ to the park yesterday.", "answer": "went"},
        {"question": "She ___ a book right now.", "answer": "is reading"},
        {"question": "What is the past tense of 'eat'?", "answer": "ate"}
    ],
    "vocabulary": [
        {"question": "What is the synonym of 'happy'?", "answer": "joyful"},
        {"question": "What is the opposite of 'hot'?", "answer": "cold"},
        {"question": "Choose the correct word: 'She is very _____.'", "answer": "beautiful"}
    ],
    "conversation": [
        {"question": "How are you today?", "answer": "I'm fine, thank you."},
        {"question": "Where do you live?", "answer": "I live in Tehran."},
        {"question": "What is your favorite hobby?", "answer": "Reading"}
    ]
}

user_data = {}

def get_updates():
    try:
        response = requests.get(url + 'getUpdates')
        return response.json()
    except:
        return {}

def get_random_exercise(topic):
    return random.choice(exercises[topic])

def get_random_resource(topic):
    return random.choice(resources[topic])

def daily_challenge(chat_id):
    topic = random.choice(["grammar", "vocabulary", "conversation"])
    exercise = get_random_exercise(topic)
    today = str(datetime.now().date())

    if chat_id not in user_data:
        user_data[chat_id] = {
            "correct": 0,
            "wrong": 0,
            "points": 0,
            "level": "beginner",
            "challenges": []
        }

    user_data[chat_id]['current'] = exercise
    user_data[chat_id]['challenges'].append({"date": today, "topic": topic, "question": exercise['question']})

    send_message(chat_id, f"📘 چالش روز ({topic}):\n{exercise['question']}")

def send_resources(chat_id):
    if chat_id in user_data and 'current' in user_data[chat_id]:
        topic = None
        question = user_data[chat_id]['current']['question']
        for key in exercises:
            for item in exercises[key]:
                if item['question'] == question:
                    topic = key
        if topic:
            link = get_random_resource(topic)
            send_message(chat_id, f"📚 منبع پیشنهادی برای تقویت {topic}:\n{link}")
        else:
            send_message(chat_id, "موضوع تمرین شما مشخص نیست.")
    else:
        send_message(chat_id, "ابتدا یک تمرین یا چالش انجام دهید.")

def progress_report(chat_id):
    if chat_id in user_data:
        data = user_data[chat_id]
        msg = f"📊 گزارش پیشرفت:\n"
        msg += f"✅ پاسخ درست: {data['correct']}\n"
        msg += f"❌ پاسخ غلط: {data['wrong']}\n"
        msg += f"🏅 امتیاز: {data['points']}\n"
        msg += f"📈 سطح فعلی: {data['level']}\n"
        send_message(chat_id, msg)
    else:
        send_message(chat_id, "هنوز تمرینی انجام نداده‌اید.")

def process_messages():
    updates = get_updates()
    for update in updates.get('result', []):
        if 'message' not in update:
            continue

        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '').strip()

        if text == "/start":
            send_message(chat_id, "سلام! 🎉 به ربات زبان‌آموزی خوش آمدید.\nبرای شروع تمرین بنویس:\n📘 /dailychallenge\n📚 /resources\n📊 /progress")

        elif text == "/dailychallenge":
            daily_challenge(chat_id)

        elif text == "/resources":
            send_resources(chat_id)

        elif text == "/progress":
            progress_report(chat_id)

        elif chat_id in user_data and 'current' in user_data[chat_id]:
            expected = user_data[chat_id]['current']['answer'].lower()
            if text.lower() == expected:
                user_data[chat_id]['correct'] += 1
                user_data[chat_id]['points'] += 10
                send_message(chat_id, "✅ عالی! پاسخ درست بود.")
                if user_data[chat_id]['points'] > 50:
                    user_data[chat_id]['level'] = "intermediate"
                if user_data[chat_id]['points'] > 100:
                    user_data[chat_id]['level'] = "advanced"
            else:
                user_data[chat_id]['wrong'] += 1
                send_message(chat_id, f"❌ نه! پاسخ درست نبود.\nدوباره تلاش کن.")

def run_bot():
    while True:
        process_messages()
        time.sleep(1)

if __name__ == "__main__":
    run_bot()
