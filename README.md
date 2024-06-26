<p align="center"><img align="center" width="280" src="/img/rounded_logo.png"/></p>

# Coastal Assistance
Coastal Assistance - это Telegram-бот, созданный в рамках выполнения кейса №03 на хакатоне "Азовское море". Этот бот позволяет пользователям загружать фотографии береговой линии и удобно просматривать уже добавленные данные о состоянии берега. После загрузки фотографии бот анализирует ее и определяет процент разрушенности. Эта информация может быть использована для разработки решений по проблеме эрозии береговой линии.

<h2>🛠️ Установка:</h2>

<p>1. Клонируйте репозиторий</p>

```
git clone https://github.com/actusnileh/CoastalAssistance.git && cd CoastalAssistance
```

<p>2. Установите все необходимые пакеты из раздела "Зависимости".</p>
  
<h2> Зависимости </h2>

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)


<h2> Основные команды </h2>

* `make app` - Запустить контейнер.
* `make build` - Собрать контейнеры.
* `make storage` - Запустить контейнер.
* `make drop-storage` - Остановить контейнер.
* `make drop-app` - Остановить контейнер.
* `make drop-all` - Остановить все контейнеры.
* `make logs` - Просмотр логов в контейнере.

<h2> .env </h2>

* `BOT_TOKEN` - Токен вашего Telegram бота. Вы можете получить этот токен у BotFather при создании нового бота.
* `ADMIN_ID` - Id аккаунта администратора в Telegram.
* `YANDEX_MAPS_TOKEN` - Токен API для использования сервиса Яндекс.Карты. 
* `POSTGRESQL_USERNAME` - Имя пользователя для подключения к базе данных PostgreSQL.
* `POSTGRESQL_PASSWORD` - Пароль для подключения к базе данных PostgreSQL.
* `POSTGRESQL_HOST` - Адрес сервера базы данных PostgreSQL.
* `POSTGRESQL_PORT` - Порт для подключения к базе данных PostgreSQL.
* `POSTGRESQL_NAME` - Имя базы данных PostgreSQL