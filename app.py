from flask import Flask  # импорт класса Flask из библиотеки flask (pip install flask)
from flask import render_template  # подключаем биб-ку для подключения html-шаблонов
from flask import request  # добавляем библиотеку request для обработки запросов
from flask import redirect  # и redirect для переадресации
from pymongo import MongoClient  # для работы с MongoDB (pip install pymongo)
from bson.objectid import ObjectId  # для работы с _id в MongoDB

app = Flask(__name__)  # создание объекта класса Flask (основным файлом будет сам этот файл (директива __name__))

client = MongoClient('localhost', 27017)  # создаем объект client класса MongoClient
db = client['pymongo_test']  # запускаем mongod.exe и работаем с БД 'pymongo_test'
collection = db['docs']  # работаем с коллекцией 'docs'


# @app.route('/')  # функция-декоратор отслеживания главной страницы по URL-адресу ('/')
# @app.route('/home')  # обработка двух URL-адресов
# def index():
#     return render_template("index.html")  # вывод шаблона на экран


@app.route('/')  # функция-декоратор отслеживания главной страницы по URL-адресу ('/')
@app.route('/home')  # обработка двух URL-адресов
@app.route('/docs')  # все документы на сайте
def docs():
    results = collection.find()  # создаем объект, кот. обращается к коллекции
    docs_col = [result for result in results]  # создаем список документов из коллекции
    print(docs_col)  # выводим список в консоль
    return render_template("docs.html", docs_col=docs_col)  # передаем список в шаблон (доступ по имени docs)


@app.route('/docs/<_id>/delete')  # удаление документа
def delete(_id):
    id_ = ObjectId(_id)  # для корректного доступа к _id документа

    try:
        collection.delete_one({'_id': id_})
        print('Document with _id: ' + _id + ' has been deleted successfully.')
        # удаляем документ с заданным _id в коллекцию
        # и выводим в консоль его _id
        return redirect('/docs')  # переадресовываем на вывод коллекции документов
    except:
        print('An error occurred while deleting the document')
        return 'An error occurred while deleting the document'


@app.route('/docs/<_id>/update', methods=['POST', 'GET'])  # редактирование документа
def update_doc(_id):
    id_ = ObjectId(_id)  # для корректного доступа к _id документа
    doc = collection.find_one({'_id': id_})  # находим документ с заденным _id
    print(doc)
    if request.method == 'POST':
        name = request.form['name']  # присваиваем переменным значения из формы
        password = request.form['password']
        email = request.form['email']

        updating_doc = {  # создаем новый документ
            "name": name,
            "password": password,
            "email": email
        }

        try:
            collection.update_one({'_id': id_}, {'$set': updating_doc})
            print('Document with _id: ' + str(id_) + ' has been updated successfully.')
            # изменяем значение полей документа в коллекции
            # и выводим в консоль его _id
            return redirect('/docs')  # переадресовываем на вывод коллекции документов
        except:
            print('An error occurred while updating the document.')
            return 'An error occurred while updating the document.'
    else:
        return render_template("update_doc.html", doc=doc)  # передать документ в шаблон


@app.route('/create_doc', methods=['POST', 'GET'])  # создание документа
# добавляем метод POST обработки запоса (по умолчанию только GET)
def create_doc():
    if request.method == 'POST':
        name = request.form['name']  # присваиваем переменным значения из формы
        password = request.form['password']
        email = request.form['email']

        new_doc = {  # создаем новый документ
            "name": name,
            "password": password,
            "email": email
        }

        try:
            result = collection.insert_one(new_doc).inserted_id
            print('Document with _id: ' + str(result) + ' has been created successfully.')
            # добавляем новый документ в коллекцию
            # и выводим в консоль его _id
            return redirect('/docs')  # переадресовываем на вывод коллекции документов
        except:
            print('An error occurred while creating the document.')
            return 'An error occurred while creating the document.'
    else:
        return render_template("create_doc.html")  # будет обрабатывать как данные из формы,
        # так и прямой заход на страницу


if __name__ == "__main__":  # если программа запускается через этот файл
    app.run(debug=True)  # запуск локального сервера в режиме отладки (вывод инф-ции об ошибках)
