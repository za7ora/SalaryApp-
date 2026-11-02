import streamlit as st
import pandas as pd
import io
from database import init_db, add_employee, search_employees, delete_employee

# تهيئة قاعدة البيانات
init_db()

st.set_page_config(page_title="نظام إدارة رواتب الموظفين", layout="wide")

# --- نظام الحماية وتسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <style>
            .stApp {
                background-color: #f1f5f9;
            }
            div.stButton > button {
                background-color: #0891b2;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 6px;
                border: none;
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔒 تسجيل الدخول إلى نظام الرواتب")
    st.markdown("الرجاء إدخال اسم المستخدم وكلمة المرور للوصول إلى النظام:")
    
    with st.form("login_form"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submit_btn = st.form_submit_button("تسجيل الدخول")
        
        if submit_btn:
            # يمكنكِ تغيير "admin" و "12345" هنا إلى أي بيانات اعتماد ترغبين بها
            if username == "admin" and password == "12345":
                st.session_state.authenticated = True
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")
                
    st.stop() # إيقاف عرض باقي الصفحة حتى يتم تسجيل الدخول بنجاح

# --- الشريط الجانبي (Sidebar) ---
st.sidebar.title("🎛️ لوحة التحكم")

menu = ["إدخال موظف جديد", "البحث واستعراض البيانات"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

st.sidebar.markdown("---")
dark_mode = st.sidebar.toggle("🌙 الوضع المظلم (Dark Mode)", value=False)
st.sidebar.markdown("---")

# زر الخروج
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📌 عن النظام")
st.sidebar.markdown(
    """
    **نظام إدارة رواتب الموظفين**  
    نظام محلي متكامل مصمم خصيصاً لاحتساب الرواتب، المخصصات، والاستقطاعات بدقة عالية، مع إمكانية إدارة السجلات وتصدير التقارير بسهولة.
    """
)

# --- تخصيص الألوان والتصميم بالكامل ---
if dark_mode:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #0f172a;
                color: #ffffff;
            }
            [data-testid="stSidebar"] .stMarkdown, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] span {
                color: #ffffff !important;
            }
            .stApp {
                background-color: #1e293b;
                color: #f1f5f9;
            }
            input, select, textarea, div[data-baseweb="select"] span {
                font-size: 16px !important;
                background-color: #0f172a !important;
                color: #f1f5f9 !important;
            }
            label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
                font-size: 18px !important;
                font-weight: bold !important;
                color: #f8fafc !important;
            }
            th {
                font-size: 18px !important;
                font-weight: bold !important;
                background-color: #0f172a !important;
                color: white !important;
            }
            td {
                font-size: 16px !important;
                font-weight: bold !important;
            }
            div.stInfo {
                background-color: #0f172a !important;
                color: #38bdf8 !important;
                border: 1px solid #0ea5e9 !important;
                font-size: 16px !important;
                font-weight: bold !important;
            }
            div.stInfo p, div.stInfo span {
                color: #38bdf8 !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 20px !important;
                font-weight: bold !important;
                color: #38bdf8 !important;
            }
            [data-testid="stMetricLabel"] {
                font-size: 16px !important;
                color: #94a3b8 !important;
            }
            div.stButton > button {
                background-color: #0ea5e9;
                color: #0f172a;
                font-weight: bold;
                font-size: 16px;
                border-radius: 6px;
                border: none;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #0e7490;
                color: #ffffff;
            }
            [data-testid="stSidebar"] .stMarkdown, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] span {
                color: #ffffff !important;
            }
            .stApp {
                background-color: #f1f5f9;
                color: #0f172a;
            }
            input, select, textarea, div[data-baseweb="select"] span {
                font-size: 16px !important;
                color: #0f172a !important;
            }
            label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
                font-size: 19px !important;
                font-weight: bold !important;
                color: #0f172a !important;
            }
            th {
                font-size: 18px !important;
                font-weight: bold !important;
                background-color: #0e7490 !important;
                color: white !important;
            }
            td {
                font-size: 16px !important;
                font-weight: bold !important;
            }
            div.stInfo {
                background-color: #d1fae5 !important;
                color: #065f46 !important;
                border: 1px solid #10b981 !important;
                font-size: 18px !important;
                font-weight: bold !important;
            }
            div.stInfo p {
                color: #065f46 !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 20px !important;
                font-weight: bold !important;
            }
            div.stButton > button {
                background-color: #0891b2;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 6px;
                border: none;
            }
            div.stButton > button:hover {
                background-color: #0e7490;
            }
        </style>
    """, unsafe_allow_html=True)

# --- محتوى الصفحات الأساسي ---
st.title("📊 نظام إدارة واحتساب رواتب الموظفين")

salary_scale = {
    1: {1: 910, 2: 930, 3: 950, 4: 970, 5: 990, 6: 1010, 7: 1030, 8: 1050, 9: 1070, 10: 1090, 11: 1110},
    2: {1: 723, 2: 740, 3: 757, 4: 774, 5: 791, 6: 808, 7: 825, 8: 842, 9: 859, 10: 876, 11: 893},
    3: {1: 600, 2: 610, 3: 620, 4: 630, 5: 640, 6: 650, 7: 660, 8: 670, 9: 680, 10: 690, 11: 700},
    4: {1: 509, 2: 517, 3: 525, 4: 533, 5: 541, 6: 549, 7: 557, 8: 565, 9: 573, 10: 581, 11: 589},
    5: {1: 429, 2: 435, 3: 441, 4: 447, 5: 453, 6: 459, 7: 465, 8: 471, 9: 477, 10: 483, 11: 489},
    6: {1: 362, 2: 368, 3: 374, 4: 380, 5: 386, 6: 392, 7: 398, 8: 404, 9: 410, 10: 416, 11: 422},
    7: {1: 296, 2: 302, 3: 308, 4: 314, 5: 320, 6: 326, 7: 332, 8: 338, 9: 344, 10: 350, 11: 356},
    8: {1: 260, 2: 263, 3: 266, 4: 269, 5: 272, 6: 275, 7: 278, 8: 281, 9: 284, 10: 287, 11: 290},
    9: {1: 210, 2: 213, 3: 216, 4: 219, 5: 222, 6: 225, 7: 228, 8: 231, 9: 234, 10: 237, 11: 240},
    10: {1: 170, 2: 173, 3: 176, 4: 179, 5: 182, 6: 185, 7: 188, 8: 191, 9: 194, 10: 197, 11: 200}
}

if choice == "إدخال موظف جديد":
    st.subheader("📝 إدخال بيانات الموظف والراتب")
    
    with st.form("salary_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            full_name = st.text_input("الاسم الثلاثي")
            grade = st.number_input("الدرجة الوظيفية", min_value=1, max_value=10, value=5)
            stage = st.number_input("المرحلة (سنوات الخدمة)", min_value=1, max_value=11, value=1)
            job_title = st.text_input("العنوان الوظيفي")
            
        with col2:
            cert_option = st.selectbox(
                "مخصصات الشهادة", 
                ["بدون", "حرفة (15%)", "ابتدائية (15%)", "متوسطة (25%)", "دبلوم (35%)", "بكلوريوس (45%)", "دبلوم عالي (55%)", "ماجستير (75%)", "دكتوراه (100%)"]
            )
            eng_option = st.selectbox("المخصصات الهندسية", ["لا يوجد", "إداري (35%)", "موقع (45%)"])
            position_option = st.selectbox("مخصصات المنصب", ["بدون", "مدير عام (20%)", "مدير شعبة (15%)"])
            higher_deg_option = st.selectbox("مخصصات شهادات عليا (50%)", ["لا", "نعم"])
            prof_option = st.selectbox("المخصصات المهنية (20%)", ["لا", "نعم"])
            
        with col3:
            marital_option = st.selectbox("مخصصات زوجية", ["لا", "نعم (50,000)"])
            child_count = st.number_input("عدد الأطفال", min_value=0, max_value=20, value=0)
            location_option = st.selectbox("مخصصات الموقع الجغرافي", ["بدون", "المركز (20,000)", "الأطراف (60,000)"])
            driving_risk_option = st.selectbox("مخصصات خطورة سواق", ["لا", "نعم (87,500)"])
            
            rent_option = st.selectbox("استقطاع إيجار دور (6%)", ["لا", "نعم"])
            loan_option = st.selectbox("استقطاع سلف (5%)", ["لا", "نعم"])
            
            notes = st.text_area("ملاحظات")

        basic_salary = salary_scale.get(int(grade), {}).get(int(stage), 0) * 1000.0

        if cert_option in ["حرفة (15%)", "ابتدائية (15%)"]:
            cert_allowance = basic_salary * 0.15
        elif cert_option == "متوسطة (25%)":
            cert_allowance = basic_salary * 0.25
        elif cert_option == "دبلوم (35%)":
            cert_allowance = basic_salary * 0.35
        elif cert_option == "بكلوريوس (45%)":
            cert_allowance = basic_salary * 0.45
        elif cert_option == "دبلوم عالي (55%)":
            cert_allowance = basic_salary * 0.55
        elif cert_option == "ماجستير (75%)":
            cert_allowance = basic_salary * 0.75
        elif cert_option == "دكتوراه (100%)":
            cert_allowance = basic_salary * 1.00
        else:
            cert_allowance = 0.0

        if eng_option == "إداري (35%)":
            eng_allowance = basic_salary * 0.35
        elif eng_option == "موقع (45%)":
            eng_allowance = basic_salary * 0.45
        else:
            eng_allowance = 0.0

        if position_option == "مدير عام (20%)":
            position_allowance = basic_salary * 0.20
        elif position_option == "مدير شعبة (15%)":
            position_allowance = basic_salary * 0.15
        else:
            position_allowance = 0.0

        higher_deg_allowance = (basic_salary * 0.50) if higher_deg_option == "نعم" else 0.0
        prof_allowance = (basic_salary * 0.20) if prof_option == "نعم" else 0.0
        marital_allowance = 50000.0 if marital_option == "نعم (50,000)" else 0.0
        child_allowance = child_count * 10000.0
        
        if location_option == "المركز (20,000)":
            location_allowance = 20000.0
        elif location_option == "الأطراف (60,000)":
            location_allowance = 60000.0
        else:
            location_allowance = 0.0
            
        driving_risk_allowance = 87500.0 if driving_risk_option == "نعم (87,500)" else 0.0

        total_entitlement = (
            basic_salary + cert_allowance + eng_allowance + position_allowance + 
            higher_deg_allowance + prof_allowance + marital_allowance + 
            child_allowance + location_allowance + driving_risk_allowance
        )
        
        pension_deduction = basic_salary * 0.10
        tax_deduction = 0.0 
        social_deduction = total_entitlement * 0.0025
        rent_deduction = (basic_salary * 0.06) if rent_option == "نعم" else 0.0
        loan_deduction = (basic_salary * 0.05) if loan_option == "نعم" else 0.0
        
        total_deduction = pension_deduction + tax_deduction + social_deduction + rent_deduction + loan_deduction
        net_salary = total_entitlement - total_deduction

        st.markdown("---")
        st.markdown("### 🧮 معاينة تفاصيل الحسابات:")
        
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        m_col1.metric("الراتب الاسمي", f"{basic_salary:,.0f} د.ع")
        m_col2.metric("مخصصات المنصب", f"{position_allowance:,.0f} د.ع")
        m_col3.metric("شهادات عليا (50%)", f"{higher_deg_allowance:,.0f} د.ع")
        m_col4.metric("المخصصات المهنية", f"{prof_allowance:,.0f} د.ع")
        m_col5.metric("الراتب الصافي", f"{net_salary:,.0f} د.ع")

        st.info(f"💰 **مجموع الاستحقاقات:** {total_entitlement:,.0f} دينار  |  📉 **مجموع الاستقطاعات:** {total_deduction:,.0f} دينار  |  ✨ **الراتب الصافي النهائي:** {net_salary:,.0f} دينار")

        submit = st.form_submit_button("حفظ بيانات الموظف في قاعدة البيانات")
        
        if submit:
            if full_name.strip() == "":
                st.error("يرجى إدخال اسم الموظف!")
            else:
                data_tuple = (
                    full_name, grade, stage, job_title, basic_salary,
                    cert_allowance, eng_allowance, position_allowance, higher_deg_allowance, prof_option,
                    marital_allowance, child_allowance, location_allowance,
                    driving_risk_allowance, total_entitlement, pension_deduction,
                    tax_deduction, social_deduction, rent_deduction, loan_deduction,
                    total_deduction, net_salary, notes
                )
                add_employee(data_tuple)
                st.success(f"تم حفظ بيانات الموظف ({full_name}) بنجاح!")

elif choice == "البحث واستعراض البيانات":
    st.subheader("🔍 البحث وإدارة سجلات الموظفين")
    
    search_term = st.text_input("أبحث عن اسم الموظف:")
    df = search_employees(search_term)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("🗑️ حذف موظف (تقاعد / استقالة / نقل)")
        
        employee_options = {f"{row['الاسم_الثلاثي']} (تسلسل: {row['الرقم']})": row['ID_H'] if 'ID_H' in df.columns else row['الرقم'] for index, row in df.iterrows()}
        selected_emp_label = st.selectbox("اختر الموظف المراد حذفه:", options=list(employee_options.keys()))
        
        if st.button("حذف الموظف المحدد نهائياً"):
            emp_id_to_delete = employee_options[selected_emp_label]
            delete_employee(emp_id_to_delete)
            st.success("تم حذف الموظف بنجاح من قاعدة البيانات!")
            st.rerun()

        st.markdown("---")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='سجل الرواتب')
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 تحميل النتائج بملف Excel",
            data=excel_data,
            file_name="salaries_arabic_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("لا توجد نتائج مطابقة للبحث.")