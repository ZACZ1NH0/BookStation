# 📚 BookStation

Một ứng dụng web quản lý sách được xây dựng bằng Python 🐍 và Django 🌐.

---

## 🚀 Bắt đầu

### 1. 📥 Clone dự án

```bash
git clone https://github.com/ZACZ1NH0/BookStation.git
cd BookStation
```

---

### 2. 🐍 Tạo môi trường ảo với Python 3.11 (nếu chưa tạo)

> ⚠️ Đảm bảo bạn đã cài Python 3.11 trước đó.

```bash
py -3.11 -m venv venv
```

Kích hoạt môi trường ảo:

- **Windows (PowerShell):**

```powershell
.\venv\Scripts\activate.ps1
```

- **Windows (CMD):**

```cmd
.\venv\Scripts\activate.bat
```
hoặc
```cmd
.\venv\Scripts\activate
```

- **macOS/Linux:**

```bash
source venv/bin/activate
```

---

### 3. 📦 Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

---

### 4. ⚙️ Cấu hình (nếu có)

> Thêm các thông tin như database, biến môi trường vào `.env` hoặc `settings.py` tùy dự án.

---

### 5. 🧪 Chạy ứng dụng với django
##với mysql (recommend với mysql workbench)

**tạo database bookstore_db**

**dùng user root với mật khẩu 1234**

**cổng 3306**

**file settings**
```settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookstore_db',
        'USER': 'root',                 # Username của MySQL
        'PASSWORD': '1234',     # Password của MySQL
        'HOST': 'localhost',            # Hoặc IP của DB server
        'PORT': '3306',                 # Cổng mặc định
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}
```
```bash
python manage.py migrate
python manage.py runserver
```

---

## 📄 Requirements

- asgiref==3.8.1
- Django==5.2.1
- mysqlclient==2.2.7
- sqlparse==0.5.3
- tzdata==2025.2
---

## 📝 Ghi chú

- Thư mục `venv/` đã được bỏ qua nhờ `.gitignore`.
- Nếu gặp lỗi `git push`, hãy chắc chắn bạn đã `git pull` trước đó.

---

## 💡 Tác giả

**ZACZ1NH0**  
📧 [Liên hệ qua GitHub](https://github.com/ZACZ1NH0)


