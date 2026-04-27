# 🔧 دليل الصيانة والإدارة

## 📊 مراقبة البوت

### عرض حالة البوت

```bash
# التحقق من أن البوت يعمل
ps aux | grep drive_bot.py | grep -v grep

# عرض معلومات العملية
ps aux | grep drive_bot.py
```

### عرض السجلات

```bash
# عرض آخر 50 سطر من السجل
tail -50 /home/ubuntu/bot.log

# عرض السجل في الوقت الفعلي
tail -f /home/ubuntu/bot.log

# البحث عن الأخطاء
grep ERROR /home/ubuntu/bot.log

# عرض سجل الإخراج
tail -f /home/ubuntu/bot_output.log
```

## 🚀 إدارة عملية البوت

### تشغيل البوت

```bash
# تشغيل مباشر (سيتوقف عند إغلاق الطرفية)
python3 /home/ubuntu/drive_bot.py

# تشغيل في الخلفية
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &

# تشغيل مع screen
screen -S telegram_bot
python3 /home/ubuntu/drive_bot.py
# اضغط Ctrl+A ثم D للخروج
```

### إيقاف البوت

```bash
# إيقاف البوت الذي يعمل في الخلفية
ps aux | grep drive_bot.py | grep -v grep | awk '{print $2}' | xargs kill -9

# أو بطريقة أكثر أماناً
pkill -f drive_bot.py
```

### إعادة تشغيل البوت

```bash
# إيقاف وتشغيل
ps aux | grep drive_bot.py | grep -v grep | awk '{print $2}' | xargs kill -9 || true
sleep 2
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &
```

## 📁 إدارة البيانات

### عرض المشاريع المحفوظة

```bash
# عرض ملف المشاريع
cat /home/ubuntu/drive_bot_data/projects.json

# عرض بصيغة منسقة
python3 -m json.tool /home/ubuntu/drive_bot_data/projects.json
```

### نسخ احتياطية

```bash
# إنشاء نسخة احتياطية من المشاريع
cp /home/ubuntu/drive_bot_data/projects.json /home/ubuntu/drive_bot_data/projects_backup_$(date +%Y%m%d_%H%M%S).json

# إنشاء نسخة احتياطية من بيانات الاعتماد
cp /home/ubuntu/drive_bot_data/credentials.json /home/ubuntu/drive_bot_data/credentials_backup_$(date +%Y%m%d_%H%M%S).json

# إنشاء نسخة احتياطية من كل شيء
tar -czf /home/ubuntu/bot_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/ubuntu/drive_bot_data/
```

### تنظيف الملفات المؤقتة

```bash
# حذف الملفات المؤقتة
rm -rf /home/ubuntu/drive_bot_data/temp/*

# حذف السجلات القديمة
rm /home/ubuntu/bot.log
```

## 🔐 الأمان

### حماية بيانات الاعتماد

```bash
# تعيين صلاحيات آمنة للملفات
chmod 600 /home/ubuntu/drive_bot_data/credentials.json
chmod 600 /home/ubuntu/drive_bot_data/projects.json

# التحقق من الصلاحيات
ls -la /home/ubuntu/drive_bot_data/
```

### إخفاء التوكن

```bash
# لا تضع التوكن في ملفات قابلة للمشاركة
# استخدم متغيرات البيئة فقط
export TELEGRAM_BOT_TOKEN='your_token_here'

# تحقق من أنه لم يُحفظ في السجل
grep TELEGRAM_BOT_TOKEN /home/ubuntu/bot.log
```

## 🐛 استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### 1. البوت لا يبدأ

```bash
# تحقق من التوكن
echo $TELEGRAM_BOT_TOKEN

# تحقق من تثبيت المتطلبات
pip list | grep -E "telegram|Pillow|google"

# اطلع على رسالة الخطأ
python3 /home/ubuntu/drive_bot.py
```

#### 2. خطأ في الاتصال بـ Google Drive

