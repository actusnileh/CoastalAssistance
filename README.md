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

* `make app` - Запустить контейнер
* `make build` - Забилдить контейнер
* `make drop` - Остановить контейнер
* `make logs` - Просмотр логов в контейнере
