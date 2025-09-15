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
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        # Variables
        self.image_paths = []   # Liste des images
        self.output_dir = ""    # Dossier de sortie
        self.brand = tk.StringVar(value="Mionjo")
        self.font_size = tk.IntVar(value=40)
        self.color = (255, 255, 255, 128)

        # Widgets
        tk.Label(root, text="Texte de copyright :").pack(pady=5)
        tk.Entry(root, textvariable=self.brand).pack(pady=5)

        tk.Label(root, text="Taille de police :").pack(pady=5)
        tk.Entry(root, textvariable=self.font_size).pack(pady=5)

        tk.Button(root, text="Choisir couleur", command=self.choose_color).pack(pady=5)
        tk.Button(root, text="Sélectionner plusieurs images", command=self.load_images).pack(pady=5)
        tk.Button(root, text="Choisir dossier de sortie", command=self.choose_output_dir).pack(pady=5)
        tk.Button(root, text="Lancer le traitement", command=self.process_images).pack(pady=15)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choisir une couleur")
        if color_code[0]:
            r, g, b = color_code[0]
            self.color = (int(r), int(g), int(b), 255)

    def load_images(self):
        filetypes = [("Images", "*.jpg *.jpeg *.png")]
        self.image_paths = filedialog.askopenfilenames(title="Choisir des images", filetypes=filetypes)
        if self.image_paths:
            messagebox.showinfo("Images chargées", f"{len(self.image_paths)} images sélectionnées")

    def choose_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Choisir le dossier de sortie")
        if self.output_dir:
            messagebox.showinfo("Dossier choisi", f"Dossier de sortie : {self.output_dir}")

    def process_images(self):
        if not self.image_paths:
            messagebox.showerror("Erreur", "Veuillez sélectionner des images d'abord")
            return
        if not self.output_dir:
            messagebox.showerror("Erreur", "Veuillez choisir un dossier de sortie")
            return

        try:
            for img_path in self.image_paths:
                filename = os.path.basename(img_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(self.output_dir, f"{name}.jpg")

                add_watermark(
                    img_path,
                    output_path,
                    brand=self.brand.get(),
                    color=self.color,
                    font_size=self.font_size.get()
                )

            messagebox.showinfo("Succès", f"{len(self.image_paths)} images traitées avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
