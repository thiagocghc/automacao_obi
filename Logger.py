import os
import logging
import sys
from datetime import datetime

MESES = {
    '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril', '05': 'Maio', '06': 'Junho', 
    '07': 'Julho','08': 'Agosto', '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
}

# Configuração do Log
def configurar_logger():
    agora = datetime.now()
    ano = agora.strftime('%Y')
    nome_mes = MESES[agora.strftime('%m')]
    nome_arquivo = f"automacao_{agora.strftime('%Y-%m-%d')}.log"

    # Pega o nome do script em execução
    nome_script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    # Gera nome de arquivo de log dinâmico
    nome_arquivo = f"{nome_script}_{agora.strftime('%Y-%m-%d')}.log"

    pasta_logs = os.path.join('logs', ano, nome_mes)
    if not os.path.exists(pasta_logs):
        os.makedirs(pasta_logs, exist_ok=True)
    caminho_log = os.path.join(pasta_logs, nome_arquivo)

    if os.path.exists(caminho_log):
        with open(caminho_log, 'w', encoding='utf8') as f:
            pass

    formato_log = '%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%d/%m/%Y %H:%M:%S'

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Limpa Handlers antigos para evitar logs duplicados
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler para arquivo
    file_handler = logging.FileHandler(caminho_log, encoding='utf8')
    file_handler.setFormatter(logging.Formatter(formato_log, datefmt='%d/%m/%Y %H:%M:%S'))
    logger.addHandler(file_handler)

    # Handler para console (StreamHandler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(formato_log, datefmt=datefmt))
    logger.addHandler(console_handler)

    return logger