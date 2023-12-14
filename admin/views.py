from sqladmin import ModelView
from sqladmin import BaseView, expose

from crud import CRUDUsers
from crud.TelegramMessageCRUD import CRUDTelegramMessage
from crud.dialogCRUD import CRUDDialog
from models import User, Admin, Dialogue, AdminWebs


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.user_id, User.phone, User.is_block, User.updated_at]

    name = "Пользователи"
    name_plural = "Пользователя"
    icon = "fa-solid fa-user"

    column_labels = {
        User.id: "id",
        User.user_id: "id Телеграм",
        User.phone: "№ телефона",
        User.created_at: "Зарегистрировался в боте",
        User.updated_at: "Был в боте",
        User.is_block: "Заблокирован",
    }

    column_sortable_list = [
        User.id,
        User.is_block,
        User.updated_at
    ]

    column_searchable_list = [
        User.user_id
    ]

    can_export = False
    can_view_details = True
    list_template = "user_statistics.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"
    # column_details_list = [User.id, User.user_id, User.phone]


class AdminAdmin(ModelView, model=Admin):
    column_list = [Admin.id, Admin.admin_id]

    name = "Саппорт"
    name_plural = "Саппорты"
    icon = "fa-solid fa-headset"

    # list_template = "list.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"

    column_labels = {
        Admin.id: "id",
        Admin.admin_id: "id Телеграм"
    }
    can_export = False


class DialogAdmin(ModelView, model=Dialogue):
    column_list = [Dialogue.id, Dialogue.user_id, Dialogue.admin_id, Dialogue.is_active, Dialogue.who_closed,
                   Dialogue.gradeUser, Dialogue.gradeAdmin]
    name = 'диалог'
    name_plural = "Диалог"
    icon = "fa-regular fa-comment-dots"

    # list_template = "stat.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"

    column_labels = {
        Dialogue.id: "id",
        Dialogue.user_id: "id Продавца",
        Dialogue.admin_id: "id Саппорта",
        Dialogue.is_active: "Активный",
        Dialogue.created_at: "Создан",
        Dialogue.updated_at: "Обновлен",
        Dialogue.who_closed: "Кто закрыл",
        Dialogue.gradeUser: "Оценка Продавца",
        Dialogue.gradeAdmin: "Оценка Саппорта"
    }
    can_create = False
    # can_edit = False
    # can_delete = False
    can_export = False

    column_sortable_list = [
        Dialogue.id,
        Dialogue.is_active,
        Dialogue.updated_at
    ]

    column_searchable_list = [
        Dialogue.user_id,
        Dialogue.admin_id,
    ]


class AdminWeb(ModelView, model=AdminWebs):
    column_list = [AdminWebs.email, AdminWebs.password]

    name = "Администратор"
    name_plural = "Администраторы"
    icon = "fa-solid fa-lock"

    column_labels = {
        AdminWebs.email: "Логин",
        AdminWebs.password: "Пароль",
    }
    can_export = False


class TelegramMessageAdmin(BaseView):
    name = "Рассылка"
    name_plural = "Рассылка"
    icon = "fa-brands fa-telegram"
    can_export = False
    @expose("/mailing", methods=["GET"])
    async def mailing_page(self, request):
        mailing = await CRUDTelegramMessage.get_all()
        return await self.templates.TemplateResponse(request,
                                                     "mailing.html",
                                                     context={"users_count": mailing})


class Statistics(BaseView):
    name = "Статистика"
    icon = "fa-solid fa-chart-line"
    @expose("/statistics", methods=["GET"])
    async def statistics_page(self, request):
        gradeUser = 0
        gradeAdmin = 0

        allDialogs = await CRUDDialog.get_all_td()

        allDialogsLen = len(await CRUDDialog.get_all_td())
        openDialogs = len(await CRUDDialog.get_all_today(is_active=True))
        closeDialogs = len(await CRUDDialog.get_all_today(is_active=False))

        for getGrade in allDialogs:
            gradeUser += getGrade.gradeUser
            gradeAdmin += getGrade.gradeAdmin

        try:
            averageGradeUser = gradeUser / allDialogsLen
            averageGradeAdmin = gradeAdmin / allDialogsLen
        except ZeroDivisionError:
            averageGradeUser = 0
            averageGradeAdmin = 0

        getIsBlockUser = len(await CRUDUsers.get_all_is_block(is_block=True))
        getIsBlockUserFalse = len(await CRUDUsers.get_all_is_block(is_block=False))

        inside_count, outside_count = await CRUDUsers.get_count_today()

        return await self.templates.TemplateResponse(request,
                                                     "stat.html",
                                                     context={
                                                         "allDialogs": allDialogsLen,
                                                         "openDialogs": openDialogs,
                                                         "closeDialogs": closeDialogs,
                                                         "gradeUser": averageGradeUser,
                                                         "gradeAdmin": averageGradeAdmin,
                                                         "getIsBlockUser": getIsBlockUser,
                                                         "getIsBlockUserFalse": getIsBlockUserFalse,
                                                         "inside_count": inside_count,
                                                         "outside_count": outside_count,
                                                     })


