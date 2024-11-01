from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Для сессий

# Вопросы для теста по уровням сложности
questions_junior = [
    {"question": "Что делает функция len()?", "options": ["Находит длину объекта", "Изменяет список", "Очищает строку"], "answer": "Находит длину объекта"},
    {"question": "Какой тип данных возвращает input()?", "options": ["int", "str", "bool"], "answer": "str"},
    {"question": "Какой оператор используется для возведения в степень?", "options": ["^", "**", "//"], "answer": "**"},
    {"question": "Как объявить функцию в Python?", "options": ["function myFunction()", "def myFunction()", "func myFunction()"], "answer": "def myFunction()"},
    {"question": "Какой метод используется для добавления элемента в конец списка?", "options": ["append()", "add()", "push()"], "answer": "append()"},
    {"question": "Какой оператор используется для деления с округлением вниз?", "options": ["/", "//", "%"], "answer": "//"},
    {"question": "Что делает оператор '==' в Python?", "options": ["Присваивает значение", "Проверяет равенство", "Сравнивает по ссылке"], "answer": "Проверяет равенство"},
    {"question": "Какой тип данных подходит для хранения 'True' или 'False'?", "options": ["int", "str", "bool"], "answer": "bool"},
    {"question": "Какой метод используется для преобразования строки в нижний регистр?", "options": ["lower()", "down()", "tolower()"], "answer": "lower()"},
    {"question": "Как импортировать библиотеку math?", "options": ["import mathlib", "include math", "import math"], "answer": "import math"}
]

questions_middle = [
    {"question": "Что делает метод items() у словаря?", "options": ["Возвращает ключи", "Возвращает значения", "Возвращает пары ключ-значение"], "answer": "Возвращает пары ключ-значение"},
    {"question": "Сколько библиотек можно импортировать в один проект?", "options": ["Не более 10", "Неограниченное количество", "Не более 23"], "answer": "Неограниченное количество"},
    {"question": "Какая библиотека отвечает за время?", "options": ["time", "Time", "clock"], "answer": "time"},
    {"question": "Где правильно создана переменная?", "options": ["num = float(2)", "$num = 2", "Нет подходящего варианта"], "answer": "num = float(2)"},
    {"question": "Какой из методов используется для удаления пары ключ-значение из словаря?", "options": ["remove()", "pop()", "delete()"], "answer": "pop()"},
    {"question": "Какой из операторов будет эквивалентен a = a + 5?", "options": ["a += 5", "a =+ 5", "a + 5 = a"], "answer": "a += 5"},
    {"question": "Какую ошибку вернет код: a = {1, 2, 3}; a[0]", "options": ["KeyError", "IndexError", "TypeError"], "answer": "TypeError"},
    {"question": "Какое значение вернет выражение bool([])?", "options": ["True","False","Error"], "answer": "False"},
    {"question": "Какой метод используется для сортировки списка по убыванию?", "options": ["sort(reverse=True)", "descending()", "sorted(list, descending=True)"], "answer": "sort(reverse=True)"},
    {"question": "Вопрос: Какой метод используется для объединения всех элементов списка в строку?", "options": ["join()", "concatenate()", " append()"], "answer": "join()"},
    
]

questions_senior = [
    {"question": "Какое выражение создает генератор?", "options": ["[]", "()", "{}"], "answer": "()"},
    
    {"question": "Что вернет выражение: `(x for x in range(3))`?", 
     "options": ["Список", "Генератор", "Кортеж"], 
     "answer": "Генератор"},

    {"question": "Какой оператор используется для исключительного 'ИЛИ' в Python?", 
     "options": ["^", "&&", "||"], 
     "answer": "^"},

    {"question": "Что произойдет, если передать генератор функции `list()`?", 
     "options": ["Возникнет ошибка", "Будет создан список", "Будет создан кортеж"], 
     "answer": "Будет создан список"},

    {"question": "Какая разница между `is` и `==` в Python?", 
     "options": ["Сравнение значений", "Сравнение ссылок на объект", "Нет разницы"], 
     "answer": "Сравнение ссылок на объект"},

    {"question": "Что делает декоратор `@staticmethod`?", 
     "options": ["Создает статический метод", "Создает метод экземпляра", "Создает метод класса"], 
     "answer": "Создает статический метод"},

    {"question": "Какой из методов модуля `functools` используется для кеширования результатов функции?", 
     "options": ["cache()", "cached_result()", "lru_cache()"], 
     "answer": "lru_cache()"},

    {"question": "Что вернет функция `zip([1, 2], [3, 4, 5])`?", 
     "options": ["[(1, 3), (2, 4), (None, 5)]", "[(1, 3), (2, 4)]", "Ошибка"], 
     "answer": "[(1, 3), (2, 4)]"},

    {"question": "Каким будет результат выражения `all([])`?", 
     "options": ["True", "False", "Ошибка"], 
     "answer": "True"},

    {"question": "Какой встроенный модуль используется для работы с многопоточностью в Python?", 
     "options": ["threading", "multiprocessing", "os"], 
     "answer": "threading"},
]

@app.route("/toggle_theme", methods=["POST"])
def toggle_theme():
    # Переключаем тему между светлой и темной
    if session.get('theme') == 'dark':
        session['theme'] = 'light'
    else:
        session['theme'] = 'dark'
    return redirect(request.referrer)  # Возврат на предыдущую страницу


# Маршрут для выбора уровня сложности
@app.route("/", methods=["GET", "POST"])
def select_level():
    if request.method == "POST":
        level = request.form.get("level")
        session["level"] = level  # Сохраняем уровень в сессии
        session["score"] = 0  # Сбрасываем счет
        return redirect(url_for("quiz", question_index=0))
    return render_template("select_level.html")

# Маршрут для теста
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    level = session.get("level")
    question_index = int(request.args.get("question_index", 0))

    # Определяем набор вопросов по уровню
    if level == "junior":
        questions = questions_junior
    elif level == "middle":
        questions = questions_middle
    elif level == "senior":
        questions = questions_senior
    else:
        return redirect(url_for("select_level"))

    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option == questions[question_index]["answer"]:
            session["score"] += 1

        question_index += 1
        if question_index < len(questions):
            return redirect(url_for("quiz", question_index=question_index))
        else:
            return redirect(url_for("result"))

    # Возвращаем текущий вопрос и индекс
    return render_template("quiz.html", question=questions[question_index], question_index=question_index)

@app.route("/result")
def result():
    score = session.get("score", 0)
    level = session.get("level", "junior")
    
    if level == "junior":
        total_questions = len(questions_junior)
    elif level == "middle":
        total_questions = len(questions_middle)
    elif level == "senior":
        total_questions = len(questions_senior)
    
    # Удаляем score и level из сессии
    session.pop("score", None)
    session.pop("level", None)
    
    return render_template("result.html", score=score, total_questions=total_questions)

if __name__ == "__main__":
    app.run(debug=True)
