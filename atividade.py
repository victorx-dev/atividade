import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageOps

# Guarda a imagem original
imagem_original = None

def aplicar_efeito(imagem, efeito):
    if efeito == "Preto e Branco":
        return imagem.convert("L").convert("RGB")
    elif efeito == "Contorno":
        return imagem.filter(ImageFilter.CONTOUR)
    elif efeito == "Sépia":
        sepia = imagem.convert("RGB")
        largura, altura = sepia.size
        pixels = sepia.load()
        for y in range(altura):
            for x in range(largura):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
        return sepia
    elif efeito == "Blur":
        return imagem.filter(ImageFilter.BLUR)
    elif efeito == "Detalhe":
        return imagem.filter(ImageFilter.DETAIL)
    elif efeito == "Emboss":
        return imagem.filter(ImageFilter.EMBOSS)
    elif efeito == "Inverter":
        if imagem.mode == 'RGBA':
            r, g, b, a = imagem.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted_image = ImageOps.invert(rgb_image)
            r2, g2, b2 = inverted_image.split()
            return Image.merge('RGBA', (r2, g2, b2, a))
        elif imagem.mode in ['RGB', 'L']:
            return ImageOps.invert(imagem)
        else:
            return imagem
    elif efeito == "Espelhar Horizontal":
        return ImageOps.mirror(imagem)
    else:
        return imagem

def abrir_imagem():
    global imagem_original
    caminho = filedialog.askopenfilename(
        title="Selecione a imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if caminho:
        imagem_original = Image.open(caminho).resize((300, 300))
        mostrar_imagem()

def mostrar_imagem():
    global imagem_original
    if imagem_original:
        efeito = efeito_var.get()
        img_com_efeito = aplicar_efeito(imagem_original, efeito)
        img_tk = ImageTk.PhotoImage(img_com_efeito)
        imagem_label.config(image=img_tk)
        imagem_label.image = img_tk

def salvar_imagem():
    if imagem_original:
        efeito = efeito_var.get()
        imagem_salvar = aplicar_efeito(imagem_original, efeito)
        caminho = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", ".png"), ("JPEG", ".jpg"), ("BMP", ".bmp"), ("GIF", ".gif")],
            title="Salvar imagem como"
        )
        if caminho:
            imagem_salvar.save(caminho)

# --- Interface com estilo ---

janela = tk.Tk()
janela.geometry("700x600")
janela.title("Manipulação de Imagens")
janela.configure(bg="#1e1e1e")
janela.resizable(False, False)

# Variável de controle de efeito
efeito_var = tk.StringVar(janela)
efeito_var.set("Sem efeito")

# Lista de efeitos
opcoes = ["Sem efeito", "Preto e Branco", "Contorno", "Sépia", "Blur", "Detalhe", "Emboss", "Inverter", "Espelhar Horizontal"]

# Frame principal de controle
frame_controles = tk.Frame(janela, bg="#1e1e1e")
frame_controles.pack(pady=20)

dropdown = tk.OptionMenu(frame_controles, efeito_var, *opcoes, command=lambda _: mostrar_imagem())
dropdown.config(bg="#444", fg="white", font=("Arial", 10), width=20, highlightthickness=0)
dropdown["menu"].config(bg="#444", fg="white", font=("Arial", 10))
dropdown.grid(row=0, column=0, padx=10)

botao_abrir = tk.Button(frame_controles, text="Abrir imagem", command=abrir_imagem,
                        bg="#007acc", fg="white", font=("Arial", 10), width=15)
botao_abrir.grid(row=0, column=1, padx=10)

botao_salvar = tk.Button(frame_controles, text="Salvar imagem", command=salvar_imagem,
                         bg="#28a745", fg="white", font=("Arial", 10), width=15)
botao_salvar.grid(row=0, column=2, padx=10)

# Label onde será exibida a imagem
imagem_label = tk.Label(janela, bg="#1e1e1e")
imagem_label.pack(pady=20)

janela.mainloop()
