import os
import random
import numpy as np
from skimage import io, color, img_as_float

def carregar_imagens_aleatorias(pasta, n=10):
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    escolhidas = random.sample(arquivos, n)
    caminhos = [os.path.join(pasta, f) for f in escolhidas]
    return caminhos

def carregar_imagem_rgb(caminho):
    img = io.imread(caminho)
    img = img_as_float(img)
    if img.ndim == 2:
        img = color.gray2rgb(img)
    return img

def danificar_imagem(img, proporcao=0.2):
    h, w, _ = img.shape
    tipo_dano = random.choice(["esparso", "buracos"])

    if tipo_dano == "esparso":
        mask = np.random.rand(h, w) > proporcao

    else:
        mask = np.ones((h, w), dtype=bool)
        n_buracos = random.randint(1, 5)
        for _ in range(n_buracos):
            bh = random.randint(h // 10, h // 4)
            bw = random.randint(w // 10, w // 4)
            y = random.randint(0, h - bh)
            x = random.randint(0, w - bw)
            mask[y:y+bh, x:x+bw] = False

    img_danificada = img.copy()
    for c in range(3):
        img_danificada[..., c] *= mask

    return img_danificada, mask
