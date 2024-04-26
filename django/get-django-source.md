I have done this a bunch, but I don't do it every day
so I forget. 

A process to get the source is

```
cd ~/workspace/OpenSource
mkdir django-4.2.8
cd django-4.2.8
```

A process to install the package is
```
cd ~/workspace/OpenSource
mkdir django-4.2.8
cd django-4.2.8
vi requirements.txt
-- add line --
django==4.2.8 # https://www.djangoproject.com/
-- save --
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ln -s .venv/lib/python3.12/site-packages/django django
cd django
git init
git status
git add .
git commit -m"4.2.8"
```
Now if you change any of the django source you can see your changes