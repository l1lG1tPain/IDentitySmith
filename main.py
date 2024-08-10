import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import requests
import json
from mimesis import Person
from mimesis.locales import Locale
import pyperclip
from ttkthemes import ThemedTk
import webbrowser

# Инициализация библиотек для генерации ФИО
person_ru = Person(Locale.RU)
person_en = Person(Locale.EN)

# API для генерации оригинальных никнеймов
def fetch_nickname():
    url = "https://randomuser.me/api/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        first_name = data['results'][0]['name']['first']
        last_name = data['results'][0]['name']['last']
        return f"{first_name}{last_name}{random.randint(100, 999)}"
    except (requests.RequestException, KeyError) as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении никнейма: {e}")
        return f"User{random.randint(1000, 9999)}"

# Функции генерации
def generate_nickname():
    try:
        nick = fetch_nickname()
        nickname_entry.delete(0, tk.END)
        nickname_entry.insert(0, nick)
        save_to_history('Никнейм', nick)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка генерации никнейма: {e}")

def generate_name():
    try:
        person = person_ru if language_var.get() == "RU" else person_en
        first_name = person.first_name()
        middle_name = person.surname()
        last_name = person.last_name()

        first_name_entry.delete(0, tk.END)
        middle_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)

        first_name_entry.insert(0, first_name)
        middle_name_entry.insert(0, middle_name)
        last_name_entry.insert(0, last_name)

        save_to_history('ФИО', f"{first_name} {middle_name} {last_name}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка генерации ФИО: {e}")

def generate_password():
    try:
        length_dict = {
            "easy": 7,
            "medium": 9,
            "hard": 14,
            "mega": 21,
            "impossible": 27
        }
        length = length_dict.get(password_strength.get(), 27)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if include_special.get():
            chars += "!@#$%^&*"
        password = ''.join(random.choices(chars, k=length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        save_to_history('Пароль', password)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка генерации пароля: {e}")

def save_to_history(type_, value):
    try:
        history_text.insert(tk.END, f"{type_}: {value}\n")
        with open("history.json", "a", encoding="utf-8") as f:
            json.dump({type_: value}, f, ensure_ascii=False)
            f.write('\n')
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения истории: {e}")

def copy_nickname():
    if nickname_entry.get():
        pyperclip.copy(nickname_entry.get())
    else:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте никнейм")

def copy_name():
    full_name = f"{first_name_entry.get()} {middle_name_entry.get()} {last_name_entry.get()}"
    if full_name.strip():
        pyperclip.copy(full_name)
    else:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ФИО")

def copy_password():
    if password_entry.get():
        pyperclip.copy(password_entry.get())
    else:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте пароль")

def clear_history():
    try:
        history_text.delete(1.0, tk.END)
        with open("history.json", "w", encoding="utf-8") as f:
            f.truncate()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка очистки истории: {e}")

def load_image(image_path, size=None):
    try:
        image = Image.open(image_path)
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки изображения: {e}")
        return None

# Интерфейс
def setup_gui():
    global root
    root = ThemedTk(theme="arc")
    root.title("IDentitySmith")
    root.geometry("550x530")
    root.resizable(False, False)

    try:
        root.iconbitmap("image/IDentitySmith.ico")
    except Exception as e:
        print(f"Не удалось загрузить иконку: {e}")

    # Загрузка иконок
    generate_icon = load_image("image/generate.png")
    copy_icon = load_image("image/copy.png")
    clear_icon = load_image("image/clear.png")
    about_icon = load_image("image/IDentitySmith.png", (150, 150))
    tg_icon = load_image("image/tg.png", (25, 25))
    github_icon = load_image("image/github.png", (25, 25))

    apply_styles()

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=tk.BOTH)

    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text="Генерация")

    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text="Пароль")

    frame3 = ttk.Frame(notebook)
    notebook.add(frame3, text="История")

    frame4 = ttk.Frame(notebook)
    notebook.add(frame4, text="О программе")

    setup_generation_tab(frame1, generate_icon, copy_icon)
    setup_password_tab(frame2, generate_icon, copy_icon)
    setup_history_tab(frame3, clear_icon)
    setup_about_tab(frame4, about_icon, tg_icon, github_icon)

    root.mainloop()

def apply_styles():
    style = ttk.Style()
    style.configure("TButton", font=("Roboto Slab", 12), padding=6, relief="flat", borderwidth=2)
    style.configure("TEntry", font=("Roboto Slab", 12), padding=6)
    style.configure("TLabel", font=("Roboto Slab", 14))
    style.configure("TRadiobutton", font=("Roboto Slab", 14))
    style.configure("TNotebook.Tab", font=("Roboto Slab", 14, "bold"), padding=[10, 10])

