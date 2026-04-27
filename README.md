# 🤖 بوت تلجرام لرفع الملفات إلى Google Drive

بوت ذكي وقوي لرفع الملفات والصور تلقائياً إلى Google Drive مباشرة من تلجرام، مع ميزات متقدمة مثل الضغط التلقائي وإدارة المشاريع.

## ✨ الميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| 📁 **إدارة المشاريع** | إنشاء وإدارة مشاريع متعددة بسهولة |
| 🗜️ **ضغط تلقائي** | ضغط الملفات والصور تلقائياً قبل الرفع |
| 💾 **حفظ دائم** | حفظ جميع البيانات في ملف JSON دائم |
| 📤 **رفع سريع** | رفع الملفات مباشرة إلى Google Drive |
| 🔄 **إدارة متقدمة** | العودة للمشاريع القديمة والتعديل عليها |
| 🔐 **آمن** | دعم كامل لبيانات الاعتماد الآمنة |
| 📊 **تتبع** | تتبع عدد الملفات المرفوعة لكل مشروع |

## 🚀 البدء السريع

### المتطلبات

- Python 3.8+
- حساب تلجرام
- حساب Google Cloud مع Google Drive API

### التثبيت

```bash
# 1. استنساخ أو تحميل المشروع
cd /home/ubuntu

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. إعداد بيانات الاعتماد
# انسخ credentials.json إلى /home/ubuntu/drive_bot_data/

# 4. تعيين التوكن
export TELEGRAM_BOT_TOKEN='your_token_here'

# 5. تشغيل البوت
python3 drive_bot.py
```

## 📖 الأدلة التفصيلية

- **[دليل الإعداد الكامل](SETUP_GUIDE.md)** - خطوات مفصلة للإعداد
- **[البدء السريع](QUICK_START.md)** - خطوات بسيطة للبدء الفوري
- **[دليل الصيانة](MAINTENANCE.md)** - إدارة وصيانة البوت

## 📁 هيكل المشروع

```
/home/ubuntu/
├── drive_bot.py                    # ملف البوت الرئيسي
├── requirements.txt                # المتطلبات
├── README.md                       # هذا الملف
├── SETUP_GUIDE.md                 # دليل الإعداد الكامل
├── QUICK_START.md                 # البدء السريع
├── MAINTENANCE.md                 # دليل الصيانة
├── bot.log                        # سجل البوت
├── bot_output.log                 # سجل الإخراج
└── drive_bot_data/
    ├── credentials.json           # بيانات اعتماد Google Drive
    ├── credentials_example.json   # مثال على بيانات الاعتماد
    ├── projects.json              # بيانات المشاريع المحفوظة
    ├── projects_example.json      # مثال على بيانات المشاريع
    └── temp/                      # ملفات مؤقتة
```

## 🎯 كيفية الاستخدام

### 1. بدء المحادثة

أرسل `/start` للبوت على تلجرام

### 2. إنشاء مشروع جديد

- اختر **📁 مشروع جديد**
- أدخل اسم المشروع
- سيتم إنشاء مجلد في Google Drive

### 3. رفع الملفات

- أرسل ملف أو صورة
- اختر المشروع المطلوب
- سيتم رفع الملف تلقائياً مع الضغط إذا لزم

### 4. إدارة المشاريع

- اختر **📂 مشاريعي** لعرض جميع مشاريعك
- يمكنك العودة لأي مشروع قديم

## 🔧 الأوامر والخيارات

| الأمر | الوصف |
|------|-------|
| `/start` | بدء المحادثة مع البوت |
| `📁 مشروع جديد` | إنشاء مشروع جديد |
| `📂 مشاريعي` | عرض جميع مشاريعك |
| `⚙️ الإعدادات` | إعدادات البوت |
| `ℹ️ معلومات` | معلومات عن البوت |

## 🗜️ نظام الضغط

