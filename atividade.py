import tkinter as tk 
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageOps

# Isso e pra gardar a imagem
imagem_original = None

# essa função e pra botar o efeito na imagem
def aplicar_efeito(imagem, efeito):
    if efeito == "Preto e Branco":
        # converti pra preto e branco (grayscale)
        return imagem.convert("L").convert("RGB")
    elif efeito == "Contorno":
        # efeito que destaca as bordas, tipo um desenho
        return imagem.filter(ImageFilter.CONTOUR)
    elif efeito == "Sépia":
        # efeito que deixa a imagem com aquele tom antigo, meio marrom
        sepia = imagem.convert("RGB")
        largura, altura = sepia.size
        pixels = sepia.load()
        for y in range(altura):
            for x in range(largura):
                r, g, b = pixels[x, y]
                # fórmula pra deixar o pixel com tom sépia
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                # atualiza pixel, garantindo que não vai passar de 255
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
        return sepia
    elif efeito == "Blur":
        # efeito que deixa tudo meio desfocado
        return imagem.filter(ImageFilter.BLUR)
    elif efeito == "Detalhe":
        # efeito detalhes
        return imagem.filter(ImageFilter.DETAIL)
    elif efeito == "Emboss":
        # efeito meio 3D
        return imagem.filter(ImageFilter.EMBOSS)
    elif efeito == "Inverter":
        # inverte as cores (tipo negativo)
        if imagem.mode == 'RGBA':
            r, g, b, a = imagem.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted_image = ImageOps.invert(rgb_image)
            r2, g2, b2 = inverted_image.split()
            return Image.merge('RGBA', (r2, g2, b2, a))
        elif imagem.mode in ['RGB', 'L']:
            return ImageOps.invert(imagem)
        else:
            return imagem  # se não der pra inverter, volta normal
    elif efeito == "Espelhar Horizontal":
        # espelha a imagem
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
        imagem_original = Image.open(caminho).resize((300, 300)) # tamanho da iamgem
        mostrar_imagem() 

# função que pega a imagem original e bota o efeito
def mostrar_imagem():
    global imagem_original
    if imagem_original:
        efeito = efeito_var.get()  # qual efeito o cara escolheu
        img_com_efeito = aplicar_efeito(imagem_original, efeito)  # bota efeito
        img_tk = ImageTk.PhotoImage(img_com_efeito)  # prepara pra mostrar no tkinter
        imagem_label.config(image=img_tk)  # troca a imagem que tá no label
        imagem_label.image = img_tk  # guarda pra não sumir a imagem


janela = tk.Tk()
janela.geometry("600x600")  
janela.title("Manipulação de imagens")  
janela.resizable(False, False)  

efeito_var = tk.StringVar(janela)
efeito_var.set("Sem efeito") 

# lista de opções de efeitos pro cara escolher
opcoes = ["Sem efeito", "Preto e Branco", "Contorno", "Sépia", "Blur", "Detalhe", "Emboss", "Inverter", "Espelhar Horizontal"]

# dropdown que mostra as opções, e chama mostrar_imagem sempre que muda
dropdown = tk.OptionMenu(janela, efeito_var, *opcoes, command=lambda _: mostrar_imagem())
dropdown.pack(pady=10) 

botao_abrir = tk.Button(janela, text="Abrir imagem", command=abrir_imagem)
botao_abrir.pack()

imagem_label = tk.Label(janela)
imagem_label.pack(pady=10)

janela.mainloop()
