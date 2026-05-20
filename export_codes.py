import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os


# Конфігурація підключення
load_dotenv()

url = URL.create(
    drivername=os.getenv("DB_DRIVER"),
    username=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DB"),
    password=os.getenv("DB_PASSWORD"),    
)

engine = create_engine(url)

def check_connection(engine):
    """
    Функція для перевірки з'єднання з базою даних.
    """
    try:
        with engine.connect() as connection:
            # Виконуємо найпростіший запит для перевірки активності
            result = connection.execute(text("SELECT 1"))# Важливо: використовуємо функцію text() для сирого SQL запиту
            if result.fetchone()[0] == 1:
                print("✅ З'єднання встановлено успішно!")
                return True
        
    except Exception as e:
        print(f"❌ Помилка з'єднання: {e}")
        return False



my_sql_query = \
    """
WITH ehealth AS (
SELECT 
    v.code, 
    v.description, 
    CASE 
        WHEN d.kwd_name = 'eHealth/ICD10_AM/condition_codes' THEN 'ICD10'
        ELSE'LOINC'
    END AS record_type
FROM core.dim_rpt_dictionary_values AS v
INNER JOIN core.dim_rpt_dictionaries AS d 
    ON v.dictionary_id = d.id
WHERE v.is_current = 'Y' 
  AND d.is_current = 'Y'
  AND d.kwd_name IN ('eHealth/ICD10_AM/condition_codes', 
                     'eHealth/LOINC/observation_codes')
),
actions AS (
SELECT
       code,
       kwd_name AS description,
	   'ACTION' AS record_type 
  FROM core.dim_rpt_services
 WHERE is_current = 'Y' 
   AND is_active
)

SELECT *
  FROM ehealth  
UNION ALL
SELECT *
  FROM actions

    """
if __name__ == "__main__":

    check_connection(engine)

    FILE = "./web_app/static/all_codes_new.csv"
    
    try:
        df = pd.read_sql(text(my_sql_query), con=engine)
        df.to_csv(FILE, index=False, encoding='utf-8')
        print(f"✅ Успішно збережено {len(df)} рядків у {FILE}")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    finally:
            # Повністю звільняємо ресурси пулу з'єднань
            engine.dispose()
            print("🔌 Пул з'єднань очищено.")

# Перевірка змін у кодах на DWH
# ---------------------------------------------------------------
    # Шляхи до файлів (винесемо в змінні для зручності)
    old_file_path = "./web_app/static/all_codes.csv"
    new_file_path = "./web_app/static/all_codes_new.csv"

    # Припускаємо, що df — це ваш новий датафрейм, зчитаний з all_codes_new.csv
    # df = pd.read_csv(new_file_path)

    df_new_sorted = df.sort_values(by='code').reset_index(drop=True)
    df_old = pd.read_csv(old_file_path)

    df_old_sorted = df_old.sort_values(by='code').reset_index(drop=True)
    df_old_sorted = df_old_sorted[df_new_sorted.columns]

    if df_old_sorted.equals(df_new_sorted):
        print("Змін у кодах не було")
        # Якщо потрібно, тут можна видалити тимчасовий all_codes_new.csv, 
        # щоб він не накопичувався в папці:
        os.remove(new_file_path)
    else:
        print("Виявлено зміни в кодах. Оновлюємо кодифікатор...")
        try:
            # 1. Видаляємо старий файл
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            
            # 2. Перейменовуємо новий файл на місце старого
            if os.path.exists(new_file_path):
                os.rename(new_file_path, old_file_path)
                print("Файли успішно оновлено!")
            else:
                print(f"Помилка: файл {new_file_path} не знайдено для перейменування.")
                
        except Exception as e:
            print(f"Сталася помилка під час оновлення файлів: {e}")
            




    
