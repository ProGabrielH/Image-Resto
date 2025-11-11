import matplotlib.pyplot as plt
from imagens import carregar_imagens_aleatorias, carregar_imagem_rgb, danificar_imagem
from reconstrucao import reconstruir_imagem, calcular_metricas

if __name__ == "__main__":
    pasta = "imgdata"
    caminhos = carregar_imagens_aleatorias(pasta, n=10)

    for caminho in caminhos:
        img = carregar_imagem_rgb(caminho)
        img_danificada, mask = danificar_imagem(img, proporcao=0.2)
        img_reconstruida = reconstruir_imagem(img_danificada, mask)

        mse, psnr, ssim = calcular_metricas(img, img_reconstruida)

        fig, axs = plt.subplots(1, 3, figsize=(12, 4))
        axs[0].imshow(img)
        axs[0].set_title("Original")
        axs[1].imshow(img_danificada)
        axs[1].set_title("Danificada")
        axs[2].imshow(img_reconstruida)
        axs[2].set_title(f"Reconstruída\nMSE={mse:.4f}, PSNR={psnr:.2f}, SSIM={ssim:.3f}")

        for ax in axs:
            ax.axis("off")

        plt.tight_layout()
        plt.show()
