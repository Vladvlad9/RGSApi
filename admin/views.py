from sqladmin import ModelView
from sqladmin import BaseView, expose

from crud import CRUDUsers
from crud.TelegramMessageCRUD import CRUDTelegramMessage
from crud.dialogCRUD import CRUDDialog
from models import User, Admin, Dialogue, AdminWeb, Groups, SalesChannel


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.last_name, User.first_name, User.middle_name,
                   User.user_id, User.phone, User.is_block, User.updated_at]

    name = "Продавца"
    name_plural = "Продавцы"
    icon = "fa-solid fa-user"

    column_labels = {
        User.id: "id",
        User.user_id: "id Телеграм",
        User.phone: "№ телефона",
        User.created_at: "Зарегистрировался в боте",
        User.updated_at: "Был в боте",
        User.is_block: "Заблокирован",
        User.last_name: "Фамилия",
        User.first_name: "Имя",
        User.middle_name: "Отчество",
        User.lnr: "№ ЛНР",
        User.sales_channel_id: "Канал продаж",
        User.sales_channel: "Канал продаж",
    }

    column_sortable_list = [
        User.id,
        User.is_block,
        User.updated_at,
        User.last_name,
        User.first_name,
        User.middle_name,
        User.lnr,
        User.sales_channel,
    ]

    column_searchable_list = [
        User.user_id,
        User.user_id,
        User.phone,
        User.created_at,
        User.updated_at,
        User.is_block,
        User.last_name,
        User.first_name,
        User.middle_name,
        User.lnr,
        User.sales_channel,
    ]

    can_export = False
    can_view_details = True
    list_template = "user_statistics.html"

    column_details_exclude_list = [User.sales_channel_id]
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"
    # column_details_list = [User.id, User.user_id, User.phone]


class AdminAdmin(ModelView, model=Admin):
    column_list = [Admin.id, Admin.admin_id, Admin.last_name, Admin.first_name, Admin.middle_name, Admin.groups]

    name = "Андеррайтер"
    name_plural = "Андеррайтеры"
    icon = "fa-solid fa-headset"

    # list_template = "list.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"

    column_labels = {
        Admin.id: "id",
        Admin.admin_id: "id Телеграм",
        Admin.last_name: "Фамилия",
        Admin.first_name: "Имя",
        Admin.middle_name: "Отчество",
        Admin.groups: "Группа"
    }
    can_export = False

    column_details_exclude_list = [Admin.groups_id]


class DialogAdmin(ModelView, model=Dialogue):
    column_list = [Dialogue.id, Dialogue.created_at, Dialogue.user_id, Dialogue.admin_id, Dialogue.is_active,
                   Dialogue.who_closed,
                   Dialogue.gradeUser, Dialogue.gradeAdmin, Dialogue.chat_name]
    name = 'Диалог'
    name_plural = "Диалог"
    icon = "fa-regular fa-comment-dots"

    # list_template = "stat.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"

    column_labels = {
        Dialogue.id: "id",
        Dialogue.created_at: "Создан",
        Dialogue.user_id: "id Продавца",
        Dialogue.admin_id: "id Саппорта",
        Dialogue.is_active: "Активный",
        Dialogue.updated_at: "Обновлен",
        Dialogue.who_closed: "Кто закрыл",
        Dialogue.gradeUser: "Оценка Продавца",
        Dialogue.gradeAdmin: "Оценка Саппорта",
        Dialogue.chat_name: "Название чата",
    }
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False

    column_sortable_list = [
        Dialogue.id,
        Dialogue.is_active,
        Dialogue.updated_at,
        Dialogue.chat_name,
        Dialogue.user_id,
        Dialogue.admin_id,
        Dialogue.created_at,
        Dialogue.who_closed,
        Dialogue.gradeUser,
        Dialogue.gradeAdmin,
    ]

    column_searchable_list = [
        Dialogue.id,
        Dialogue.is_active,
        Dialogue.updated_at,
        Dialogue.chat_name,
        Dialogue.user_id,
        Dialogue.admin_id,
        Dialogue.created_at,
        Dialogue.who_closed,
        Dialogue.gradeUser,
        Dialogue.gradeAdmin,
    ]


class AdminWebs(ModelView, model=AdminWeb):
    column_list = [AdminWeb.email]

    name = "Администратор"
    name_plural = "Администраторы"
    icon = "fa-solid fa-lock"

    column_details_exclude_list = [AdminWeb.password]

    column_labels = {
        AdminWeb.email: "Логин",
    }
    can_export = False


class GroupAdmin(ModelView, model=Groups):
    column_list = [Groups.name, Groups.admin_groups]

    name = "Группа"
    name_plural = "Группы"
    icon = "fa-solid fa-users"

    column_labels = {
        Groups.name: "Название",
        Groups.admin_groups: "Андеррайтер"
    }
    can_export = False


class SalesChannelAdmin(ModelView, model=SalesChannel):
    column_list = [SalesChannel.name, SalesChannel.user_chanel]

    name = "Канал продаж"
    name_plural = "Канал продаж"
    icon = "fa-solid fa-cloud"

    column_labels = {
        SalesChannel.name: "Название",
        SalesChannel.user_chanel: "Продавец"
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


