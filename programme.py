import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# ==== Couleurs Pantone ====
VERT = "#289728"   # Pantone 362C
BLEU = "#62B4E8"  # Pantone 2915C
MARRON = "#905A33" # Pantone 4635C

def add_watermark(image_path, output_path, brand="Mionjo", color=(255, 255, 255, 128), font_size=40):
    image = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))

    year = datetime.now().year
    watermark_text = f"© {year} {brand}"

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(txt_layer)
    width, height = image.size

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x, y = width - text_width - 10, height - text_height - 10
    draw.text((x, y), watermark_text, font=font, fill=color)

    watermarked = Image.alpha_composite(image, txt_layer)
    watermarked.convert("RGB").save(output_path, "JPEG")


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Mionjo Copyright Tool")
        self.root.geometry("520x500")
        self.root.configure(bg="#f7f9fc")
        self.root.resizable(False, False)

        self.image_paths = []
        self.output_dir = ""
        self.brand = tk.StringVar(value="Mionjo")
        self.font_size = tk.IntVar(value=40)
        self.color = (255, 255, 255, 128)

        # ==== TITRE ====
        title = tk.Label(root, text="Mionjo Copyright Tool",
                         font=("Helvetica", 16, "bold"),
                         bg=BLEU, fg="white", pady=10)
        title.pack(fill="x")

        # ==== SECTION PARAMÈTRES ====
        frame_params = tk.LabelFrame(root, text=" Paramètres du watermark ",
                                     bg="#f7f9fc", padx=10, pady=10, font=("Helvetica", 10, "bold"))
        frame_params.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_params, text="Texte de copyright :", bg="#f7f9fc").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_params, textvariable=self.brand, width=25).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frame_params, text="Taille de police :", bg="#f7f9fc").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_params, textvariable=self.font_size, width=10).grid(row=1, column=1, padx=5, pady=3, sticky="w")

        tk.Button(frame_params, text="🎨 Choisir couleur", command=self.choose_color,
                  bg=BLEU, fg="white", relief="flat").grid(row=2, column=0, columnspan=2, pady=8)

        # ==== SECTION FICHIERS ====
        frame_files = tk.LabelFrame(root, text=" Fichiers ", bg="#f7f9fc",
                                    padx=10, pady=10, font=("Helvetica", 10, "bold"))
        frame_files.pack(fill="x", padx=15, pady=10)

        tk.Button(frame_files, text="📂 Sélectionner plusieurs images", command=self.load_images,
                  bg=BLEU, fg="white", relief="flat").pack(fill="x", pady=5)

        self.label_images = tk.Label(frame_files, text="Aucune image sélectionnée", bg="#f7f9fc", fg="gray")
        self.label_images.pack()

        tk.Button(frame_files, text="📁 Choisir dossier de sortie", command=self.choose_output_dir,
                  bg=VERT, fg="white", relief="flat").pack(fill="x", pady=5)

        self.label_output = tk.Label(frame_files, text="Aucun dossier choisi", bg="#f7f9fc", fg="gray")
        self.label_output.pack()

        # ==== BOUTON ACTION ====
        frame_action = tk.Frame(root, bg="#f7f9fc")
        frame_action.pack(fill="x", side="bottom", pady=15)

        tk.Button(frame_action, text="🚀 Lancer le traitement",
                command=self.process_images,
                bg=MARRON, fg="white",
                font=("Helvetica", 12, "bold"),
                relief="flat", padx=15, pady=8).pack(pady=5)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choisir une couleur")
        if color_code[0]:
            r, g, b = color_code[0]
            self.color = (int(r), int(g), int(b), 255)

    def load_images(self):
        filetypes = [("Images", "*.jpg *.jpeg *.png")]
        self.image_paths = filedialog.askopenfilenames(title="Choisir des images", filetypes=filetypes)
        if self.image_paths:
            self.label_images.config(text=f"{len(self.image_paths)} images sélectionnées", fg="black")

    def choose_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Choisir le dossier de sortie")
        if self.output_dir:
            self.label_output.config(text=f"Dossier : {self.output_dir}", fg="black")

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

            messagebox.showinfo("Succès", f"{len(self.image_paths)} images traitées avec succès ✅")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
