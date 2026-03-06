# Reddit Clone

Django kullanarak, reddit platformunun temel özelliklerini barındıran bir web uygulamasıdır.

## Özellikler


- Gönderi, Topluluk oluşturma ve görüntüleme
- Topluluk oluşturma ve katılma
- Kullanıcı kaydı ve girişi
- Kullanıcı profilleri
- Beğeni ve beğenmeme
- Oylama sistemi
- Yorum yapma
- Arama

## Kurulum
 
### Gereksinimler

- Python 3.10+
- pip

### Çalıştırma adımları

1. Repoyu klonlayın:
```bash
git clone https://github.com/kullanici/reddit-clone.git
cd reddit-clone
```

2. Sanal ortam oluşturun:
```bash
python -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
python.exe -m venv venv
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. .env dosyasını oluşturun:
```bash
cp .env.example .env
```

5. Veritabanını oluşturun:
```bash
python manage.py migrate
```

5. Geliştirme sunucusunu başlatın:
```bash
python manage.py runserver
```

6. Tarayıcınızda http://localhost:8000 adresine gidin.

## Proje Yapısı

reddit_clone/
├── .env.example
├── .gitignore
├── README.md
└── reddit_clone/
    ├── accounts/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── context_processors.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    │
    ├── communities/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── permissions.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── views.py
    │
    ├── config/
    │   ├── settings/
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── dev.py
    │   │   └── prod.py
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── posts/
    │   ├── migrations/
    │   ├── services/
    │   │   ├── comments.py
    │   │   ├── querysets.py
    │   │   └── sorting.py
    │   ├── templatetags/
    │   │   ├── __init__.py
    │   │   └── markdown_extras.py
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    │
    ├── static/
    │   └── css/
    │
    ├── templates/
    │   ├── accounts/
    │   │   ├── login.html
    │   │   ├── notifications.html
    │   │   ├── profile.html
    │   │   └── register.html
    │   ├── communities/
    │   │   ├── add_moderator.html
    │   │   ├── community_create.html
    │   │   ├── community_detail.html
    │   │   ├── community_edit.html
    │   │   └── rule_add.html
    │   ├── posts/
    │   │   ├── partials/
    │   │   ├── home_feed.html
    │   │   ├── post_create.html
    │   │   └── post_detail.html
    │   ├── search/
    │   │   └── results.html
    │   ├── 403.html
    │   ├── 404.html
    │   ├── base.html
    │   └── home.html
    │
    ├── votes/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── services.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    │
    ├── manage.py
    └── requirements.txt


## Modüllerin Görevleri

Her klasör belirli bir sorumluluk alanına odaklanır ve projenin bakımını, geliştirilmesini ve ölçeklenmesini kolaylaştırır.

### accounts/
Kullanıcı kimlik doğrulama, kayıt, giriş, profil ve kullanıcıya bağlı yardımcı işlemleri içerir.

### communities/
Topluluk oluşturma, düzenleme, moderasyon işlemleri, topluluk kuralları ve topluluğa özgü yetki kontrollerini yönetir.

### config/
Projenin merkezi yapılandırma katmanıdır.  
URL yönlendirmeleri, WSGI/ASGI giriş noktaları ve ortam bazlı ayarlar burada bulunur.

### posts/
Gönderi ve yorum odaklı ana içerik katmanıdır.  
Ayrıca servis mantıkları (services/) ve özel template tag yapıları da bu modül altında yer alır.

### static/
Projenin ortak statik dosyalarını barındırır.  
CSS gibi arayüz varlıkları bu klasörde tutulur.

### templates/
Tüm uygulamalar tarafından kullanılan HTML şablonlarını içerir.  
Sayfa yapısı, ortak layout'lar ve uygulamaya özel template dosyaları burada yer alır.

### votes/
Gönderi ve yorumlar üzerindeki oy verme / oy geri çekme mantığını yönetir.

### manage.py
Django komutlarının çalıştırıldığı ana giriş dosyasıdır.

### requirements.txt
Projede kullanılan Python bağımlılıklarını listeler.


## Projede kullanılan teknolojiler

- Django
- HTML
- CSS
- JavaScript
- Bootstrap
- SQLite

