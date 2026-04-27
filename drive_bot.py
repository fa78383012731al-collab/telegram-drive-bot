#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تلجرام لرفع الملفات إلى Google Drive
يتضمن ميزات: الضغط التلقائي، الحفظ الدائم، إدارة المشاريع
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import io

# استيراد مكتبات Telegram
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
    from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackQueryHandler
    from telegram.error import TelegramError
except ImportError:
    print("يرجى تثبيت مكتبة python-telegram-bot")
    print("pip install python-telegram-bot")
    exit(1)

# استيراد مكتبات معالجة الملفات
try:
    from PIL import Image
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("يرجى تثبيت مكتبة Pillow")
    print("pip install Pillow pillow-heif")
    exit(1)

# استيراد مكتبات Google Drive
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
# from google.colab import auth  # Removed as it's for Colab only
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

# إعداد نظام التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/ubuntu/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ثوابت المسارات
DATA_DIR = Path('/home/ubuntu/drive_bot_data')
PROJECTS_FILE = DATA_DIR / 'projects.json'
CREDENTIALS_FILE = DATA_DIR / 'credentials.json'
TEMP_DIR = DATA_DIR / 'temp'

# إنشاء المجلدات المطلوبة
DATA_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# حالات المحادثة
CHOOSING_ACTION = 1
CREATING_PROJECT = 2
SELECTING_PROJECT = 3
UPLOADING_FILE = 4
SETTING_CREDENTIALS = 5

class DriveManager:
    """مدير Google Drive"""
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.load_credentials()
    
    def load_credentials(self):
        """تحميل بيانات اعتماد Google Drive"""
        try:
            if CREDENTIALS_FILE.exists():
                self.credentials = Credentials.from_service_account_file(
                    str(CREDENTIALS_FILE),
                    scopes=['https://www.googleapis.com/auth/drive']
                )
                self.service = build('drive', 'v3', credentials=self.credentials)
                logger.info("تم تحميل بيانات اعتماد Google Drive بنجاح")
            else:
                logger.warning("لم يتم العثور على ملف بيانات الاعتماد")
        except Exception as e:
            logger.error(f"خطأ في تحميل بيانات الاعتماد: {e}")
    
    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """إنشاء مجلد جديد في Google Drive"""
        try:
            if not self.service:
                logger.error("خدمة Google Drive غير متصلة")
                return None
            
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            folder_id = folder.get('id')
            logger.info(f"تم إنشاء المجلد: {folder_name} (ID: {folder_id})")
            return folder_id
        except Exception as e:
            logger.error(f"خطأ في إنشاء المجلد: {e}")
            return None
    
    def upload_file(self, file_path: str, folder_id: str, file_name: Optional[str] = None) -> Optional[str]:
        """رفع ملف إلى Google Drive"""
        try:
            if not self.service:
                logger.error("خدمة Google Drive غير متصلة")
                return None
            
            if not os.path.exists(file_path):
                logger.error(f"الملف غير موجود: {file_path}")
                return None
            
            file_name = file_name or os.path.basename(file_path)
            
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            file_id = file.get('id')
            logger.info(f"تم رفع الملف: {file_name} (ID: {file_id})")
            return file_id
        except Exception as e:
            logger.error(f"خطأ في رفع الملف: {e}")
            return None
    
    def get_folder_link(self, folder_id: str) -> str:
        """الحصول على رابط المجلد"""
        return f"https://drive.google.com/drive/folders/{folder_id}"


