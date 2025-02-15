# Django Project

## Setup

1. Install docker desktop
2. Add a volume to persist data. Change the path in the docker-compose.yml file. 
3. Update the docker-compose.yml file with your resend api key.
4. Run `docker compose up --build`

Send a POST request to the endpoint to evaluate a prompt.

```bash
curl -X POST http://localhost:8000/evaluate -H "Content-Type: application/json" -d '{"input_prompt": "Sample prompt"}'
```

The pgadmin service mentioned inside the docker-compose.yml file is used to view the database.
You can access it by going to http://localhost:5050. The default credentials are:

```
Email: admin@example.com
Password: admin
Host: db
Port: 5432
Username: postgres
Password: 1234
```

You can change the credentials in the docker-compose.yml file.

If you change the name of the services in docker-compose.yml file, you need to update the host in settings.py file. 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'db',
        'PORT': '5432',
    }
}
CELERY_BROKER_URL=redis://redis:6379/0
```






