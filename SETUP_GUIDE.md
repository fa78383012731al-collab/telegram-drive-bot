# دليل إعداد بوت تلجرام لرفع الملفات إلى Google Drive

## 📋 المتطلبات

- Python 3.8 أو أحدث
- حساب تلجرام
- حساب Google Cloud مع تفعيل Google Drive API

## 🚀 خطوات الإعداد

### 1. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2. إعداد بيانات اعتماد Google Drive

#### أ. إنشاء مشروع Google Cloud

1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. أنشئ مشروعاً جديداً
3. فعّل Google Drive API:
   - اذهب إلى "APIs & Services" > "Library"
   - ابحث عن "Google Drive API"
   - اضغط "Enable"

#### ب. إنشاء مفتاح خدمة

1. اذهب إلى "APIs & Services" > "Credentials"
2. اضغط "Create Credentials" > "Service Account"
3. ملأ التفاصيل المطلوبة
4. اضغط "Create and Continue"
5. اضغط "Create Key" > "JSON"
6. سيتم تحميل ملف JSON - احفظه باسم `credentials.json`

#### ج. نسخ ملف بيانات الاعتماد

```bash
cp /path/to/credentials.json /home/ubuntu/drive_bot_data/credentials.json
```

### 3. إعداد توكن تلجرام

1. تحدث مع [@BotFather](https://t.me/botfather) على تلجرام
2. أنشئ بوتاً جديداً واحصل على التوكن
3. عيّن متغير البيئة:

```bash
export TELEGRAM_BOT_TOKEN='your_token_here'
```

### 4. تشغيل البوت

```bash
python3 /home/ubuntu/drive_bot.py
```

أو لتشغيل البوت في الخلفية:

```bash
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &
```

## 📁 هيكل المشروع

```
/home/ubuntu/
├── drive_bot.py                 # ملف البوت الرئيسي
├── requirements.txt             # المتطلبات
├── SETUP_GUIDE.md              # هذا الملف
├── bot.log                      # سجل البوت
├── drive_bot_data/
│   ├── credentials.json         # بيانات اعتماد Google Drive
│   ├── projects.json            # بيانات المشاريع
│   └── temp/                    # ملفات مؤقتة
```

## 🎯 ميزات البوت

### 1. إنشاء مشاريع جديدة
- أنشئ مشاريع متعددة لتنظيم ملفاتك
- كل مشروع له مجلد منفصل في Google Drive

### 2. ضغط تلقائي للملفات
- **الصور**: تقليل الجودة مع الحفاظ على الوضوح
- **الملفات**: ضغط باستخدام gzip
- الحد الأقصى: 20 ميجابايت

### 3. حفظ دائم للمشاريع
- جميع المشاريع تُحفظ في ملف JSON
- لا تضيع البيانات عند إعادة تشغيل البوت

### 4. إدارة المشاريع
- عرض جميع مشاريعك
- العودة لأي مشروع قديم
- تحديث المشاريع الموجودة

## 📱 استخدام البوت

### الأوامر الأساسية

1. **/start** - بدء المحادثة مع البوت
2. **📁 مشروع جديد** - إنشاء مشروع جديد
3. **📂 مشاريعي** - عرض مشاريعك
4. **⚙️ الإعدادات** - إعدادات البوت
5. **ℹ️ معلومات** - معلومات عن البوت

### رفع الملفات

1. اختر **📁 مشروع جديد** أو **📂 مشاريعي**
2. أرسل الملف أو الصورة
3. اختر المشروع المطلوب
4. سيتم رفع الملف تلقائياً مع الضغط إذا لزم

## 🔧 استكشاف الأخطاء

### البوت لا يبدأ
- تحقق من أن التوكن صحيح: `echo $TELEGRAM_BOT_TOKEN`
- تحقق من الاتصال بالإنترنت
- اطلع على السجل: `tail -f /home/ubuntu/bot.log`

### خطأ في رفع الملفات
- تأكد من أن ملف `credentials.json` موجود
- تأكد من أن Google Drive API مفعّل
- تحقق من صلاحيات الخدمة

### الملفات لا تُضغط
- تحقق من تثبيت Pillow: `pip list | grep Pillow`
- تأكد من أن الملف ليس تالفاً
- اطلع على السجل للأخطاء

## 🛑 إيقاف البوت

```bash
# إيقاف البوت الذي يعمل في الخلفية
ps aux | grep drive_bot.py | grep -v grep | awk '{print $2}' | xargs kill -9
```

## 📝 ملاحظات مهمة

1. **حد الحجم**: تلجرام يسمح بـ 20 ميجابايت كحد أقصى للملفات
2. **الملفات الكبيرة جداً**: إذا كان الملف أكبر من 20 ميجابايت، يجب ضغطه أولاً
3. **الخصوصية**: لا تشارك ملف `credentials.json` مع أحد
4. **النسخ الاحتياطية**: احتفظ بنسخة احتياطية من `projects.json`

## 🤝 الدعم

إذا واجهت مشكلة:

1. اطلع على السجل: `cat /home/ubuntu/bot.log`
2. تحقق من متطلبات الإعداد
3. جرّب إعادة تشغيل البوت
4. تأكد من أن جميع المتطلبات مثبتة

## 📚 مراجع إضافية

- [توثيق python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [توثيق Google Drive API](https://developers.google.com/drive/api)
- [توثيق Pillow](https://pillow.readthedocs.io/)
