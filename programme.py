import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def add_watermark(image_path, output_path, brand="Mionjo", color=(255, 255, 255, 128), font_size=40):
    # Ouvrir l'image
    image = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # Préparer le texte
    year = datetime.now().year
    watermark_text = f"© {year} {brand}"

    # Charger une police
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Windows
    except:
        font = ImageFont.load_default()  # Fallback

    draw = ImageDraw.Draw(txt_layer)
    width, height = image.size

    # Dimensions du texte
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Position bas-droit
    x, y = width - text_width - 10, height - text_height - 10
    draw.text((x, y), watermark_text, font=font, fill=color)

    # Fusionner
    watermarked = Image.alpha_composite(image, txt_layer)
    watermarked.convert("RGB").save(output_path, "JPEG")


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mionjo Copyright Tool")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Variables
        self.image_path = ""
        self.output_path = ""
        self.brand = tk.StringVar(value="Mionjo")
        self.font_size = tk.IntVar(value=40)
        self.color = (255, 255, 255, 128)

        # Widgets
        tk.Label(root, text="Texte de copyright :").pack(pady=5)
        tk.Entry(root, textvariable=self.brand).pack(pady=5)

        tk.Label(root, text="Taille de police :").pack(pady=5)
        tk.Entry(root, textvariable=self.font_size).pack(pady=5)

        tk.Button(root, text="Choisir couleur", command=self.choose_color).pack(pady=5)
        tk.Button(root, text="Sélectionner une image", command=self.load_image).pack(pady=5)
        tk.Button(root, text="Ajouter le watermark", command=self.process_image).pack(pady=15)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choisir une couleur")
        if color_code[0]:
            r, g, b = color_code[0]
            self.color = (int(r), int(g), int(b), 255)

    def load_image(self):
        filetypes = [("Images", "*.jpg *.jpeg *.png")]
        self.image_path = filedialog.askopenfilename(title="Choisir une image", filetypes=filetypes)
        if self.image_path:
            self.output_path = os.path.splitext(self.image_path)[0] + "_watermarked.jpg"
            messagebox.showinfo("Image chargée", f"Image sélectionnée : {self.image_path}")

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Erreur", "Veuillez choisir une image d'abord")
            return
        try:
            add_watermark(
                self.image_path,
                self.output_path,
                brand=self.brand.get(),
                color=self.color,
                font_size=self.font_size.get()
            )
            messagebox.showinfo("Succès", f"Image sauvegardée : {self.output_path}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
