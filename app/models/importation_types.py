from enum import Enum


class ImportTypeEnum(str, Enum):
    vinhos_de_mesa = "Vinhos de mesa"
    espumantes = "Espumantes"
    uvas_frescas = "Uvas frescas"
    uvas_passas = "Uvas passas"
    suco_de_uva = "Suco de uva"
