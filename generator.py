import random
import requests
from mimesis import Person
from mimesis.locales import Locale
import pyperclip
from tkinter import messagebox


class Generator:
    def __init__(self):
        self.person_ru = Person(Locale.RU)
        self.person_en = Person(Locale.EN)

    def fetch_nickname(self):
        url = "https://randomuser.me/api/"
        try:
            response = requests.get(url, timeout=5)  # Устанавливаем таймаут в 5 секунд
            response.raise_for_status()
            data = response.json()
            first_name = data['results'][0]['name']['first']
            last_name = data['results'][0]['name']['last']
            return f"{first_name}{last_name}{random.randint(100, 999)}"
        except (requests.RequestException, KeyError) as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении никнейма: {e}")
            return f"User{random.randint(1000, 9999)}"

    def generate_nickname(self):
        try:
            return self.fetch_nickname()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации никнейма: {e}")
            return "User"

    def generate_name(self, language):
        try:
            person = self.person_ru if language == "RU" else self.person_en
            first_name = person.first_name()
            middle_name = person.surname()
            last_name = person.last_name()
            return first_name, middle_name, last_name
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации ФИО: {e}")
            return "Имя", "Отчество", "Фамилия"

    def generate_password(self, strength, include_special):
        try:
            length_dict = {
                "easy": 7,
                "medium": 9,
                "hard": 14,
                "very_hard": 21,
                "impossible": 27
            }
            length = length_dict.get(strength, 27)
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            if include_special:
                chars += "!@#$%^&*"
            return ''.join(random.choices(chars, k=length))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации пароля: {e}")
            return ""

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
