## Docker
### Build and Start Docker Containers
```
docker compose up --build -d
```
### Access Django's Shell
```
docker exec -it django_app sh
```

## Django
### Make Migrations
```
python manage.py makemigrations
```
### Apply Migrations
```
python manage.py migrate
```
### Create superuser (if not done already)
```
python manage.py createsuperuser
```
### Restart Django Container
```
docker-compose restart django 
```
### Extract SQL from database
```
python manage.py inspectdb > models.py
```
### Extract SQL code from migration
```
python manage.py sqlmigrate inventory 0001
```








{
  "name": "stsdring",
  "slug": "xsAlb_29_JJg6aaGdLRmW18mO0Ye8dAw6kAyvelsCBG2wcxk",
  "description": "string",
  "is_digital": true,
  "is_active": true,
  "price": "-22.39",
 "new_category": {
    "name": "Example Category"
  },
  "stock": {
    "quantity": 2147483647
  }
}