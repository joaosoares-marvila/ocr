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


    caminho_bloco1 = os.path.join(pasta_bloco1,'completo.jpg')
    caminho_bloco2 = os.path.join(pasta_bloco2, 'completo.jpg')
    caminho_bloco3 = os.path.join(pasta_bloco3, 'completo.jpg')

    img = Image.open(caminho_img_original)

    box1 = (200,1635, 1450, 1880)
    bloco1 = img.crop(box1)
    #bloco1.show()
    bloco1.save(caminho_bloco1)

    box2 = (200, 1880, 1450, 2135)
    bloco2 = img.crop(box2)
    #bloco2.show()
    bloco2.save(caminho_bloco2)

    box3 = (200, 2135, 1450, 2400)
    bloco3 = img.crop(box3)
    #bloco3.show()
    bloco3.save(caminho_bloco3)

    return [pasta_bloco1, pasta_bloco2, pasta_bloco3]

def corta_blocos_em_coluna(pasta_bloco: str) -> None:

    caminho_bloco_completo = os.path.join(pasta_bloco, 'completo.jpg')

    caminho_cpf = os.path.join(pasta_bloco,'cpf.jpg')
    caminho_nome = os.path.join(pasta_bloco,'nome.jpg')
    caminho_valor1 = os.path.join(pasta_bloco,'valor1.jpg')
    caminho_valor2 = os.path.join(pasta_bloco,'valor2.jpg')
    caminho_valor3 = os.path.join(pasta_bloco,'valor3.jpg')
    
    
    img = Image.open(caminho_bloco_completo)

    box1 = (100, 0, 235, 310)
    cpf = img.crop(box1)
    #cpf.show()
    cpf.save(caminho_cpf)

    box2 = (240, 0, 533, 310)
    nome = img.crop(box2)
    #nome.show()
    nome.save(caminho_nome)

    box3 = (920, 0, 1045, 310)
    valor1 = img.crop(box3)
    #valor1.show()
    valor1.save(caminho_valor1)

    box4 = (1045, 0, 1137, 310)
    valor2 = img.crop(box4)
    #valor2.show()
    valor2.save(caminho_valor2)

    box5 = (1135, 0, 1250, 310)
    valor3 = img.crop(box5)
    #valor3.show()
    valor3.save(caminho_valor3)


def faz_leitura_bloco(pasta_bloco: str) -> None:
    
    arquivo_cpf = os.path.join(pasta_bloco, 'cpf.jpg')
    cpfs_bloco = le_imagem(img_path=arquivo_cpf)
    quantidade_cpfs = len(cpfs_bloco)

    arquivo_nome = os.path.join(pasta_bloco, 'nome.jpg')
    nomes_bloco = le_imagem(img_path=arquivo_nome)
    quantidade_nomes = len(nomes_bloco)

    arquivo_valor1 = os.path.join(pasta_bloco, 'valor1.jpg')
    valor1_bloco = le_imagem(img_path=arquivo_valor1)
    quantidade_valor1 = len(valor1_bloco)
    dif_valor1_cpf = quantidade_valor1 - quantidade_cpfs
    valor1_bloco = valor1_bloco[dif_valor1_cpf:]

    arquivo_valor2 = os.path.join(pasta_bloco, 'valor2.jpg')
    valor2_bloco = le_imagem(img_path=arquivo_valor2)
    quantidade_valor2 = len(valor2_bloco)
    dif_valor2_cpf = quantidade_valor2 - quantidade_cpfs
    valor2_bloco = valor2_bloco[dif_valor2_cpf:]

    arquivo_valor3 = os.path.join(pasta_bloco, 'valor3.jpg')
    valor3_bloco = le_imagem(img_path=arquivo_valor3)
    quantidade_valor3 = len(valor3_bloco)
    dif_valor3_cpf = quantidade_valor3 - quantidade_cpfs
    valor3_bloco = valor3_bloco[dif_valor3_cpf:]



    dados = []
    for i in range(len(cpfs_bloco)):
        dados.append({
            'cpf': cpfs_bloco[i],
            'nome': nomes_bloco[i],
            'valor_1': valor1_bloco[i],
            'valor_2': valor2_bloco[i],
            'valor_3': valor3_bloco[i]
        })

    return dados

def obtem_arquivos_jpg_diretorio(diretorio: str) -> list[str]:

    arquivos_dietorio = os.listdir(path=diretorio)
    
    lista_retorno = []

    for arquivo in arquivos_dietorio:
        if '.jpg' in arquivo:
            lista_retorno.append(arquivo)

    return lista_retorno


if __name__ == '__main__':

    wb_path = '/home/joao/Área de Trabalho/ocr/modelo2-v2/assets/planilhas/planilha-modelo2.xlsx'

    planilha_retorno = Planilha(
        caminho_arquivo=wb_path,
        nome_planilha='Principal',
        cabecalho=['cpf', 'nome','valor_1', 'valor_2', 'valor_3']
    )

    pasta_imgs = r'/home/joao/Área de Trabalho/ocr/modelo2-v2/assets/imgs'

    nomes_imgs = obtem_arquivos_jpg_diretorio(diretorio=pasta_imgs)
    
    for nome_img in nomes_imgs:

        pastas_blocos = corta_imagens_em_blocos(nome_img=nome_img, pasta_img=pasta_imgs)
        
        for pasta_bloco in pastas_blocos:
            corta_blocos_em_coluna(pasta_bloco=pasta_bloco)

            dados = faz_leitura_bloco(pasta_bloco=pasta_bloco)

            for registro in dados:

                planilha_retorno.adiciona_dado(
                    dados=registro
                )
