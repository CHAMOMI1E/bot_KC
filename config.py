from dotenv import load_dotenv
import os

# Загрузить переменные из файла .env в переменные окружения
load_dotenv()


DB_TOKEN = os.getenv('DB_TOKEN')
TOKEN_TEST = os.getenv('TOKEN')
