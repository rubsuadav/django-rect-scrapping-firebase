[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aab804dc1a06435f868a50c655c66c53)](https://app.codacy.com/gh/rubsuadav/django-rect-scrapping-firebase?utm_source=github.com&utm_medium=referral&utm_content=rubsuadav/django-rect-scrapping-firebase&utm_campaign=Badge_Grade)

# INSTALLATION

## 1. Clone this repository

```bash
git clone https://github.com/rubsuadav/django-rect-scrapping-firebase.git
```

## 2. Create a virtualenv

```bash
python -m venv venv
```

## 3. Activate virtualenv

### 3.1. Windows

```bash
.\venv\Scripts\activate
```

### 3.2. Linux

```bash
source venv/bin/activate
```

### 4. Install requirements

```bash
pip install -r requirements.txt
```

### 5. Run project

```bash
python manage.py runserver
```

### NOTE:

<p>You need to have a firebase account and create a project to use this project
and put the credentials in the local_settings.py file,
IF YOU DON'T HAVE A FIREBASE ACCOUNT, YOU CAN'T RUN THE API SERVER</p>

## NOTE2:

<p>You need to activate the authentication method with email and password in the
firebase console. Also, install the stripe/firestore-stripe-payments extension
in your firebase project using a stripe SECRET_KEY. Follow the instructions
on the extension page.</p>
