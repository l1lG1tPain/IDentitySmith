import json
from tkinter import messagebox
import os

class HistoryManager:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.history_file = "history.json"
        self.initialize_history_file()

    def initialize_history_file(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def save_to_history(self, type_, value):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            data.append({type_: value})

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            self.update_history_text(data)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения истории: {e}")
            print(e)  # Добавим вывод ошибки в консоль для отладки

    def update_history_text(self, data):
        self.ui_manager.history_text.delete(1.0, "end")
        for record in data:
            for key, value in record.items():
                self.ui_manager.history_text.insert("end", f"{key}: {value}\n")

    def clear_history_file(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        self.ui_manager.history_text.delete(1.0, "end")
