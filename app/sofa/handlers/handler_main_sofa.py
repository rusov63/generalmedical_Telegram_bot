from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from app.anesthetic_risk.keyboards.keyboard_hypotension import kb_hypotension
from app.sofa.handlers.calc_EyeVerbalMotor import (calculation_Eye_response, calculation_Verbal_response,
                                                   calculation_Motor_response, final_calculation_EyeVerbalMotor)
from app.sofa.handlers.calc_hypotension import calculate_hypotension
from app.sofa.handlers.calc_kidney import calculation_creatinin
from app.sofa.handlers.calc_liver import calculation_liver
from app.sofa.handlers.calc_platelet import calculation_platelet
from app.sofa.handlers.calc_respiratory import calculation_respiratory
from app.sofa.handlers.calc_PaoFio import calculation_PaoFio
from app.sofa.handlers.check_Correct_values import (check_correct_values_FioPao, check_correct_kb_respiratory,
                                                    check_correct_kb_platelet, check_correct_kb_liver,
                                                    check_correct_kb_creatinin, check_correct_kb_hypotension,
                                                    check_correct_kb_eye, check_correct_kb_verbal,
                                                    check_correct_kb_motor)
from app.sofa.handlers.result_calculating_functions import total_result_functions
from app.sofa.keyboards.inline_kb_sofa import inline_sofa
from app.sofa.keyboards.kb_creatinin import kb_creatinin
from app.sofa.keyboards.kb_eye import kb_eye
from app.sofa.keyboards.kb_liver import kb_liver
from app.sofa.keyboards.kb_motor import kb_motor
from app.sofa.keyboards.kb_platelet import kb_platelet
from app.sofa.keyboards.kb_respiratory import kb_respiratory
from app.sofa.keyboards.kb_verbal import kb_verbal


class Reg(StatesGroup):
    """
    Класс для создания состояний в контексте конечного автомата (FSM).
    Служит для сбора информации от пользователя о состоянии здоровья.

    Атрибуты состояния:
    pao2 (State): Парциальное давление кислорода в артериальной крови.
    fio2 (State): Оценка уровня кислорода в крови.
    respiratory (State): Респираторная поддержка.
    platelet (State): Оценка состояния тромбоцитов и коагуляции.
    liver (State): Оценка функции печени, включая уровень билирубина.
    creatinin_kidney (State): Оценка функции почек по уровню креатинина.
    hypotension (State): Оценка состояния гипотензии, пониженного артериального давления.

    Шкала комы Глазго:
    eye_response (State): Открывание глаз.
    verbal_response (State): Речевая реакция.
    motor_response (State): Двигательная реакция.
    """
    pao2 = State()  # Дыхание. Парциальное давление кислорода в артериальной крови.
    fio2 = State()  # Дыхание. Второй параметр, оценка уровня кислорода в крови.

    respiratory = State()  # Респираторная поддержка

    platelet = State()  # Тромбоциты. Коагуляция.
    liver = State()  # Печень. Билирубин.
    creatinin_kidney = State()  # Почка. Креатинин.
    hypotension = State()  # Гипотензия. Пониженное артериальное давление

    # Шкала комы Глазго
    eye_response = State()  # Открывание глаз
    verbal_response = State()  # Речевая реакция
    motor_response = State()  # Двигательная реакция


# Экземпляр класса Router, представляющий маршрутизатор для управления сетевыми соединениями.
sofa_router = Router()