```bash
# تحقق من وجود ملف بيانات الاعتماد
ls -la /home/ubuntu/drive_bot_data/credentials.json

# تحقق من صحة JSON
python3 -m json.tool /home/ubuntu/drive_bot_data/credentials.json

# تحقق من تفعيل Google Drive API
# اذهب إلى https://console.cloud.google.com/
```

#### 3. مشاكل في ضغط الملفات

```bash
# تحقق من تثبيت Pillow
python3 -c "from PIL import Image; print('Pillow OK')"

# تحقق من الملفات المؤقتة
ls -la /home/ubuntu/drive_bot_data/temp/

# تنظيف الملفات المؤقتة
rm -rf /home/ubuntu/drive_bot_data/temp/*
```

## 📈 الإحصائيات

### عرض إحصائيات الاستخدام

```bash
# عدد المشاريع
python3 -c "import json; data = json.load(open('/home/ubuntu/drive_bot_data/projects.json')); print(f'عدد المستخدمين: {len(data)}'); print(f'إجمالي المشاريع: {sum(len(v) for v in data.values())}')"

# حجم البيانات
du -sh /home/ubuntu/drive_bot_data/

# حجم السجلات
du -sh /home/ubuntu/*.log
```

## 🔄 التحديثات

### تحديث المتطلبات

```bash
# تحديث جميع المتطلبات
pip install --upgrade -r requirements.txt

# تحديث مكتبة معينة
pip install --upgrade python-telegram-bot
```

### تحديث البوت

```bash
# إيقاف البوت الحالي
pkill -f drive_bot.py

# تحديث الملفات
# (استبدل drive_bot.py بالإصدار الجديد)

# تشغيل البوت الجديد
nohup python3 /home/ubuntu/drive_bot.py > /home/ubuntu/bot_output.log 2>&1 &
```

## 📅 الجدولة التلقائية

### إنشاء نسخة احتياطية يومية

```bash
# أضف هذا السطر إلى crontab
crontab -e

# أضف السطر التالي:
0 2 * * * tar -czf /home/ubuntu/backups/bot_backup_$(date +\%Y\%m\%d).tar.gz /home/ubuntu/drive_bot_data/
```

### تنظيف الملفات المؤقتة أسبوعياً

```bash
# أضف هذا السطر إلى crontab
0 3 * * 0 rm -rf /home/ubuntu/drive_bot_data/temp/*
```

## 📞 الدعم الفني

### جمع معلومات للدعم

```bash
# إنشاء ملف معلومات النظام
{
  echo "=== معلومات النظام ==="
  uname -a
  echo ""
  echo "=== إصدار Python ==="
  python3 --version
  echo ""
  echo "=== المتطلبات المثبتة ==="
  pip list | grep -E "telegram|Pillow|google"
  echo ""
  echo "=== حالة البوت ==="
  ps aux | grep drive_bot.py | grep -v grep || echo "البوت غير مشغّل"
  echo ""
  echo "=== آخر 20 سطر من السجل ==="
  tail -20 /home/ubuntu/bot.log
} > /home/ubuntu/support_info.txt

cat /home/ubuntu/support_info.txt
```

## ✅ قائمة التحقق الدورية

- [ ] التحقق من أن البوت يعمل: `ps aux | grep drive_bot.py`
- [ ] مراجعة السجلات للأخطاء: `tail -f /home/ubuntu/bot.log`
- [ ] إنشاء نسخة احتياطية من البيانات: `tar -czf backup.tar.gz /home/ubuntu/drive_bot_data/`
- [ ] التحقق من مساحة التخزين: `df -h`
- [ ] تحديث المتطلبات: `pip install --upgrade -r requirements.txt`
- [ ] تنظيف الملفات المؤقتة: `rm -rf /home/ubuntu/drive_bot_data/temp/*`

---

**ملاحظة**: قم بهذه الفحوصات بانتظام للحفاظ على البوت يعمل بكفاءة.
