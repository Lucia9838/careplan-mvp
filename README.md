# Care Plan MVP

## Structure
```
careplan-mvp/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── app/
    ├── manage.py
    ├── careplan/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── core/
        ├── __init__.py
        ├── urls.py
        ├── views.py
        └── templates/
            └── index.html
```

## Run
```bash
# Set your Anthropic API key in docker-compose.yml, then:
docker-compose up --build
# Visit http://localhost:8000
```
