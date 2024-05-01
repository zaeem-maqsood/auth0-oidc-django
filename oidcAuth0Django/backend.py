from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class PermissionBackend(OIDCAuthenticationBackend):

    def get_username(self, claims):
        return claims.get("sub")

    def create_user(self, claims):
        print("Coming to the create user method")
        email = claims.get("email")
        username = self.get_username(claims)
        # Use a custom namespace for the user roles claim. Can be anything.
        custom_user_role_claim = (
            "iam.org.project.oidc-auth0-django-backend.roles.userRoles"
        )

        if "admin" in claims[custom_user_role_claim]:
            user = self.UserModel.objects.create_user(
                username, email=email, is_superuser=True, is_staff=True
            )
            return user
        else:
            user = self.UserModel.objects.create_user(username, email=email)
            return user

    def update_user(self, user, claims):
        # Use a custom namespace for the user roles claim. Can be anything.
        custom_user_role_claim = (
            "iam.org.project.oidc-auth0-django-backend.roles.userRoles"
        )

        if "admin" in claims[custom_user_role_claim]:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        user.save()
        return user
