import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity

def montar_sistema(mask, canal):
    h, w = canal.shape
    n = h * w
    A = lil_matrix((n, n))
    b = np.zeros(n)

    def idx(i, j): return i * w + j

    for i in range(h):
        for j in range(w):
            p = idx(i, j)
            if mask[i, j]:
                A[p, p] = 1
                b[p] = canal[i, j]
            else:
                A[p, p] = -4
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < h and 0 <= nj < w:
                        A[p, idx(ni, nj)] = 1
    return A.tocsr(), b

def reconstruir_canal(mask, canal):
    A, b = montar_sistema(mask, canal)
    x = spsolve(A, b)
    return x.reshape(canal.shape)

def reconstruir_imagem(img_danificada, mask):
    canais = []
    for c in range(3):
        canais.append(reconstruir_canal(mask, img_danificada[..., c]))
    return np.stack(canais, axis=-1)

def calcular_metricas(original, reconstruida):
    mse = mean_squared_error(original, reconstruida)
    psnr = peak_signal_noise_ratio(original, reconstruida, data_range=1)
    ssim = structural_similarity(original, reconstruida, channel_axis=-1, data_range=1)
    return mse, psnr, ssim
