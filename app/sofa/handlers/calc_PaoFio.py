from functools import lru_cache


@lru_cache(maxsize=5)
def calculation_PaoFio(pao2: str, fio2: str) -> str | int:
    """
    Функция для расчета дыхательной функции на основе полученных значений пао2 и fio2.

    Эта функция принимает два строковых параметра, представляющих значения парциального давления кислорода
    и фракции вдохновляемого кислорода. Производит расчет по формуле 100 * pao2 / fio2.
    Результат округляется до ближайшего целого числа.

    :param pao2: Строка, представляющая значение парциального давления кислорода (pao2).
    :param fio2: Строка, представляющая значение фракции вдохновляемого кислорода (fio2).

    :return: Возвращает целое число, которое соответствует результату расчета:
             - 0, если результат больше 401;
             - 1, если результат находится в диапазоне от 301 до 400;
             - 2, если результат находится в диапазоне от 200 до 300;
             - 3, если результат находится в диапазоне от 100 до 200;
             - 4, если результат 100 или меньше.
    """

    total = round((100 * float(pao2)) / float(fio2))

    if total > 401:
        return 0
    elif 301 < total <= 400:
        return 1
    elif 200 < total <= 300:
        return 2
    elif 100 < total <= 200:
        return 3
    elif total <= 100:
        return 4

# total = calculation_PaoFio('40', '30')
# print(total)

# if not pao2.isnumeric() or not fio2.isnumeric():
#     return f'<b>Ошибка, повторите еще раз!</b>'
