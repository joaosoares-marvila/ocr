from PIL import Image
from paddleocr import PaddleOCR
from planilha import Planilha
import os
from loguru import logger


def le_imagem(img_path: str) -> dict:
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(img_path, cls=True)
    
    linhas = []
    for idx in range(len(result)):
        
        res = result[idx]

        for line in res:
            
            valor = line[1][0]

            if str(valor).strip().upper() in ['CPF', 'VALOR', 'TOTAL', 'CAMBIO']:
                continue

            linhas.append(valor)
    
    return linhas

def corta_imagens_em_blocos(pasta_img: str, nome_img: str) -> None:

    caminho_img_original = os.path.join(pasta_img, nome_img)

    pasta_img_blocos = nome_img.split('.')[0]
    pasta_cortados = os.path.join(pasta_img,pasta_img_blocos) 
    if not os.path.exists(pasta_cortados):
        os.mkdir(pasta_cortados)

    pasta_bloco1 = os.path.join(pasta_cortados, 'bloco1')
    pasta_bloco2 = os.path.join(pasta_cortados, 'bloco2')
    pasta_bloco3 = os.path.join(pasta_cortados, 'bloco3')

    if not os.path.exists(pasta_bloco1):
        os.mkdir(pasta_bloco1)
    if not os.path.exists(pasta_bloco2):
        os.mkdir(pasta_bloco2)
    if not os.path.exists(pasta_bloco3):
        os.mkdir(pasta_bloco3)

    caminho_bloco1 = os.path.join(pasta_bloco1,'completo.png')
    caminho_bloco2 = os.path.join(pasta_bloco2, 'completo.png')
    caminho_bloco3 = os.path.join(pasta_bloco3,'completo.png')

    img = Image.open(caminho_img_original)

    box1 = (25, 230, 450, 957)
    bloco1 = img.crop(box1)
    #bloco1.show()
    bloco1.save(caminho_bloco1)

    box2 = (25, 950, 450, 1657)
    bloco2 = img.crop(box2)
    #bloco2.show()
    bloco2.save(caminho_bloco2)

    box3 = (25, 1650, 450, 2100)
    bloco3 = img.crop(box3)
    #bloco3.show()
    bloco3.save(caminho_bloco3)

    return [pasta_bloco1, pasta_bloco2, pasta_bloco3]

def corta_blocos_em_coluna(pasta_bloco: str) -> None:

    caminho_bloco_completo = os.path.join(pasta_bloco, 'completo.png')

    caminho_cpf = os.path.join(pasta_bloco,'cpf.png')
    caminho_valor1 = os.path.join(pasta_bloco,'valor1.png')
    caminho_valor2 = os.path.join(pasta_bloco,'valor2.png')
    
    
    img = Image.open(caminho_bloco_completo)

    box1 = (0, 0, 123, 700)
    cpf = img.crop(box1)
    #cpf.show()
    cpf.save(caminho_cpf)

    box2 = (135, 0, 215, 700)
    valor1 = img.crop(box2)
    #valor1.show()
    valor1.save(caminho_valor1)

    box3 = (325, 0, 425, 700)
    valor2 = img.crop(box3)
    #valor2.show()
    valor2.save(caminho_valor2)

def faz_leitura_bloco(pasta_bloco: str) -> None:
    
    arquivo_cpf = os.path.join(pasta_bloco, 'cpf.png')
    cpfs_bloco = le_imagem(img_path=arquivo_cpf)
    

    arquivo_valor1 = os.path.join(pasta_bloco, 'valor1.png')
    valor1_bloco = le_imagem(img_path=arquivo_valor1)


    arquivo_valor2 = os.path.join(pasta_bloco, 'valor2.png')
    valor2_bloco = le_imagem(img_path=arquivo_valor2)

    dados = []
    for i in range(len(cpfs_bloco)):
        dados.append({
            'cpf': cpfs_bloco[i],
            'valor_1': valor1_bloco[i],
            'valor_2': valor2_bloco[i]
        })

    return dados

def obtem_arquivos_png_diretorio(diretorio: str) -> list[str]:

    arquivos_dietorio = os.listdir(path=diretorio)
    
    lista_retorno = []

    for arquivo in arquivos_dietorio:
        if '.png' in arquivo:
            lista_retorno.append(arquivo)

    return lista_retorno


if __name__ == '__main__':

    wb_path = '/home/joao/Área de Trabalho/ocr/modelo1/assets/planilhas/planilha-modelo1.xlsx'

    planilha_retorno = Planilha(
        caminho_arquivo=wb_path,
        nome_planilha='Principal',
        cabecalho=['cpf', 'valor_1', 'valor_2']
    )

    pasta_imgs = r'/home/joao/Área de Trabalho/ocr/modelo1/assets/imgs'

    nomes_imgs = obtem_arquivos_png_diretorio(diretorio=pasta_imgs)
    
    for nome_img in nomes_imgs:

        pastas_blocos = corta_imagens_em_blocos(nome_img=nome_img, pasta_img=pasta_imgs)
        
        for pasta_bloco in pastas_blocos:
            corta_blocos_em_coluna(pasta_bloco=pasta_bloco)

            dados = faz_leitura_bloco(pasta_bloco=pasta_bloco)

            for registro in dados:

                planilha_retorno.adiciona_dado(
                    dados=registro
                )
