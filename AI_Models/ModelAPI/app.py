import joblib
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. تعريف التطبيق
app = FastAPI(title="Egypt & US Hybrid Traffic Risk API", version="1.0")

# 2. السماح للواجهة (الخريطة) إنها تتصل بالسيرفر (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. تحديد مسار الموديلات وتحميلها
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
US_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'road_risk_model.pkl')
EGYPT_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'pure_egypt_model.pkl')

print("⏳ جاري تحميل الموديلات...")
us_model = joblib.load(US_MODEL_PATH)
egypt_model = joblib.load(EGYPT_MODEL_PATH)
print("✅ تم تحميل الموديلات بنجاح!")

# 4. هيكل استقبال البيانات
class TrafficInput(BaseModel):
    hour: int
    day_of_week: str
    temperature_c: float
    humidity_pct: float
    wind_speed_ms: float
    current_speed: float
    weather_encoded: str
    adas_encoded: str

# 5. دالة الذكاء الاصطناعي الذكية
@app.post("/predict/egypt")
def predict_egyptian_risk(data: TrafficInput):
    days_mapping = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, 
        "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    weather_mapping = {
        "Sunny": 0, "Rainy": 1, "Foggy": 2, "Clear": 0
    }
    adas_mapping = {
        "Normal": 0, "Alert": 0, "Drowsy": 1, "Fatigued": 2, "Distracted": 3
    }
    
    day_num = days_mapping.get(data.day_of_week.capitalize(), 0)
    weather_num = weather_mapping.get(data.weather_encoded.capitalize(), 0)
    adas_num = adas_mapping.get(data.adas_encoded.capitalize(), 0)

    features = [[
        data.hour,
        day_num,
        data.temperature_c,
        data.humidity_pct,
        data.wind_speed_ms,
        data.current_speed,
        adas_num
    ]]
    
    # توقع الموديل الخام
    prediction = egypt_model.predict(features)[0]
    prediction_str = str(prediction)
    
    # 🌟 التدخل الذكي لمعالجة الطرق المغلقة أو البطيئة وحالة السائق
    
    # لو السائق مرهق أو نعسان، مستحيل نعتبر الطريق آمن تماماً
    if data.adas_encoded in ["Drowsy", "Fatigued"]:
        if prediction_str in ["Minor", "Safe"]:
            prediction_str = "Moderate"
            
    # لو مشتت، الخطورة تعلى
    if data.adas_encoded == "Distracted":
        prediction_str = "High"

    # لو الطريق سرعته أقل من 25 كم/س (مقفول، زحمة شديدة، أو حوادث) والسواق حالته سيئة = كارثة
    if data.current_speed < 25.0 and data.adas_encoded != "Normal":
        prediction_str = "Severe"

    # تحديد الرسالة المناسبة بناءً على الخطورة
    if prediction_str == "Severe":
        reason = "🚨 تحذير حرج: الطريق يحتوي على إغلاقات أو زحام شديد (سرعة بطيئة جداً)، وحالتك (نعسان/مرهق) لا تسمح بالقيادة إطلاقاً. توقف فوراً!"
    elif prediction_str == "High":
        reason = "⚠️ تحذير عالي: حالتك الحالية تشكل خطراً كبيراً على هذا المسار. يرجى تجنب القيادة."
    elif prediction_str == "Moderate":
        reason = "🟡 تنبيه: يرجى الانتباه وتخفيف السرعة. حالتك تتطلب حذراً إضافياً على هذا الطريق."
    else:
        reason = "✅ الطريق سالك وحالتك طبيعية. رحلة آمنة."

    return {
        "model": "Egypt ADAS Hybrid Model",
        "predicted_severity_level": prediction_str,
        "recommendation_reason": reason,
        "message": "تم التقييم بنجاح."
    }