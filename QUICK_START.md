# 🚀 البدء السريع

## خطوات بسيطة للبدء

### 1️⃣ تثبيت المتطلبات

```bash
cd /home/ubuntu
pip install -r requirements.txt
```

### 2️⃣ إعداد Google Drive

1. اذهب إلى https://console.cloud.google.com/
2. أنشئ مشروعاً جديداً
3. فعّل Google Drive API
4. أنشئ مفتاح خدمة (Service Account Key)
5. احفظ ملف JSON باسم `credentials.json`
6. انسخه إلى `/home/ubuntu/drive_bot_data/credentials.json`

### 3️⃣ إعداد توكن تلجرام

```bash
# تحدث مع @BotFather على تلجرام وأنشئ بوتاً
export TELEGRAM_BOT_TOKEN='your_token_here'
```

### 4️⃣ تشغيل البوت

```bash
# تشغيل مباشر
python3 /home/ubuntu/drive_bot.py

# أو في الخلفية
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &
```

## ✨ ميزات البوت

| الميزة | الوصف |
|--------|-------|
| 📁 مشاريع | إنشاء وإدارة مشاريع متعددة |
| 🗜️ ضغط | ضغط تلقائي للملفات الكبيرة |
| 💾 حفظ | حفظ دائم للبيانات في JSON |
| 📤 رفع | رفع سريع إلى Google Drive |
| 🔄 إدارة | العودة للمشاريع القديمة |

## 📱 الاستخدام

1. ابدأ محادثة مع البوت: `/start`
2. اختر **📁 مشروع جديد**
3. أدخل اسم المشروع
4. أرسل ملفاتك
5. اختر المشروع المطلوب
6. تم! ✅

## 🆘 حل المشاكل

### البوت لا يعمل
```bash
# تحقق من التوكن
echo $TELEGRAM_BOT_TOKEN

# اطلع على السجل
tail -f /home/ubuntu/bot.log
```

### خطأ في رفع الملفات
- تأكد من وجود `credentials.json`
- تحقق من تفعيل Google Drive API
- أعد تشغيل البوت

## 📂 الملفات المهمة

```
/home/ubuntu/
├── drive_bot.py              # البوت الرئيسي
├── requirements.txt          # المتطلبات
├── SETUP_GUIDE.md           # دليل مفصل
├── QUICK_START.md           # هذا الملف
└── drive_bot_data/
    ├── credentials.json     # بيانات Google
    ├── projects.json        # المشاريع المحفوظة
    └── temp/               # ملفات مؤقتة
```

## 🎓 نصائح

- استخدم أسماء واضحة للمشاريع
- احتفظ بنسخة من `credentials.json` في مكان آمن
- تحقق من السجل عند حدوث مشاكل
- أعد تشغيل البوت بعد تحديث الإعدادات

---

**هل تحتاج مساعدة؟** اطلع على `SETUP_GUIDE.md` للتفاصيل الكاملة.
