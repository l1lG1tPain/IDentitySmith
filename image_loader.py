from tkinter import messagebox
from PIL import Image, ImageTk

class ImageLoader:
    def load_image(self, image_path, size=None):
        try:
            image = Image.open(image_path)
            if size:
                image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки изображения: {e}")
            return None
