# Flask — Перевірка кодів ЕСОЗ

Веб-застосунок для перевірки медичних кодів (МКХ-10, LOINC, інтервенції) на наявність у реєстрі ЕСОЗ.

---

## Що робить

Приймає список кодів від користувача, звіряє їх з еталонним набором і повертає перелік відсутніх у ЕСОЗ.

Підтримувані типи кодів:

- **ICD-10** — діагнози (`eHealth/ICD10_AM/condition_codes`)
- **LOINC** — спостереження (`eHealth/LOINC/observation_codes`)
- **ACTION** — інтервенції/послуги

---

## Стек

| Компонент | Версія |
|-----------|--------|
| Python | 3.12 |
| Flask | 3.1 |
| Flask-WTF | 1.3 |
| pandas | 3.0 |
| SQLAlchemy | — |
| Poetry | 2.x |

---

## Структура проєкту

```
.
├── main.py                  # точка входу, маршрути Flask
├── export_codes.py          # скрипт вивантаження та оновлення реєстру кодів
├── pyproject.toml
├── poetry.lock
├── requirements.txt         # для деплою на PythonAnywhere
└── web_app/
    ├── static/
    │   ├── all_codes.csv    # еталонний реєстр кодів
    │   └── css/
    │       └── style.css
    └── templates/
        ├── base.html
        └── index.html
```

---

## Локальний запуск

### 1. Клонувати репозиторій

```bash
git clone https://github.com/olekoval/flask_searching_codes.git
cd flask_searching_codes
```

### 2. Встановити залежності через Poetry

```bash
poetry install
```

### 3. Створити `.env`

```env
SECRET_KEY=your-secret-key-here

# Параметри підключення до БД (потрібні лише для export_codes.py)
DB_DRIVER=postgresql+psycopg2
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_DB=your-db-name
```

Без `SECRET_KEY` застосунок запуститься з випадково згенерованим ключем — сесії будуть скидатися при перезапуску.

### 4. Запустити

```bash
poetry run python main.py
```

Відкрити у браузері: [http://localhost:5000](http://localhost:5000)

---

## Оновлення реєстру кодів

Реєстр зберігається у `web_app/static/all_codes.csv` і формується скриптом `export_codes.py`, який:

1. Підключається до DWH через змінні середовища з `.env`.
2. Вивантажує актуальні коди ICD-10, LOINC та інтервенцій.
3. Порівнює новий зріз зі старим `all_codes.csv`.
4. Замінює файл лише якщо виявлено зміни — інакше видаляє тимчасовий файл.

```bash
poetry run python export_codes.py
```

Очікуваний формат CSV:

```
code,description,record_type
A00,Cholera,ICD10
26436-6,Complete blood count,LOINC
```

> Після оновлення `all_codes.csv` потрібно перезавантажити воркер на PythonAnywhere (кнопка **Reload**), щоб Flask підхопив новий файл — він читається один раз при старті застосунку.
## Оновлення файлу all_codes.csv на PythonAnywhere

## Оновлення змін з github на PythonAnywhere
```bash
cd ~/kod-checker
git pull
```
---

## Деплой на PythonAnywhere

Коротко:

```bash
# 1. Згенерувати requirements.txt локально (якщо ще не зроблено)
poetry export -f requirements.txt --output requirements.txt --without-hashes --without-markers

# 2. На сервері — клонувати і встановити залежності
git clone https://github.com/olekoval/flask_searching_codes.git
python3.12 -m venv ~/.virtualenvs/my-env
source ~/.virtualenvs/my-env/bin/activate
pip install -r requirements.txt
```

Після налаштування Web App і WSGI-файлу — натиснути **Reload**.

---

## Змінні середовища

| Змінна | Де потрібна | Опис |
|--------|-------------|------|
| `SECRET_KEY` | `main.py` | Ключ підпису CSRF-токенів Flask-WTF |
| `DB_DRIVER` | `export_codes.py` | SQLAlchemy driver, напр. `postgresql+psycopg2` |
| `DB_HOST` | `export_codes.py` | Хост бази даних |
| `DB_USER` | `export_codes.py` | Користувач БД |
| `DB_PASSWORD` | `export_codes.py` | Пароль БД |
| `DB_DB` | `export_codes.py` | Назва бази даних |

---


