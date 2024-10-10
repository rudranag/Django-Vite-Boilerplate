# Setting up Backend

## Creating virtual environment

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt

```
## Setup Django

```
python manage.py migrate
```

## Run Backend

```
python manage.py runserver 0.0.0.0:8000
```

# Setting up Frontend

```
cd frontend
npm install

```

## Run frontend

```
npm run dev
```


# Enable Debug Toolbar 

Go to BASEDIR

```
echo "ENABLE_DEBUG_TOOLBAR=True" >> .env
```




# Swagger Docs


```
http://127.0.0.1:8000/swagger/
```


# React Todo Page


```
http://127.0.0.1:8000/r/todo
```
