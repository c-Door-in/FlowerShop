# FlowerShop

Сайт для магазина цветов.  

## Установка
Сайт написан полностью на Django.  

### Базовые настройки Django
У вас уже должен быть установлен `Python3`.  
Установите зависимости:
```
pip install -r requirements.txt
```
Запустите миграцию базы данных:
```
python manage.py migrate
```
Создайте учетную запись администратора:
```
python manage.py createsuperuser
```
Для автоматической отправки сообщений об обратном звонке и о заказе 
используется телеграм бот.  
Создайте в корне проекта файл `.env` и добавьте в него переменные окружения:
```
SECRET_KEY='your-django-secret-key'

BOT_API_KEY='your-telegram-bot-api-key'
```
Для оплаты используется система `Yoomoney`. В файл `.env` добавьте:
```
YOOMONEY_KEY=your-yoomoney-api-key

YOOMONEY_ID=your-yoomoney-id
```
### Настройка элементов сайта в базе данных.
Для корректного отображения некоторых элементов сайта, 
необходимо добавить в базу данных записи о букетах.  
База данных имеет следующую структуру:
- Событие (для которого подходит букет) - отображается при подборе букета
- Букет
- Заказ
- Обратный звонок - информация о запрошенной консультации
- Доставка - информация о доставке по заказу
- Платеж - подробности проведенного платежа

## Запуск
Для запуска используйте любой сервер. Можно воспользоваться 
встроенным сервером Django:
```
pyhon manage.py runserver
```

## Цели проекта
Проект создан по заказу портала [Devman](https://devman.org)
