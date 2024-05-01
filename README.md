# Authenticating Django Admin with Auth0 

I wanted to connect with Auth0 using a more secure package than `authlib`. I came across this package: [mozilla-django-oidc’s](https://github.com/mozilla/mozilla-django-oidc) which seems much more stable and robust.

## Step 1: Install packages
`pip install -r requirements.txt`

## Step 2: Setup .env and settings file
Create a .env file with:

```
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_DOMAIN=
```

I abstracted the user model (as you should with any Django project) and pointed the setting to it.
Copy over the logic from `authO-oidc-django/backend.py` and amend it to your use case.

Add users to 'admin' role and set the flow in Auth0 actions:
Create a new role for your users who are admins and add them to it.
Make sure the namespace is the same as what you will use in `backend.py`
```
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'iam.org.project.oidc-auth0-django-backend.roles.userRoles';
  if (event.authorization) {
    api.idToken.setCustomClaim(`${namespace}:userRoles`, event.authorization.roles);
    api.accessToken.setCustomClaim(`${namespace}:userRoles`, event.authorization.roles);
  }
};
```

```
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["oidcAuth0Django.backend.PermissionBackend"]
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

Copy over the logic at the end of the setting.py file.

## Step 4
Override the login screen on the Django admin to ask users to login via Auth0 instead
