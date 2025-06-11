# 📚 BookStation

**BookStation** là một ứng dụng web quản lý sách được xây dựng bằng Django 🌐.

🔗 [Truy cập ứng dụng tại đây](https://bookstation-vjjf.onrender.com/)

---

## 📸 Giao diện

<img src="https://res.cloudinary.com/djsjtslen/image/upload/v1748625495/webpage_rcmpaz.png" width="600"/>
<img src="https://res.cloudinary.com/djsjtslen/image/upload/v1748625495/webpage2_noa6on.png" width="600"/>
<img src="https://res.cloudinary.com/djsjtslen/image/upload/v1748625643/webpage3_mzmfum.png" width="600"/>
<img src="https://res.cloudinary.com/djsjtslen/image/upload/v1748625643/webpage4_mihxjx.png" width="600"/>

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

### 4. ⚙️ Cấu hình
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

---

### 5. 🧪 Chạy ứng dụng với django

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📄 Requirements
```
﻿asgiref==3.8.1
Django==5.2.1
django-widget-tweaks==1.5.0
et_xmlfile==2.0.0
mysqlclient==2.2.7
numpy==1.26.4
openpyxl==3.1.5
pandas==2.1.3
pillow==11.2.1
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
sqlparse==0.5.3
tzdata==2025.2
Unidecode==1.4.0
```
##  Cấu trúc dự án
```
BookStation
│   manage.py
│   requirements.txt
│   
│   
├───accounts
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_alter_users_phone.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-311.pyc
│   │           0002_alter_users_phone.cpython-311.pyc
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   └───accounts
│   │           base.html
│   │           edit_profile.html
│   │           login.html
│   │           profile.html
│   │           register.html
│   │           
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           forms.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───analytics
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   └───analytics
│   │           book_inventory_detail.html
│   │           customer_stats.html
│   │           dashboard.html
│   │           order_stats.html
│   │           
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───books
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_alter_author_birth_date.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-311.pyc
│   │           0002_alter_author_birth_date.cpython-311.pyc
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   ├───authors
│   │   │       author_confirm_delete.html
│   │   │       author_detail.html
│   │   │       author_form.html
│   │   │       author_list.html
│   │   │       
│   │   ├───books
│   │   │       book_confirm_delete.html
│   │   │       book_detail.html
│   │   │       book_form.html
│   │   │       book_list.html
│   │   │       search_results.html
│   │   │       
│   │   ├───categories
│   │   │       category_confirm_delete.html
│   │   │       category_detail.html
│   │   │       category_form.html
│   │   │       category_list.html
│   │   │       
│   │   └───publishers
│   │           publisher_confirm_delete.html
│   │           publisher_detail.html
│   │           publisher_form.html
│   │           publisher_list.html
│   │           
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           forms.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───BookStation
│   │   .gitignore
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │   
│   ├───templates
│   │       base.html
│   │       
│   └───__pycache__
│           settings.cpython-311.pyc
│           urls.cpython-311.pyc
│           wsgi.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───home
│   │   admin.py
│   │   apps.py
│   │   middleware.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   └───home
│   │           home.html
│   │           
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           middleware.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───media
│   ├───author
│   │       ToHoai_trong.jpg
│   │       victorhugo.webp
│   │       victorhugo_vwvL8TO.webp
│   │       
│   └───book_covers
│           1984.jpg
│           1984_fDPUJc3.jpg
│           atomic_habits.jpg
│           book_1.jpg
│           book_10.jpg
│           book_11.jpg
│           book_12.jpg
│           book_13.jpg
│           book_14.jpg
│           book_15.jpg
│           book_16.jpg
│           book_17.jpg
│           book_18.jpg
│           book_19.jpg
│           book_2.jpg
│           book_20.jpg
│           book_3.jpg
│           book_4.jpg
│           book_5.jpg
│           book_6.jpg
│           book_7.jpg
│           book_8.jpg
│           book_9.jpg
│           Dacnhantam.jpg
│           demen1.jpg
│           educated.jpg
│           harry_potter_and_the_sorcerers_stone.jpg
│           jane_eyre.jpg
│           ngkk.webp
│           nhungnguoikhonkho_kwqGLyc.jpg
│           pride_and_prejudice.jpg
│           silent_patient.jpg
│           sukk1.jpg
│           the_catcher_in_the_rye.jpg
│           the_chronicles_of_narnia.jpg
│           the_da_vinci_code.jpg
│           the_great_gatsby.jpg
│           the_hobbit.jpg
│           to_kill_a_mockingbird.jpg
│           vu.jpg
│           
├───orders
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_order_payment_method_alter_order_status.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-311.pyc
│   │           0002_order_payment_method_alter_order_status.cpython-311.pyc
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   └───orders
│   │           base.html
│   │           cart.html
│   │           create_order.html
│   │           order_list.html
│   │           order_success.html
│   │           
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           forms.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───reviews
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_alter_review_book_delete_book.py
│   │   │   0003_review_rating.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-311.pyc
│   │           0002_alter_review_book_delete_book.cpython-311.pyc
│   │           0003_review_rating.cpython-311.pyc
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   └───reviews
│   │           add_reviews.html
│   │           book_review.html
│   │           
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           forms.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───staff
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   test.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           __init__.cpython-311.pyc
│   │           
│   ├───templates
│   │   └───staff
│   │       │   dashboard_staff.html
│   │       │   
│   │       ├───accounts
│   │       │       add_users.html
│   │       │       change_user.html
│   │       │       list_users.html
│   │       │       
│   │       └───books
│   │               add_author.html
│   │               add_book.html
│   │               add_category.html
│   │               add_publisher.html
│   │               change_author.html
│   │               change_book.html
│   │               change_category.html
│   │               change_publisher.html
│   │               view_author.html
│   │               view_book.html
│   │               view_category.html
│   │               view_publisher.html
│   │               
│   └───__pycache__
│           admin.cpython-311.pyc
│           apps.cpython-311.pyc
│           forms.cpython-311.pyc
│           models.cpython-311.pyc
│           urls.cpython-311.pyc
│           views.cpython-311.pyc
│           __init__.cpython-311.pyc
│           
├───static
│   ├───css
│   │   ├───analytics
│   │   │       analytics.css
│   │   │       book_inventory_detail.css
│   │   │       customer_analysis.css
│   │   │       customer_stats.css
│   │   │       order_stats.css
│   │   │       
│   │   ├───author_detail
│   │   │       style.css
│   │   │       
│   │   ├───author_list
│   │   │       style.css
│   │   │       
│   │   ├───base
│   │   │       style.css
│   │   │       
│   │   ├───books
│   │   │       style.css
│   │   │       
│   │   ├───books_list
│   │   │       style.css
│   │   │       
│   │   ├───book_detail
│   │   │       style.css
│   │   │       
│   │   ├───category_detail
│   │   │       style.css
│   │   │       
│   │   ├───category_list
│   │   │       style.css
│   │   │       
│   │   ├───edit_profile
│   │   │       style.css
│   │   │       
│   │   ├───home
│   │   │       slide.css
│   │   │       style.css
│   │   │       
│   │   ├───login
│   │   │       style.css
│   │   │       
│   │   ├───profile
│   │   │       style.css
│   │   │       
│   │   ├───publisher_detail
│   │   │       style.css
│   │   │       
│   │   ├───publisher_list
│   │   │       style.css
│   │   │       
│   │   ├───register
│   │   │       style.css
│   │   │       
│   │   ├───search_results
│   │   │       style.css
│   │   │       
│   │   └───staff
│   │           style.css
│   │           
│   ├───image
│   │       Bachkhoadialy.jpg
│   │       demen.jpg
│   │       demen1.jpg
│   │       images1.jpg
│   │       tuduynhanhcham.jpeg
│   │       yourname.gif
│   │       yourname.jpg
│   │       
│   └───js
│       │   analytics.js
│       │   
│       ├───analytics
│       │       customer_stats.js
│       │       order_stats.js
│       │       
│       ├───base
│       │       script.js
│       │       
│       ├───book_detail
│       │       quantity-control.js
│       │       
│       └───home
│               banner_slider.js
│               script.js
│               
└───templates
        base.html
        
```
## 📝 Ghi chú

- Thư mục `venv/` đã được bỏ qua nhờ `.gitignore`.
- Nếu gặp lỗi `git push`, hãy chắc chắn bạn đã `git pull` trước đó.

---
## 📄 License

This project is licensed under the [MIT License](LICENSE).



