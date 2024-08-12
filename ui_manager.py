import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from generator import Generator
from history_manager import HistoryManager
from image_loader import ImageLoader
import webbrowser
import os
import sys
import threading

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class UIManager:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("IDentitySmith")
        self.root.geometry("550x530")
        self.root.resizable(False, False)

        # Установка иконки окна
        try:
            self.root.iconbitmap(resource_path('image/IDentitySmith.ico'))  # Используем resource_path
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")

        self.generator = Generator()
        self.history_manager = HistoryManager(self)
        self.image_loader = ImageLoader()

        # Сохранение иконок в переменных экземпляра
        self.generate_icon = self.image_loader.load_image(resource_path("image/generate.png"), size=(24, 24))
        self.copy_icon = self.image_loader.load_image(resource_path("image/copy.png"), size=(24, 24))
        self.clear_icon = self.image_loader.load_image(resource_path("image/clear.png"), size=(24, 24))
        self.about_icon = self.image_loader.load_image(resource_path("image/IDentitySmith.png"), (150, 150))
        self.tg_icon = self.image_loader.load_image(resource_path("image/tg.png"), (25, 25))
        self.github_icon = self.image_loader.load_image(resource_path("image/github.png"), (25, 25))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Обработка закрытия окна
        self.setup_gui()

    def setup_gui(self):
        self.apply_styles()

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill=tk.BOTH)

        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text="Генерация")

        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text="Пароль")

        frame3 = ttk.Frame(notebook)
        notebook.add(frame3, text="История")

        frame4 = ttk.Frame(notebook)
        notebook.add(frame4, text="О программе")

        self.setup_generation_tab(frame1)
        self.setup_password_tab(frame2)
        self.setup_history_tab(frame3)
        self.setup_about_tab(frame4)

    def apply_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Roboto Slab", 12), padding=6, relief="flat", borderwidth=2)
        style.configure("TEntry", font=("Roboto Slab", 12), padding=6)
        style.configure("TLabel", font=("Roboto Slab", 14))
        style.configure("TRadiobutton", font=("Roboto Slab", 14))
        style.configure("TNotebook.Tab", font=("Roboto Slab", 14, "bold"), padding=[10, 10])

    def setup_generation_tab(self, frame):
        ttk.Label(frame, text="Генерация никнейма").pack(padx=5, pady=5)
        self.nickname_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
        self.nickname_entry.pack(padx=5, pady=5)

        nickname_frame = ttk.Frame(frame)
        nickname_frame.pack(padx=5, pady=5)

        ttk.Button(nickname_frame, text="Генерировать", image=self.generate_icon, compound=tk.LEFT,
                   command=self.generate_nickname).pack(side=tk.LEFT, padx=5)
        ttk.Button(nickname_frame, text="", image=self.copy_icon, command=self.copy_nickname).pack(side=tk.LEFT, padx=5)

        ttk.Label(frame, text="Генерация ФИО").pack(padx=5, pady=5)
        self.first_name_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
        self.first_name_entry.insert(0, "Имя")
        self.first_name_entry.pack(padx=5, pady=5)
        self.middle_name_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
        self.middle_name_entry.insert(0, "Отчество")
        self.middle_name_entry.pack(padx=5, pady=5)
        self.last_name_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
        self.last_name_entry.insert(0, "Фамилия")
        self.last_name_entry.pack(padx=5, pady=5)

        self.language_var = tk.StringVar(value="RU")
        ttk.Label(frame, text="Выбор языка").pack(padx=5, pady=5)
        ttk.Radiobutton(frame, text="Русский", variable=self.language_var, value="RU").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Английский", variable=self.language_var, value="EN").pack(anchor=tk.W)

        name_frame = ttk.Frame(frame)
        name_frame.pack(padx=5, pady=5)

        ttk.Button(name_frame, text="Генерировать", image=self.generate_icon, compound=tk.LEFT,
                   command=self.generate_name).pack(side=tk.LEFT, padx=5)
        ttk.Button(name_frame, text="", image=self.copy_icon, command=self.copy_name).pack(side=tk.LEFT, padx=5)

    def setup_password_tab(self, frame):
        ttk.Label(frame, text="Генерация пароля").pack(padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, width=30, font=("Roboto Slab", 12))
        self.password_entry.pack(padx=5, pady=5)

        password_frame = ttk.Frame(frame)
        password_frame.pack(padx=5, pady=5)

        ttk.Button(password_frame, text="Генерировать", image=self.generate_icon, compound=tk.LEFT,
                   command=self.generate_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(password_frame, text="", image=self.copy_icon, command=self.copy_password).pack(side=tk.LEFT, padx=5)

        # Измененные уровни сложности
        ttk.Label(frame, text="Выбор сложности пароля").pack(padx=5, pady=5)
        self.password_strength = tk.StringVar(value="medium")
        ttk.Radiobutton(frame, text="Простой", variable=self.password_strength, value="easy").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Умеренный", variable=self.password_strength, value="medium").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Сложный", variable=self.password_strength, value="hard").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Очень сложный", variable=self.password_strength, value="very_hard").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Максимально сложный", variable=self.password_strength, value="impossible").pack(anchor=tk.W)

        self.include_special = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Включить спецсимволы", variable=self.include_special).pack(anchor=tk.W)

    def setup_history_tab(self, frame):
        ttk.Label(frame, text="История").pack(padx=5, pady=5)
        self.history_text = tk.Text(frame, height=20, font=("Roboto Slab", 12))
        self.history_text.pack(padx=5, pady=5)

        ttk.Button(frame, text="Очистить историю", image=self.clear_icon, compound=tk.LEFT,
                   command=self.clear_history).pack(padx=5, pady=5)

    def setup_about_tab(self, frame):
        ttk.Label(frame, text="О программе:").pack(padx=5, pady=5)
        ttk.Label(frame, image=self.about_icon).pack(padx=5, pady=5)
        ttk.Label(frame, text="IDentitySmith v1.2.18", font=("Roboto Slab", 14)).pack(padx=5, pady=5)
        ttk.Label(frame, text="Разработчик: l1lG1tPain", font=("Roboto Slab", 12)).pack(padx=5, pady=5)
        ttk.Label(frame, text="Вы можете связаться со мной\n через следующие платформы:").pack(padx=5, pady=5)

        social_frame = ttk.Frame(frame)
        social_frame.pack(padx=5, pady=5)

        ttk.Button(social_frame, image=self.tg_icon,
                   command=lambda: webbrowser.open("https://t.me/cybersnitch")).pack(side=tk.LEFT, padx=5)
        ttk.Button(social_frame, image=self.github_icon,
                   command=lambda: webbrowser.open("https://github.com/l1lG1tPain/IDentitySmith")).pack(side=tk.LEFT,
                                                                                                      padx=5)

    def generate_nickname(self):
        # Создаем и запускаем поток для генерации никнейма
        threading.Thread(target=self._generate_nickname_in_thread).start()

    def _generate_nickname_in_thread(self):
        try:
            nick = self.generator.generate_nickname()
            self.nickname_entry.delete(0, tk.END)
            self.nickname_entry.insert(0, nick)
            self.history_manager.save_to_history('Никнейм', nick)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации никнейма: {e}")

    def generate_name(self):
        try:
            first_name, middle_name, last_name = self.generator.generate_name(self.language_var.get())
            self.first_name_entry.delete(0, tk.END)
            self.middle_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)

            self.first_name_entry.insert(0, first_name)
            self.middle_name_entry.insert(0, middle_name)
            self.last_name_entry.insert(0, last_name)

            self.history_manager.save_to_history('ФИО', f"{first_name} {middle_name} {last_name}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации ФИО: {e}")

    def generate_password(self):
        try:
            password = self.generator.generate_password(self.password_strength.get(), self.include_special.get())
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.history_manager.save_to_history('Пароль', password)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации пароля: {e}")

    def copy_nickname(self):
        if self.nickname_entry.get():
            self.generator.copy_to_clipboard(self.nickname_entry.get())
        else:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте никнейм")

    def copy_name(self):
        full_name = f"{self.first_name_entry.get()} {self.middle_name_entry.get()} {self.last_name_entry.get()}"
        if full_name.strip():
            self.generator.copy_to_clipboard(full_name)
        else:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ФИО")

    def copy_password(self):
        if self.password_entry.get():
            self.generator.copy_to_clipboard(self.password_entry.get())
        else:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте пароль")

    def clear_history(self):
        try:
            self.history_manager.clear_history_file()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка очистки истории: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()