class FileCompressor:
    """ضاغط الملفات"""
    
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
    
    @staticmethod
    def compress_image(image_path: str, output_path: str, quality: int = 85) -> bool:
        """ضغط صورة"""
        try:
            with Image.open(image_path) as img:
                # تحويل إلى RGB إذا لزم الأمر
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # حفظ مع ضغط
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                # التحقق من الحجم
                if os.path.getsize(output_path) > FileCompressor.MAX_FILE_SIZE:
                    # محاولة ضغط أكثر
                    return FileCompressor.compress_image(image_path, output_path, quality=quality-10)
                
                logger.info(f"تم ضغط الصورة: {image_path}")
                return True
        except Exception as e:
            logger.error(f"خطأ في ضغط الصورة: {e}")
            return False
    
    @staticmethod
    def compress_file(file_path: str, output_path: str) -> bool:
        """ضغط ملف عام"""
        try:
            file_size = os.path.getsize(file_path)
            
            if file_size <= FileCompressor.MAX_FILE_SIZE:
                # نسخ الملف بدون ضغط
                import shutil
                shutil.copy2(file_path, output_path)
                return True
            
            # محاولة ضغط باستخدام gzip
            import gzip
            import shutil
            
            with open(file_path, 'rb') as f_in:
                with gzip.open(output_path + '.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            if os.path.getsize(output_path + '.gz') <= FileCompressor.MAX_FILE_SIZE:
                os.rename(output_path + '.gz', output_path)
                logger.info(f"تم ضغط الملف: {file_path}")
                return True
            else:
                os.remove(output_path + '.gz')
                logger.error(f"لم يتمكن من ضغط الملف إلى الحد المسموح: {file_path}")
                return False
        except Exception as e:
            logger.error(f"خطأ في ضغط الملف: {e}")
            return False


class ProjectManager:
    """مدير المشاريع"""
    
    def __init__(self):
        self.projects = self.load_projects()
    
    def load_projects(self) -> Dict:
        """تحميل المشاريع من ملف JSON"""
        try:
            if PROJECTS_FILE.exists():
                with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"خطأ في تحميل المشاريع: {e}")
        return {}
    
    def save_projects(self):
        """حفظ المشاريع في ملف JSON"""
        try:
            with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.projects, f, ensure_ascii=False, indent=2)
            logger.info("تم حفظ المشاريع بنجاح")
        except Exception as e:
            logger.error(f"خطأ في حفظ المشاريع: {e}")
    
    def create_project(self, project_name: str, user_id: int, folder_id: str) -> bool:
        """إنشاء مشروع جديد"""
        try:
            user_key = str(user_id)
            if user_key not in self.projects:
                self.projects[user_key] = {}
            
            self.projects[user_key][project_name] = {
                'folder_id': folder_id,
                'created_at': datetime.now().isoformat(),
                'files_count': 0
            }
            
            self.save_projects()
            logger.info(f"تم إنشاء المشروع: {project_name} للمستخدم: {user_id}")
            return True
        except Exception as e:
            logger.error(f"خطأ في إنشاء المشروع: {e}")
            return False
    
    def get_user_projects(self, user_id: int) -> Dict:
        """الحصول على مشاريع المستخدم"""
        return self.projects.get(str(user_id), {})
    
    def get_project(self, user_id: int, project_name: str) -> Optional[Dict]:
        """الحصول على تفاصيل مشروع معين"""
        user_projects = self.get_user_projects(user_id)
        return user_projects.get(project_name)
    
    def update_project(self, user_id: int, project_name: str, data: Dict):
        """تحديث بيانات المشروع"""
        try:
            user_key = str(user_id)
            if user_key in self.projects and project_name in self.projects[user_key]:
                self.projects[user_key][project_name].update(data)
                self.save_projects()
                return True
        except Exception as e:
            logger.error(f"خطأ في تحديث المشروع: {e}")
        return False


class TelegramBot:
    """بوت تلجرام الرئيسي"""
    
    def __init__(self, token: str):
        self.token = token
        self.drive_manager = DriveManager()
        self.project_manager = ProjectManager()
        self.user_context = {}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /start"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        welcome_message = f"""
مرحباً بك {user_name}! 👋

أنا بوت رفع الملفات إلى Google Drive.

يمكنني مساعدتك في:
✅ إنشاء مشاريع جديدة
✅ رفع الملفات والصور تلقائياً
✅ ضغط الملفات الكبيرة تلقائياً
✅ إدارة المشاريع السابقة

