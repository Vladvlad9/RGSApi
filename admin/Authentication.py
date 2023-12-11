from typing import Optional

from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse


from crud.AdminWeb import CRUDAdminWeb
from routers.admin.auth import create_access_token
from routers.admin.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        get_admin = await CRUDAdminWeb.get_admin(email=str(email), password=str(password))
        if get_admin:
            access_token = create_access_token({'sub': str(get_admin.id)})
            request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        get_admin = await get_current_user(token=token)
        if not get_admin:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return True


authentication_backend = AdminAuth(secret_key="...")
