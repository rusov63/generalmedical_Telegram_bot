from functools import lru_cache


@lru_cache(maxsize=3)
def get_answer_age(user: str) -> int:
    """
    Извлекает числовое значение из строки, представляющей возраст,
    и возвращает его в виде целого числа.

    Параметры:
    - user (str): Строка, содержащая текст, из которого необходимо
      извлечь числовое значение.

    Параметры:
    - user (str): Строка, содержащая текст, из которого необходимо извлечь числовое значение возраст.

    Возвращает:
    - int: Целое число, представляющее извлеченное числовое значение возраст.
           Если в строке нет числа или оно находится вне диапазона 18-100, будет возвращено None.

    Кэширование: Функция использует декоратор @lru_cache(maxsize=3) для
    кэширования результатов. Это означает, что если функция вызывается с теми же аргументами,
    результат будет возвращен из кэша, что ускоряет выполнение и уменьшает количество вычислений.
    Максимальный размер кэша установлен на 3, что позволяет хранить результаты пяти последних
    уникальных вызовов функции.
    """

    if user.isdigit():
        if (18 <= int(user) <= 100):
            return int(user)
    return None

# print(get_answer_age('45'))  # Получили 45
# print(get_answer_age('fghvkf'))  # Получили пустую строку
# print(get_answer_age('-lklkl120'))  # Получили None
# print(get_answer_age('120'))  # Получили None
# print(get_answer_age.cache_info())  # CacheInfo(hits=0, misses=4, maxsize=6, currsize=4)



@lru_cache(maxsize=3)
def get_answer_creatinine(user: str) -> int:
    """
    Извлекает числовое значение креатинина из строки, переданной в качестве аргумента.

    Параметры:
    - user (str): Строка, содержащая текст, из которого необходимо извлечь числовое значение креатинина.

    Возвращает:
    - int: Целое число, представляющее извлеченное числовое значение креатинина.
           Если в строке нет числа или оно находится вне диапазона 0-1000, будет возвращено None.

    Кэширование:
    Функция использует декоратор '@lru_cache' для кэширования результатов.
    Это означает, что если функция вызывается с теми же аргументами,
    результат будет возвращен из кэша, что ускоряет выполнение и
    уменьшает количество вычислений. Максимальный размер кэша установлен
    на 3, что позволяет хранить результаты трех последних уникальных
    вызовов функции.
    """
    if user.isdigit():
        if 0 <= int(user) <= 1000:
            return int(user)
    return None
