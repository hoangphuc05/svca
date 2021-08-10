# SVCA API backend
## About
This is the Django program power the back-end of Spokane Valley Community Advocates website at https://sv-communityadvocates.org/

## Installing
### Requirements
#### This program was tested on Python 3.9

### (optional) Create new environment and use it
```shell
python3 -m venv new-env-name

# Activate
# Linux/macOS
source new-venv-name/bin/activate

# Windows
new-venv-name\bin\activate\activate.bin
```
### Installing dependencies
```shell
# Linux/macOS
pip3 install -r requirements.txt

# Windows
py -m pip install -r requirements.txt
```

### Setting up token and secret
This program relies on token from environment variables from a `.env` file in the program root folder.

`.env` example
```shell
DB_HOST=database.example.com
DB_USER=database_example_user
DB_PASSWORD=database_example_password
SECRET_KEY=django_example_secret_key
EMAIL_TOKEN=example_email_token
GOOGLE_RECAPTCHA_SECRET_KEY=google_recaptcha_secret
```
  
## Documentation
### Blog:
https://documenter.getpostman.com/view/8358593/Tzz4QK14

## Link that I clicked:
- For deploying:
    - https://blog.codeasite.com/how-do-i-find-apache-http-server-log-files/
    - https://levelup.gitconnected.com/hands-on-how-to-host-django-with-apache2-d9cd0670d51b
    - https://medium.com/@iammiracle/deploy-django-on-apache-mod-wsgi-747c6e4db9d1
    - https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/
    - https://serverfault.com/questions/216252/how-to-configure-apache-sites-available-vs-httpd-conf

- AWS CD: CodeDeploy reference:
    - https://docs.aws.amazon.com/codedeploy/latest/userguide/application-revisions-appspec-file.html#add-appspec-file-server
    - https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-files.html
    - https://github.com/aws/aws-codedeploy-agent/issues/14
    