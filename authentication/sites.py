from unfold.sites import UnfoldAdminSite

from .forms import LoginForm


class AuthenticationAdminSite(UnfoldAdminSite):
    login_form = LoginForm


authentication_admin_site = AuthenticationAdminSite()