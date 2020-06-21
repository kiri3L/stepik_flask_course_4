# stepik_flask_course_4

Перед первым запуском необходимо выполнить следующие действия

1. Создать переменную окружения
```
	export DATABASE_URL='postgresql://user:password@hostname:port/database_name'
```

2. Выполнить миграцию
```
	flask db upgrade
```
3. Зполнить базу данных данными из .json файлов
```
	python3 run.py --init
```

После этого можно запустить приложение двумя способами:

1. flask
```
	python3 run.py
```

2. Gunicorn
```
	gunicorn src:app
```

Работающее приложения можно посмотреть [тут](https://dry-everglades-18357.herokuapp.com/)