def setup_generation_tab(frame, generate_icon, copy_icon):
    ttk.Label(frame, text="Генерация никнейма").pack(padx=5, pady=5)
    global nickname_entry
    nickname_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
    nickname_entry.pack(padx=5, pady=5)

    nickname_frame = ttk.Frame(frame)
    nickname_frame.pack(padx=5, pady=5)

    ttk.Button(nickname_frame, text="Генерировать", image=generate_icon, compound=tk.LEFT, command=generate_nickname).pack(side=tk.LEFT, padx=5)
    ttk.Button(nickname_frame, text="", image=copy_icon, command=copy_nickname).pack(side=tk.LEFT, padx=5)

    ttk.Label(frame, text="Генерация ФИО").pack(padx=5, pady=5)
    global first_name_entry, middle_name_entry, last_name_entry
    first_name_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
    first_name_entry.insert(0, "Имя")
    first_name_entry.pack(padx=5, pady=5)
    middle_name_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
    middle_name_entry.insert(0, "Отчество")
    middle_name_entry.pack(padx=5, pady=5)
    last_name_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
    last_name_entry.insert(0, "Фамилия")
    last_name_entry.pack(padx=5, pady=5)

    global language_var
    language_var = tk.StringVar(value="RU")
    ttk.Label(frame, text="Выбор языка").pack(padx=5, pady=5)
    ttk.Radiobutton(frame, text="Русский", variable=language_var, value="RU").pack(anchor=tk.W)
    ttk.Radiobutton(frame, text="Английский", variable=language_var, value="EN").pack(anchor=tk.W)

    name_frame = ttk.Frame(frame)
    name_frame.pack(padx=5, pady=5)

    ttk.Button(name_frame, text="Генерировать", image=generate_icon, compound=tk.LEFT, command=generate_name).pack(side=tk.LEFT, padx=5)
    ttk.Button(name_frame, text="", image=copy_icon, command=copy_name).pack(side=tk.LEFT, padx=5)

def setup_password_tab(frame, generate_icon, copy_icon):
    ttk.Label(frame, text="Генерация пароля").pack(padx=5, pady=5)
    global password_entry
    password_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
    password_entry.pack(padx=5, pady=5)

    password_frame = ttk.Frame(frame)
    password_frame.pack(padx=5, pady=5)

    ttk.Button(password_frame, text="Генерировать", image=generate_icon, compound=tk.LEFT, command=generate_password).pack(side=tk.LEFT, padx=5)
    ttk.Button(password_frame, text="", image=copy_icon, command=copy_password).pack(side=tk.LEFT, padx=5)

    global password_strength
    password_strength = tk.StringVar(value="hard")
    ttk.Label(frame, text="Сложность пароля").pack(padx=5, pady=5)
    ttk.Radiobutton(frame, text="Легкий", variable=password_strength, value="easy").pack(anchor=tk.W)
    ttk.Radiobutton(frame, text="Средний", variable=password_strength, value="medium").pack(anchor=tk.W)
    ttk.Radiobutton(frame, text="Сложный", variable=password_strength, value="hard").pack(anchor=tk.W)
    ttk.Radiobutton(frame, text="Очень сложный", variable=password_strength, value="mega").pack(anchor=tk.W)
    ttk.Radiobutton(frame, text="Невозможный", variable=password_strength, value="impossible").pack(anchor=tk.W)

    global include_special
    include_special = tk.BooleanVar(value=True)
    ttk.Checkbutton(frame, text="Использовать специальные символы", variable=include_special).pack(anchor=tk.W)

def setup_history_tab(frame, clear_icon):
    ttk.Label(frame, text="История").pack(padx=5, pady=5)
    global history_text
    history_text = tk.Text(frame, width=65, height=15, font=("Roboto Slab", 12))
    history_text.pack(padx=5, pady=5)

    ttk.Button(frame, text="Очистить историю", image=clear_icon, compound=tk.LEFT, command=clear_history).pack(padx=5, pady=5)

def setup_about_tab(frame, about_icon, tg_icon, github_icon):
    ttk.Label(frame, text="О программе").pack(padx=5, pady=5)
    ttk.Label(frame, image=about_icon).pack(padx=5, pady=5)
    ttk.Label(frame, text="IDentitySmith v1.2.17", font=("Roboto Slab", 14)).pack(padx=5, pady=5)
    ttk.Label(frame, text="Разработчик: l1lG1tPain", font=("Roboto Slab", 12)).pack(padx=5, pady=5)
    ttk.Label(frame, text="Вы можете связаться со мной через следующие платформы:").pack(padx=5, pady=5)

    social_frame = ttk.Frame(frame)
    social_frame.pack(padx=5, pady=5)

    ttk.Button(social_frame, image=tg_icon, command=lambda: webbrowser.open("https://t.me/YourTelegramHandle")).pack(side=tk.LEFT, padx=5)
    ttk.Button(social_frame, image=github_icon, command=lambda: webbrowser.open("https://github.com/YourGitHubHandle")).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    setup_gui()
