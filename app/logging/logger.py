import logging
import os
from logging.handlers import RotatingFileHandler

# Caminho para o arquivo de log
log_path = os.path.join(os.getcwd(), "app", "logging", "app.log")

# Criação do logger
logger = logging.getLogger("embrapa_api")
logger.setLevel(logging.DEBUG)

# Handler para arquivo com rotação de 1MB, mantendo 3 arquivos antigos
file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Formatação do log
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
file_handler.setFormatter(formatter)

# Adiciona o handler apenas uma vez
if not logger.hasHandlers():
    logger.addHandler(file_handler)
