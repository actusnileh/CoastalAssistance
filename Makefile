DC = docker compose
APP_FILE = docker_compose/app.yaml
STORAGE_FILE = docker_compose/database.yaml

.PHONY: app
app:
	${DC} -f ${APP_FILE} up -d

.PHONY: app-drop
drop:
	${DC} -f ${APP_FILE} down

.PHONY: drop-all
drop-all:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} down
	
.PHONY: logs
logs:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} logs -f

.PHONY: build
build:
	${DC} -f ${APP_FILE} -f ${STORAGE_FILE} up --build -d

