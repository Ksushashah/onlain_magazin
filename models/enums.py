from enum import Enum
class StatusEnum(str,Enum):
    NEW = "Новый"
    IN_PROGRESS = "В процессе"
    DONE = "Выполнен"
    DRAFT = "Черновик"

class RatingEnum(str, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10    