### الصور
- تقليل الجودة مع الحفاظ على الوضوح
- دعم جميع صيغ الصور (JPG, PNG, GIF, BMP)
- الحد الأقصى: 20 ميجابايت

### الملفات
- ضغط باستخدام gzip
- دعم جميع أنواع الملفات
- الحد الأقصى: 20 ميجابايت

## 💾 نظام الحفظ الدائم

جميع المشاريع تُحفظ في ملف `projects.json`:

```json
{
  "user_id": {
    "project_name": {
      "folder_id": "google_drive_folder_id",
      "created_at": "2024-01-15T10:30:00",
      "files_count": 5
    }
  }
}
```

## 🔐 الأمان

- بيانات الاعتماد محفوظة في ملف منفصل
- لا يتم حفظ التوكن في الملفات
- صلاحيات آمنة للملفات الحساسة
- تشفير اختياري للبيانات الحساسة

## 🐛 استكشاف الأخطاء

### البوت لا يبدأ

```bash
# تحقق من التوكن
echo $TELEGRAM_BOT_TOKEN

# تحقق من المتطلبات
pip list | grep -E "telegram|Pillow|google"

# اطلع على رسالة الخطأ
python3 drive_bot.py
```

### خطأ في رفع الملفات

```bash
# تحقق من بيانات الاعتماد
ls -la /home/ubuntu/drive_bot_data/credentials.json

# تحقق من صحة JSON
python3 -m json.tool /home/ubuntu/drive_bot_data/credentials.json

# اطلع على السجل
tail -f /home/ubuntu/bot.log
```

### مشاكل في الضغط

```bash
# تحقق من Pillow
python3 -c "from PIL import Image; print('OK')"

# نظف الملفات المؤقتة
rm -rf /home/ubuntu/drive_bot_data/temp/*
```

## 📊 المراقبة والإحصائيات

```bash
# عرض حالة البوت
ps aux | grep drive_bot.py

# عرض السجلات
tail -f /home/ubuntu/bot.log

# عرض إحصائيات الاستخدام
python3 -c "import json; data = json.load(open('/home/ubuntu/drive_bot_data/projects.json')); print(f'المستخدمون: {len(data)}'); print(f'المشاريع: {sum(len(v) for v in data.values())}')"
```

## 🔄 إدارة البوت

### تشغيل البوت

```bash
# تشغيل مباشر
python3 /home/ubuntu/drive_bot.py

# تشغيل في الخلفية
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &
```

### إيقاف البوت

```bash
pkill -f drive_bot.py
```

### إعادة تشغيل البوت

```bash
pkill -f drive_bot.py || true
sleep 2
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &
```

## 📚 المراجع

- [توثيق python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [توثيق Google Drive API](https://developers.google.com/drive/api)
- [توثيق Pillow](https://pillow.readthedocs.io/)

## 🤝 المساهمة

يمكنك تحسين البوت بإضافة ميزات جديدة أو إصلاح الأخطاء.

## 📝 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام الحر.

## 💡 نصائح مفيدة

1. **استخدم أسماء واضحة للمشاريع** - لسهولة البحث والتنظيم
2. **احتفظ بنسخة احتياطية** - من `credentials.json` و `projects.json`
3. **راقب السجلات** - للتحقق من عمل البوت بشكل صحيح
4. **نظف الملفات المؤقتة** - بانتظام لتوفير المساحة
5. **حدّث المتطلبات** - للحصول على أحدث الميزات والأمان

## 🆘 الدعم

إذا واجهت مشكلة:

1. اطلع على [دليل الإعداد](SETUP_GUIDE.md)
2. تحقق من [دليل الصيانة](MAINTENANCE.md)
3. اطلع على السجلات: `tail -f /home/ubuntu/bot.log`
4. تأكد من تثبيت جميع المتطلبات

---

**تم تطوير هذا البوت بواسطة Manus** ✨

**الإصدار**: 2.0  
**آخر تحديث**: 2024-01-27