اختر ما تريد:
"""
        
        keyboard = [
            [KeyboardButton("📁 مشروع جديد"), KeyboardButton("📂 مشاريعي")],
            [KeyboardButton("⚙️ الإعدادات"), KeyboardButton("ℹ️ معلومات")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        return CHOOSING_ACTION
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل العامة"""
        text = update.message.text
        user_id = update.effective_user.id
        
        if text == "📁 مشروع جديد":
            await update.message.reply_text("أدخل اسم المشروع الجديد:")
            return CREATING_PROJECT
        
        elif text == "📂 مشاريعي":
            projects = self.project_manager.get_user_projects(user_id)
            if not projects:
                await update.message.reply_text("لا توجد مشاريع لديك حالياً.")
                return CHOOSING_ACTION
            
            project_list = "\n".join([f"• {name}" for name in projects.keys()])
            await update.message.reply_text(f"مشاريعك:\n\n{project_list}")
            return CHOOSING_ACTION
        
        elif text == "⚙️ الإعدادات":
            await update.message.reply_text(
                "الإعدادات:\n\n"
                "1. يجب تحميل ملف بيانات اعتماد Google Drive (credentials.json)\n"
                "2. ضع الملف في: /home/ubuntu/drive_bot_data/credentials.json"
            )
            return CHOOSING_ACTION
        
        elif text == "ℹ️ معلومات":
            await update.message.reply_text(
                "معلومات البوت:\n\n"
                "🤖 بوت رفع الملفات إلى Google Drive\n"
                "📦 الإصدار: 2.0\n"
                "✨ الميزات:\n"
                "  • ضغط تلقائي للملفات\n"
                "  • حفظ دائم للمشاريع\n"
                "  • إدارة المشاريع\n"
                "  • دعم جميع أنواع الملفات"
            )
            return CHOOSING_ACTION
        
        return CHOOSING_ACTION
    
    async def create_project(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إنشاء مشروع جديد"""
        project_name = update.message.text
        user_id = update.effective_user.id
        
        # إنشاء مجلد في Google Drive
        folder_id = self.drive_manager.create_folder(project_name)
        
        if folder_id:
            self.project_manager.create_project(project_name, user_id, folder_id)
            folder_link = self.drive_manager.get_folder_link(folder_id)
            
            await update.message.reply_text(
                f"✅ تم إنشاء المشروع '{project_name}' بنجاح!\n\n"
                f"رابط المجلد: {folder_link}\n\n"
                f"يمكنك الآن رفع الملفات إلى هذا المشروع."
            )
        else:
            await update.message.reply_text(
                "❌ حدث خطأ في إنشاء المشروع.\n"
                "تأكد من أن بيانات اعتماد Google Drive مثبتة بشكل صحيح."
            )
        
        return CHOOSING_ACTION
    
    async def handle_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الملفات المرفوعة"""
        user_id = update.effective_user.id
        
        # الحصول على المشاريع
        projects = self.project_manager.get_user_projects(user_id)
        
        if not projects:
            await update.message.reply_text("لا توجد مشاريع لديك. أنشئ مشروعاً أولاً.")
            return CHOOSING_ACTION
        
        # إنشاء لوحة مفاتيح لاختيار المشروع
        keyboard = []
        for project_name in projects.keys():
            keyboard.append([InlineKeyboardButton(project_name, callback_data=f"project_{project_name}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("اختر المشروع لرفع الملف إليه:", reply_markup=reply_markup)
        
        # حفظ الملف المؤقت
        if update.message.document:
            file = await update.message.document.get_file()
            temp_path = TEMP_DIR / f"{user_id}_{update.message.document.file_name}"
            await file.download_to_drive(str(temp_path))
            self.user_context[user_id] = {'file_path': str(temp_path), 'file_name': update.message.document.file_name}
        elif update.message.photo:
            file = await update.message.photo[-1].get_file()
            temp_path = TEMP_DIR / f"{user_id}_photo.jpg"
            await file.download_to_drive(str(temp_path))
            self.user_context[user_id] = {'file_path': str(temp_path), 'file_name': 'photo.jpg'}
        
        return UPLOADING_FILE
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أزرار الاختيار"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        if data.startswith("project_"):
            project_name = data.replace("project_", "")
            project = self.project_manager.get_project(user_id, project_name)
            
            if not project or user_id not in self.user_context:
                await query.edit_message_text("حدث خطأ. يرجى المحاولة مرة أخرى.")
                return
            
            file_info = self.user_context[user_id]
            file_path = file_info['file_path']
            file_name = file_info['file_name']
            
            # ضغط الملف إذا لزم الأمر
            compressed_path = TEMP_DIR / f"compressed_{file_name}"
            
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                FileCompressor.compress_image(file_path, str(compressed_path))
                upload_path = str(compressed_path)
            else:
                FileCompressor.compress_file(file_path, str(compressed_path))
                upload_path = str(compressed_path) if os.path.exists(str(compressed_path)) else file_path
            
            # رفع الملف
            file_id = self.drive_manager.upload_file(upload_path, project['folder_id'], file_name)
            
            if file_id:
                # تحديث عدد الملفات
                self.project_manager.update_project(
                    user_id,
                    project_name,
                    {'files_count': project.get('files_count', 0) + 1}
                )
                
                await query.edit_message_text(
                    f"✅ تم رفع الملف '{file_name}' بنجاح!\n"
                    f"المشروع: {project_name}"
                )
            else:
                await query.edit_message_text("❌ حدث خطأ في رفع الملف.")
            
            # تنظيف الملفات المؤقتة
            try:
                os.remove(file_path)
                if os.path.exists(str(compressed_path)):
                    os.remove(str(compressed_path))
            except:
                pass
            
            del self.user_context[user_id]
    
    def run(self):
        """تشغيل البوت"""
        app = Application.builder().token(self.token).build()
        
        # معالجات الأوامر
        app.add_handler(CommandHandler("start", self.start))
        
        # معالج المحادثة
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                CHOOSING_ACTION: [
                    MessageHandler(filters.TEXT, self.handle_message),
                    MessageHandler(filters.Document.ALL | filters.PHOTO, self.handle_file)
                ],
                CREATING_PROJECT: [
                    MessageHandler(filters.TEXT, self.create_project)
                ],
                UPLOADING_FILE: [
                    CallbackQueryHandler(self.button_callback)
                ]
            },
            fallbacks=[CommandHandler("start", self.start)]
        )
        
        app.add_handler(conv_handler)
        app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # معالج الملفات
        app.add_handler(MessageHandler(
            filters.Document.ALL | filters.PHOTO,
            self.handle_file
        ))
        
        logger.info("بدء تشغيل البوت...")
        app.run_polling()


def main():
    """الدالة الرئيسية"""
    # الحصول على التوكن من متغير البيئة
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("يرجى تعيين متغير البيئة TELEGRAM_BOT_TOKEN")
        print("export TELEGRAM_BOT_TOKEN='your_token_here'")
        exit(1)
    
    bot = TelegramBot(token)
    bot.run()


if __name__ == '__main__':
    main()
