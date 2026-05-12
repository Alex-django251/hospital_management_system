pip install -r requirements.txt   # install packages
python manage.py collectstatic --noinput  # collect static files
python manage.py migrate --noinput        # run database migrations
