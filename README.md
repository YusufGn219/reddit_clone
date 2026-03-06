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

# Proje Yapısı

```
reddit_clone/
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── posts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── posts/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── create.html
│       │   └── update.html
│       └── base.html
├── communities/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── communities/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── create.html
│       │   └── update.html
│       └── base.html
├── users/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── users/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── create.html
│       │   └── update.html
│       └── base.html
├── static/
└── templates/
```

## Projede kullanılan teknolojiler

- Django
- HTML
- CSS
- JavaScript
- Bootstrap
- SQLite

