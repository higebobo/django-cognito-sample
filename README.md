# Using AWS Cognito in Django without client secret

## Overview

[django\-cognito\-redux](https://pypi.org/project/django-cognito-redux/) is one of the [Django](https://www.djangoproject.com/) authentication libraries.  
It's fine working with Django 3.x.  

But, sharing the same cognito user pool with other web application, for examle [Vue.js](https://vuejs.org/), there is a problem.

Django-cognito-redux required the client secret key of the cognito application client.  
So, override the original function, can be solved.

This is a simple sample about this.

## Prerequisites

You have already been created User pool in AWS (require `USER_PASSWORD_AUTH` permission)

## Set up

Clone this repository

```shell
git clone git@github.com:higebobo/django-cognito-sample.git
cd django-cognito-sample
```

Install libraries

```shell
pip install -r requirements.txt
```

Initialize database

```shell
python manage.py makemigrations
python manage.py migrate
```

Create superuser

```shell
python manage.py createsuperuser
```

Set environment variables

```
cp .env.sample .env
```

And customize it

> Unset or set empty for APP_SECRET_KEY, if you have no client secret.
> Set 0 or 1 in boolean variables (DEBUG etc).

You can see more detail [here](https://github.com/patriotresearch/django-cognito-redux/).

Run server

```shell
python manage.py runserver
```

Check the authentication by brower `http://localhost:8000/admin`
