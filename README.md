# url-shortener
Сервис для сокращения ссылок и перехода по сокращенным ссылкам. Python, Fast API

* `POST /shorten` — создание короткой ссылки
* `GET /{code}` — редирект на оригинальный URL
* Логирование событий
* Тесты на pytest
* SQLite без ORM

# Запуск проекта

## 1. Клонирование репозитория

```bash
git clone https://github.com/verolence/url-shortener
cd url-shortener
```

## 2. Создание виртуального окружения

```bash
python -m venv venv
```

### Активация

**Windows:**

```bash
.\venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

## 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -e .
```

## 4. Запуск приложения

```bash
uvicorn app.main:app --reload
```

После запуска сервер будет доступен по адресу:

```
http://127.0.0.1:8000
```

# Использование API

## Создание короткой ссылки

### В PowerShell:

```powershell
$body = @{ url = "https://boto.education/" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/shorten" -Method POST -Body $body -ContentType "application/json"
```

Пример ответа:

```json
{
  "short_url": "http://localhost:8000/cnGmT9"
}
```

## Переход по короткой ссылке

Открыть в браузере:

```
http://127.0.0.1:8000/cnGmT9
```

или через curl:

```bash
curl -L http://127.0.0.1:8000/cnGmT9
```

Произойдёт редирект на оригинальный URL.
