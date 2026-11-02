import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'salaries_arabic.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            الرقم INTEGER PRIMARY KEY AUTOINCREMENT,
            الاسم_الثلاثي TEXT,
            الدرجة INTEGER,
            المرحلة INTEGER,
            العنوان_الوظيفي TEXT,
            الراتب_الاسمي REAL,
            مخصصات_الشهادة REAL,
            المخصصات_الهندسية REAL,
            مخصصات_المنصب REAL,
            مخصصات_شهادات_عليا REAL,
            المخصصات_المهنية REAL,
            مخصصات_الزوجية REAL,
            مخصصات_الأطفال REAL,
            مخصصات_الموقع_الجغرافي REAL,
            خطورة_السواق REAL,
            مجموع_الاستحقاقات REAL,
            استقطاعات_التقاعد REAL,
            استقطاعات_الضريبة REAL,
            أمانات_الشؤون_الاجتماعية REAL,
            استقطاعات_إيجار_الدور REAL,
            استقطاعات_السلف REAL,
            مجموع_الاستقطاعات REAL,
            الراتب_الصافي REAL,
            ملاحظات TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_employee(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (
            الاسم_الثلاثي, الدرجة, المرحلة, العنوان_الوظيفي, الراتب_الاسمي,
            مخصصات_الشهادة, المخصصات_الهندسية, المخصصات_المنصب, مخصصات_شهادات_عليا, المخصصات_المهنية,
            مخصصات_الزوجية, المخصصات_الأطفال, المخصصات_الموقع_الجغرافي, خطورة_السواق, مجموع_الاستحقاقات,
            استقطاعات_التقاعد, استقطاعات_الضريبة, أمانات_الشؤون_الاجتماعية,
            استقطاعات_إيجار_الدور, استقطاعات_السلف, مجموع_الاستقطاعات, الراتب_الصافي, ملاحظات
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def search_employees(search_term):
    conn = sqlite3.connect(DB_PATH)
    if search_term:
        query = "SELECT * FROM employees WHERE الاسم_الثلاثي LIKE ?"
        df = pd.read_sql_query(query, conn, params=('%' + search_term + '%',))
    else:
        df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    
    # حفظ المعرف الحقيقي لقاعدة البيانات في عمود مخفي مؤقت للحذف الصحيح
    if not df.empty and 'الرقم' in df.columns:
        df['ID_H'] = df['الرقم']
        # جعل عمود الرقم يبدأ التسلسل من 1
        df['الرقم'] = range(1, len(df) + 1)
    
    # ترتيب الأعمدة الأساسي
    exact_columns_order = [
        'الرقم', 'الاسم_الثلاثي', 'الدرجة', 'المرحلة', 'العنوان_الوظيفي', 'الراتب_الاسمي',
        'مخصصات_الشهادة', 'المخصصات_الهندسية', 'مخصصات_المنصب', 'مخصصات_شهادات_عليا', 'المخصصات_المهنية',
        'مخصصات_الزوجية', 'المخصصات_الأطفال', 'مخصصات_الموقع_الجغرافي', 'خطورة_السواق', 'مجموع_الاستحقاقات',
        'استقطاعات_التقاعد', 'استقطاعات_الضريبة', 'أمانات_الشؤون_الاجتماعية', 'استقطاعات_إيجار_الدور',
        'استقطاعات_السلف', 'مجموع_الاستقطاعات', 'الراتب_الصافي', 'ملاحظات'
    ]
    existing_cols = [col for col in exact_columns_order if col in df.columns]
    df = df[existing_cols]
        
    return df

def delete_employee(emp_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE الرقم = ?", (emp_id,))
    conn.commit()
    conn.close()