@sofa_router.message(Command('sofa'))
async def start_command(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду '/sofa', инициируя сценарий оценки по шкале SOFA.

    Эта функция выполняет следующие действия:
    1. Очищает текущее состояние пользователя, чтобы сбросить сценарий заполнения.
    2. Информирует пользователя о выборе шкалы SOFA, которая используется для оценки прогноза смертности
       и степени органной недостаточности у пациентов в отделениях реанимации и интенсивной терапии (ОРИТ).
    3. Устанавливает состояние для ввода значения PaO₂ (парциальное давление кислорода в артериальной крови).
    4. Запрашивает у пользователя ввод значения PaO₂ в миллиметрах ртутного столба (мм рт. ст.).

    :param:
    - message (types.Message): Сообщение, содержащее команду от пользователя.
    - state (FSMContext): Контекст состояния для управления состоянием пользователя в сценарии.
    """
    await state.clear()  # автоматический сброс закрытие сценария заполнения.

    await message.answer(f'Выбрали: шкала SOFA (оценка прогноза смертности и степени органной недостаточности'
                         f' у пациентов ОРИТ)')

    await state.set_state(Reg.pao2)  # Установка состояния Reg.pao2.

    await message.answer(f'Введите PaO₂ (мм рт. ст.): ')


@sofa_router.callback_query(F.data == '/sofa')
async def start_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие на кнопку в интерфейсе и инициирует сценарий оценки по шкале SOFA.

    :param
    - callback (CallbackQuery): Объект обратного вызова, содержащий данные о нажатии кнопки.
    - state (FSMContext): Контекст состояния, используемый для управления состоянием пользователя.

    Описание работы функции:
    1. Очищает текущее состояние, сбрасывая сценарий заполнения.
    2. Отправляет пользователю сообщение с информацией о выбранной шкале SOFA,
       которая используется для оценки прогноза смертности и степени органной недостаточности у пациентов в ОРИТ.
    3. Отправляет ответ на событие обратного вызова, подтверждая выбор шкалы SOFA.
    4. Устанавливает состояние для следующего ввода (Reg.pao2).
    5. Запрашивает у пользователя ввод значения PaO₂ в миллиметрах ртутного столба.

    :return
    - None: Функция не возвращает значения, но отправляет сообщения пользователю.
    """
    await state.clear()  # автоматический сброс закрытие сценария заполнения.

    await callback.message.answer(f'Выбрали: шкала SOFA (оценка прогноза смертности и степени органной недостаточности'
                                  f' у пациентов ОРИТ)')
    await callback.answer(f'шкала SOFA')

    await state.set_state(Reg.pao2)  # Установка состояния Reg.pao2.

    await callback.message.answer(f'Введите PaO₂ (мм рт. ст.): ')


@sofa_router.message(F.text, Reg.pao2)
async def write_user_pao(message: types.Message, state: FSMContext):
    """
    Функция является обработчиком сообщений, который активируется,
    когда пользователь вводит значение PaO₂ в рамках взаимодействия с ботом.
    Проверяет корректность значений через функцию check_correct_values, если данные не корректны,
    выводит ошибку в виде сообщения пользователю телеграма.
    Запрашивает следующее значение FiO₂, продолжая процесс взаимодействия с пользователем в рамках шкалы SOFA.

    :param message: Объект сообщения, который содержит текст, введенный пользователем.
    :param state: Контекст состояния, который позволяет управлять состоянием пользователя в
    рамках конечного автомата (FSM).
    """

    # проверяем корректность введенных значений от пользователя
    user = check_correct_values_FioPao(message.text)
    if user is None:
        await message.reply(f'<b>Пожалуйста, введите корректное значение!</b>')
        return

    await state.update_data(pao2=message.text)  # сохраняет введенное пользователем значение PaO₂
    await state.set_state(Reg.fio2)  # Установка состояния Reg.fio2.

    await message.answer(f'Введите FiO₂ (мм рт. ст.): ')


@sofa_router.message(F.text, Reg.fio2)
async def write_user_fio(message: types.Message, state: FSMContext):
    """
    Обрабатывает сообщение от пользователя, запрашивая значение FiO₂ (фракция кислорода в дыхательных газах).

    Функция проверяет корректность введенного значения. Если значение некорректно,
    пользователю отправляется сообщение с просьбой ввести корректное значение.
    В случае успешной проверки, введенное значение сохраняется в состоянии,
    и устанавливается следующее состояние для запроса информации о респираторной поддержке.

    Параметры:
    - message (types.Message): Сообщение от пользователя, содержащее введенное значение FiO₂.
    - state (FSMContext): Контекст состояния, используемый для хранения данных между сообщениями.
    """

    # проверяем корректность введенных значений от пользователя
    user = check_correct_values_FioPao(message.text)
    if user is None:
        await message.reply(f'<b>Пожалуйста, введите корректное значение!</b>')
        return

    await state.update_data(fio2=message.text)  # Cохраняет введенное пользователем значение FiO₂
    await state.set_state(Reg.respiratory)  # Установка состояния Reg.respiratory.

    await message.answer(f'Требуется респираторная поддержка? ', reply_markup=kb_respiratory())


@sofa_router.message(F.text, Reg.respiratory)
async def write_user_fio(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_respiratory(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_respiratory())
        return

    await state.update_data(respiratory=message.text)  # Cохраняет введенное пользователем значение respiratory

    await state.set_state(Reg.platelet)  # Установка состояния Reg.platelet.
    
    await message.answer(f'Выберите уровень тромбоцитов (10⁹/мл): ', reply_markup=kb_platelet())


@sofa_router.message(F.text, Reg.platelet)
async def write_user_platelet(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_platelet(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_platelet())
        return

    await state.update_data(platelet=message.text)  # Сохраняет введенное пользователем значение platelet

    await state.set_state(Reg.liver)  # Установка состояния Reg.liver.

    await message.answer(f'Выберите билирубин сыворотки (мкмоль/л): ', reply_markup=kb_liver())


@sofa_router.message(F.text, Reg.liver)
async def write_user_liver(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_liver(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_liver())
        return

    await state.update_data(liver=message.text)  # Сохраняет введенное пользователем значение liver

    await state.set_state(Reg.creatinin_kidney)  # Установка состояния Reg.creatinin_kidney.

    await message.answer(f'Выберите креатинин (мкмоль/л) или диурез: ', reply_markup=kb_creatinin())


@sofa_router.message(F.text, Reg.creatinin_kidney)
async def write_user_hypotension(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_creatinin(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_creatinin())
        return

    await state.update_data(creatinin_kidney=message.text)  # Сохраняет введенное пользователем значение creat_kidney

    await state.set_state(Reg.hypotension)  # Установка состояния Reg.hypotension.

    await message.answer(f'Выберите уровень гипотензии или степень инотропной '
                         f'поддержки: ', reply_markup=kb_hypotension())


@sofa_router.message(F.text, Reg.hypotension)
async def write_user_eye(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_hypotension(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_hypotension())
        return

    await state.update_data(hypotension=message.text)  # Сохраняет введенное пользователем значение hypotension

    await state.set_state(Reg.eye_response)  # Установка состояния Reg.eye_response

    await message.answer(f'Для дальнейшего расчета требуется вычисление по шкале комы Глазго '
                         f'(взрослые и дети старше 4 лет)')
    await message.answer(f'Открывание глаз: ', reply_markup=kb_eye())


@sofa_router.message(F.text, Reg.eye_response)
async def write_user_eye(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_eye(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_eye())
        return

    await state.update_data(eye_response=message.text)  # Сохраняет введенное пользователем значение eye_response

    await state.set_state(Reg.verbal_response)  # Установка состояния Reg.verbal_response

    await message.answer(f'Речевая реакция: ', reply_markup=kb_verbal())


@sofa_router.message(F.text, Reg.verbal_response)
async def write_user_verbal(message: types.Message, state: FSMContext):

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_verbal(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_verbal())
        return

    await state.update_data(verbal_response=message.text)  # Сохраняет введенное пользователем значение verbal_response

    await state.set_state(Reg.motor_response)  # Установка состояния Reg.motor_response

    await message.answer(f'Двигательная реакция: ', reply_markup=kb_motor())


@sofa_router.message(F.text, Reg.motor_response)
async def write_user_motor(message: types.Message, state: FSMContext):
    """
    Обрабатывает сообщение от пользователя, сохраняет введенное значение
    для моторной реакции и выполняет расчеты на основе состояния.
    Проверяет на корректность введеных значений.

    Параметры:
    - message (types.Message): Сообщение, содержащее текст от пользователя.
    - state (FSMContext): Контекст состояния, используемый для хранения
      и получения данных о состоянии пользователя.

    Описание:
    Функция сохраняет текст сообщения в состоянии как 'motor_response'.
    Затем извлекает данные о состоянии, включая значения для
    различных медицинских показателей (pao2, fio2, respiratory,
    platelet, liver, creatinin_kidney, hypotension, eye_response,
    verbal_response). На основе этих данных выполняются расчеты
    для получения итогового значения, которое затем отправляется
    пользователю. После этого состояние очищается для подготовки
    к следующему взаимодействию.
    """

    # проверяем корректность введенных значений от пользователя
    user = check_correct_kb_motor(message.text)
    if user is None:
        await message.reply(f'<b>Выберите корректное значение из предложенного!</b>', reply_markup=kb_motor())
        return

    await state.update_data(motor_response=message.text)  # Сохраняет введенное пользователем значение motor_response

    data = await state.get_data()

    # получение значения Дыхание pao2, fio2
    total_PaoFio = calculation_PaoFio(data['pao2'], data['fio2'])

    # получение значения Респираторная поддержка respiratory
    total_respiratory = calculation_respiratory(data['respiratory'])

    # получение значения тромбоциты platelet
    total_platelet = calculation_platelet(data['platelet'])

    # получение значения Печень
    total_liver = calculation_liver(data['liver'])

    # получение значения Креатинин
    total_kidney = calculation_creatinin(data['creatinin_kidney'])

    # получение значения Гипотензия
    total_hypotension = calculate_hypotension(data['hypotension'])

    # Расчет Шкала комы Глазго:
    #     eye_response: Открывание глаз.
    #     verbal_response: Речевая реакция.
    #     motor_response: Двигательная реакция.
    total_EyeVerbalMotor = final_calculation_EyeVerbalMotor(calculation_Eye_response(data['eye_response']),
                                                 calculation_Verbal_response(data['verbal_response']),
                                                 calculation_Motor_response(data['motor_response']))

    # Финальный расчет, вывод результата
    final_number = total_result_functions(total_PaoFio, total_respiratory,
                                        total_platelet, total_liver,
                                        total_kidney, total_hypotension,
                                        total_EyeVerbalMotor)

    # Вывод результата пользователю
    await message.answer(f'{final_number}')

    # очистка состояния.
    await state.clear()

    # Меню: на стартовую страницу или вернуться назад
    await message.answer(f'Выберите действие: ', reply_markup=inline_sofa())

    # await message.answer(f'Дыхание = {total_PaoFio}, Респираторная = {total_respiratory}, '
    #                      f'тромбоциты = {total_platelet}, Печень = {total_liver}, '
    #                      f'креатинин = {total_kidney}, Гипотензия = {total_hypotension},'
    #                      f'Глазго = {total_EyeVerbalMotor}')