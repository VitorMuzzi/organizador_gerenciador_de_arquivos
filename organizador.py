import os
import shutil
import re
import argparse
import time
import logging
import json
import sys
from send2trash import send2trash

def carregar_configuracao():
    caminho_config = 'config.json'
    if not os.path.exists(caminho_config):
        print(f"Erro: O arquivo '{caminho_config}' não foi encontrado na pasta atual.")
        sys.exit(1)
        
    with open(caminho_config, 'r', encoding='utf-8') as arquivo_json:
        return json.load(arquivo_json)

config = carregar_configuracao()
PASTA_DOWNLOADS = config['pasta_downloads']
TIPOS_DE_ARQUIVOS = config['tipos_de_arquivos']

logging.basicConfig(
    filename=os.path.join(PASTA_DOWNLOADS, 'historico_organizacao.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def organizar_arquivos():
    padrao_duplicata = re.compile(r"^(.*?) \(\d+\)(\.[a-zA-Z0-9]+)$")
    arquivos_movidos = 0

    for arquivo in os.listdir(PASTA_DOWNLOADS):
        caminho_completo = os.path.join(PASTA_DOWNLOADS, arquivo)
        
        if not os.path.exists(caminho_completo):
            continue
            
        if os.path.isdir(caminho_completo):
            continue
            
        if arquivo == 'historico_organizacao.log':
            continue

        match = padrao_duplicata.match(arquivo)
        if match:
            nome_base = match.group(1)
            extensao_arq = match.group(2)
            nome_original = f"{nome_base}{extensao_arq}"
            
            pasta_destino_correta = "Outros"
            for pasta, exts in TIPOS_DE_ARQUIVOS.items():
                if extensao_arq.lower() in exts:
                    pasta_destino_correta = pasta
                    break
            
            caminho_antigo_solto = os.path.join(PASTA_DOWNLOADS, nome_original)
            caminho_antigo_organizado = os.path.join(PASTA_DOWNLOADS, pasta_destino_correta, nome_original)

            arquivo_antigo_deletado = False
            
            if os.path.exists(caminho_antigo_solto):
                send2trash(caminho_antigo_solto)
                arquivo_antigo_deletado = True
            elif os.path.exists(caminho_antigo_organizado):
                send2trash(caminho_antigo_organizado)
                arquivo_antigo_deletado = True

            if arquivo_antigo_deletado:
                novo_caminho_base = os.path.join(PASTA_DOWNLOADS, nome_original)
                try:
                    os.rename(caminho_completo, novo_caminho_base)
                    arquivo = nome_original
                    caminho_completo = novo_caminho_base
                    logging.info(f"[Substituição] '{nome_original}' antigo foi para a lixeira. Novo assumiu o lugar.")
                except FileExistsError:
                    pass

        _, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()
        
        pasta_destino = "Outros"
        for pasta, extensoes_validas in TIPOS_DE_ARQUIVOS.items():
            if extensao in extensoes_validas:
                pasta_destino = pasta
                break
                
        caminho_pasta_destino = os.path.join(PASTA_DOWNLOADS, pasta_destino)
        
        if not os.path.exists(caminho_pasta_destino):
            os.makedirs(caminho_pasta_destino)
        
        caminho_final = os.path.join(caminho_pasta_destino, arquivo)
        
        try:
            shutil.move(caminho_completo, caminho_final)
            logging.info(f"Movido: {arquivo} -> {pasta_destino}")
            print(f"Movido: {arquivo} -> {pasta_destino}")
            arquivos_movidos += 1
        except shutil.Error:
            logging.warning(f"Conflito: O arquivo {arquivo} já existe em {pasta_destino}.")
            
    return arquivos_movidos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organizador de Downloads")
    parser.add_argument("--auto", action="store_true", help="Ativa o modo de monitoramento contínuo")
    args = parser.parse_args()

    if args.auto:
        print("Modo automático ativado. Pressione Ctrl+C para parar.")
        logging.info("--- Iniciando modo automático ---")
        try:
            while True:
                movidos = organizar_arquivos()
                if movidos > 0:
                    print(f"[{time.strftime('%H:%M:%S')}] {movidos} arquivo(s) organizado(s). Aguardando...")
                time.sleep(60) 
        except KeyboardInterrupt:
            print("\nModo automático encerrado pelo usuário.")
            logging.info("--- Modo automático encerrado ---")
    else:
        print("Executando organização única...")
        logging.info("--- Execução manual iniciada ---")
        organizar_arquivos()
        print("Organização concluída! Verifique o log para detalhes.")