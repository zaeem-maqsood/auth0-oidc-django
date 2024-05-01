# Authenticating Django Admin with Auth0 

I wanted to connect with Auth0 using a more secure package than `authlib`. I came across this package: [mozilla-django-oidc’s](https://github.com/mozilla/mozilla-django-oidc) which seems much more stable and robust.

## Step 1: Install packages
`pip install -r requirements.txt`

## Step 2: Setup .env and settings file
I abstracted the user model (as you should with any Django project) and pointed the setting to it

```
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["oidcAuth0Django.backends.PermissionBackend"]
```

Add the packages and the new user model to installed_apps.

Set Django Rest Framework authentication:
```
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
```
