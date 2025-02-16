# Deploy Django

## Step 1: Install Linux Dependencies

```sh
apt update && sudo apt upgrade -y
apt install python3-pip python3-venv nginx -y
```

## Step 2: Configure Git

```sh
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

## Step 3: Clone Django Project

> Clone your django repository

```sh
cd /var/www
git clone https://your-repo.git django_project
cd django_project
```

## Step 4: Setup Python Virtual Environment
sudo systemctl status gunicorn
### Create and activate a Python virtual environment:

```sh
python3 -m venv env
source env/bin/activate
```

### Install required packages:

```sh
pip install -r requirements.txt
pip install gunicorn
```

## Step 5: Prepare the Database

### Prepare the Database

```sh
python manage.py makemigrations
python manage.py migrate
```

### createsuperuser

```sh
python manage.py createsuperuser
```

## Step 6: Check Django Setup

> Check Overall working

```sh
python manage.py runserver 0.0.0.0:8000
```

## Step 7: Collect Static Files

> Run collect static files:

`python manage.py collectstatic --noinput`

## Step 8: Test Gunicorn Manually

> Run Test Gunicorn:

`gunicorn --bind 0.0.0.0:8000 mysite.wsgi:application`

## Step 9: Setup a Dedicated Linux User for Django

> Create a new user:

`adduser django-app`

> Change ownership of the Django project:

`chown -R django-app:django-app /home/youruser/django_project`

> Switch to the new user:

`sudo su - django-app`

## Step 10: Configure Gunicorn with Systemd

> Create a systemd service for Gunicorn:

`vi /etc/systemd/system/gunicorn.service`

> Paste the following:

```sh
[Unit]
Description=Gunicorn Daemon for Django Project
After=network.target

[Service]
User=django-app
Group=django-app
WorkingDirectory=/var/www/cm-1st-web-marketing-class-2025
ExecStart=/var/www/cm-1st-web-marketing-class-2025/env/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 mysite.wsgi:application

[Install]
WantedBy=multi-user.target
```

> Reload the Gunicorn

```sh
systemctl daemon-reload
systemctl restart gunicorn
systemctl enable gunicorn
```

> Check if Gunicorn is running:

`ps aux | grep gunicorn`

## Step 11: Configure Nginx to Serve Django App

### Create an Nginx configuration file for your Django project.

```sh
vi /etc/nginx/sites-available/django_project
```

> Paste the following configuration:

```sh
server {
   listen 80;
   listen [::]:80;
   server_name www.wizzops.cloud;
   return 301 http://wizzops.cloud$request_uri;
}

server {
   listen 80;
   listen [::]:80;
   server_name wizzops.cloud;

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

## Step 12: Enable and Restart Nginx

> Link the config file to sites-enabled

`ln -s /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/`

> Test Nginx configuration:

`nginx -t`

> Restart Nginx:

`systemctl reload nginx.service`

## Step 13: Install & Configure SSL (Let’s Encrypt)

### Install Certbot

`apt install certbot python3-certbot-nginx -y`

### Verify Certbot Installation

`certbot --version`

### Generate SSL Certificate

> Run the command line

- `certbot --nginx -d yourdomain.com -d www.yourdomain.com`
- `certbot --nginx -d wizzops.cloud -d www.wizzops.cloud`

### Verify SSL Configuration in Nginx

> Check the file:

`vi /etc/nginx/sites-available/django_project`

> You should see lines like:

```sh
ssl_certificate /etc/letsencrypt/live/wizzops.cloud/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/wizzops.cloud/privkey.pem;
```

> Restart Nginx:

`systemctl reload nginx.service`

## Step 14: Setup Auto-Renewal for SSL

- Setup crontab to do the job `crontab -e`
- Add this line at the bottom `0 3 */80 * * certbot renew --quiet && systemctl restart nginx`

```sh
•	0 3 → Run at 3:00 AM.
•	*/80 → Run every 80 days.
•	certbot renew --quiet → Renews SSL only if needed.
•	&& systemctl restart nginx → Restarts Nginx to apply new SSL certificate.
```

## Step 15: Test SSL Renewal

> To test renewal:

`certbot renew --dry-run`

## Step 16: Adjust Firewall Rules

> Ensure the firewall allows web traffic:

```sh
ufw allow 'Nginx Full'
ufw allow 'OpenSSH'
```

> Check firewall status:

`sudo ufw status`

## Step 17: Reboot and Final Check

```sh
systemctl status gunicorn
systemctl status nginx
```

## Reference

- [how-to-set-up-a-firewall-with-ufw-on-ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu)
