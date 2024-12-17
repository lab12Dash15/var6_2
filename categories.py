from enum import Enum, unique

@unique
class SortElement(Enum):
    ID = "Id"
    CATEGORY = "Категория"
    NAME = "Название"
    PRICE = "Цена"
    PRESENT = "Наличие"