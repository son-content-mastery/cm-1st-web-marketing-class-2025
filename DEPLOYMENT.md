# Deploy Django

## Install Dependencies

```sh
apt update && sudo apt upgrade -y
apt install python3-pip python3-venv nginx -y
```

## Config GIT

```sh
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

## Clone Django Project

Clone your django repository

```sh
cd /var/www
git clone https://your-repo.git django_project
cd django_project
```

## Step 3: Setup Python Virtual Environment

> Create and activate a Python virtual environment:

```sh
python3 -m venv env
source env/bin/activate
```

> Install required packages:

```sh
pip install -r requirements.txt
pip install gunicorn
```

> Prepare the Database

```sh
python manage.py makemigrations
python manage.py migrate
```

> Check Overall working

`python manage.py runserver 0.0.0.0:8000`

> Run collect static files:

`python manage.py collectstatic --noinput`

> Run Test Gunicorn:

`gunicorn --bind 0.0.0.0:8000 mysite.wsgi.application`

# Setup Linux user

```sh
adduser django-app

sudo chown -R django-app:django-app /home/youruser/django_project

sudo su - django-app
```

## Setup Gunicorn as a Systemd Service

### Create guni

`vi /etc/systemd/system/gunicorn.service`

```sh
[Unit]
Description=Gunicorn Daemon for Django Project
After=network.target

[Service]
User=django-app
Group=django-app
WorkingDirectory=/var/www/cm-1st-web-marketing-class-2025
ExecStart=/var/www/cm-1st-web-marketing-class-2025/env/bin/gunicorn --workers 3 --bind unix:/var/www/cm-1st-web-marketing-class-2025/gunicorn.sock mysite.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Reload the Gunicorn

```sh
systemctl daemon-reload
systemctl restart gunicorn
systemctl enable gunicorn
```

### Recheck Gunicorn

`ps aux | grep gunicorn`

## Configure Nginx (Static & Media Files)

### Create an Nginx configuration file for your Django project.

```sh
vi /etc/nginx/sites-available/django_project
```

> Add this config

```sh
server {
    listen 80;
    server_name www.wizzops.cloud wizzops.cloud;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }

    location /static/ {
        alias /var/www/cm-1st-web-marketing-class-2025/staticfiles/;
    }

    location /media/ {
        alias /var/www/cm-1st-web-marketing-class-2025/media/;
    }

    client_max_body_size 100M;
}
```

> Link the config file to sites-enabled

`ln -s /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/`

> Test and Restart Nginx

```sh
nginx -t

systemctl reload nginx.service
```

### Install and Config SSL

> Run the following command to install Certbot

`apt install certbot python3-certbot-nginx -y`

> Check certbot install

`certbot --version`

### Generate cert

> Run the command line

`certbot --nginx -d wizzops.cloud -d www.wizzops.cloud`

### Recheck Certificate on nginx config

`vi /etc/nginx/sites-available/django_project`

### Recheck and Reload Nginx config

```sh
nginx -t

systemctl reload nginx.service
```

### Automatic Renewal SSL Certificate Renewal

- Setup crontab to do the job `crontab -e`
- Add this config `0 3 */80 * * certbot renew --quiet && systemctl restart nginx`
  - ```sh
    •	0 3 → Run at 3:00 AM.
	•	*/80 → Run every 80 days.
	•	certbot renew --quiet → Renews SSL only if needed.
	•	&& systemctl restart nginx → Restarts Nginx to apply new SSL certificate.
    ```

### Test Cerbot Renewal

`certbot renew --dry-run`

## Create Superuser Django app

`python manage.py createsuperuser`
