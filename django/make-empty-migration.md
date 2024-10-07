
If you want to make a new migration where you are going to do some work programmatically. 
You can scaffold the migration by doing.
You want to do: 

```
python manage.py makemigrations --empty <app_name>
```

I do most of my work in containers these days, so to 
spin up new django container and running bash command you can do

```
docker compose --file=local.yml run --rm  django python manage.py makemigrations --empty django-app-name
```