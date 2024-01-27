import os
from sqladmin import ModelView, action
from sqladmin import BaseView, expose
from fastapi import HTTPException
from crud import CRUDUsers
from crud.AdminCRUD import CRUDAdmin
from crud.TelegramMessageCRUD import CRUDTelegramMessage
from crud.dialogCRUD import CRUDDialog
from models import User, Admin, Dialogue, AdminWeb, Groups, SalesChannel
from starlette.responses import Response, FileResponse
from sqladmin.helpers import secure_filename
import pandas as pd


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.last_name, User.first_name, User.middle_name,
                   User.user_id, User.phone, User.is_block, User.updated_at, User.lnr]

    name = "Продавцы"
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
        User.quotation_number: "Номер котировки клиента",
        User.lnr: "№ ЛНР",
    }

    column_sortable_list = [
        User.id,
        User.is_block,
        User.updated_at,
        User.last_name,
        User.first_name,
        User.middle_name,
        User.lnr,
    ]

    column_searchable_list = [
        User.user_id,
        User.phone,
        User.created_at,
        User.updated_at,
        User.is_block,
        User.last_name,
        User.first_name,
        User.middle_name,
        User.lnr,
    ]

    column_details_exclude_list = [User.dialogue]
    form_excluded_columns = [User.dialogue]

    can_export = False
    can_view_details = True
    list_template = "user_statistics.html"

    # form_include_pk = True
    # column_details_exclude_list = [User.dialogue]
    # form_excluded_columns = [User.dialogue]
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"
    # column_details_list = [User.id, User.user_id, User.phone]


class AdminAdmin(ModelView, model=Admin):
    column_list = [Admin.id, Admin.admin_id, Admin.last_name, Admin.first_name, Admin.middle_name, Admin.groups]

    name = "Сотрудники РГС"
    name_plural = "Сотрудники РГС"
    icon = "fa-solid fa-headset"

    # list_template = "list.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"
    form_include_pk = True
    column_labels = {
        Admin.id: "id",
        Admin.admin_id: "id Телеграм",
        Admin.last_name: "Фамилия",
        Admin.first_name: "Имя",
        Admin.middle_name: "Отчество",
        Admin.groups: "Группа"
    }
    can_export = False

    column_details_exclude_list = [Admin.groups_id, Admin.groups, Admin.id]
    form_excluded_columns = [Admin.dialogue, Admin.groups_id, Admin.id]


class DialogAdmin(ModelView, model=Dialogue):
    column_list = [Dialogue.id, Dialogue.created_at, Dialogue.user, Dialogue.admin, Dialogue.is_active,
                   Dialogue.who_closed,
                   Dialogue.gradeUser, Dialogue.gradeAdmin, Dialogue.chat_name]
    name = 'Диалог'
    name_plural = "Диалог"
    icon = "fa-regular fa-comment-dots"

    # list_template = "stat.html"
    # details_template = "details.html"
    # edit_template = "edit.html"
    # create_template = "create.html"
    form_include_pk = True

    column_labels = {
        Dialogue.id: "id",
        Dialogue.created_at: "Создан",

        Dialogue.is_active: "Активный",
        Dialogue.updated_at: "Закрытие диалога",
        Dialogue.who_closed: "Кто закрыл",
        Dialogue.gradeUser: "Оценка Продавца",
        Dialogue.gradeAdmin: "Оценка Саппорта",
        Dialogue.chat_name: "Название чата",
        Dialogue.dialogue_time: "Продолжительность диалога (сек)",
        Dialogue.reaction_time: "Время реакции (сек)",
    }
    # can_create = False
    # can_edit = False
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

    # column_details_exclude_list = [Dialogue.sales_channel_id, Dialogue.sales_channel]
    # column_export_exclude_list = column_details_exclude_list

    @action(
        name="export-users",
        label="Выгрузить диалоги",
        include_in_schema=False,
        add_in_detail=False,
        add_in_list=True,

    )
    async def export_department_users(self, request) -> Response:
        data = []
        dialogs = await CRUDDialog.get_all()

        for dialog in dialogs:
            get_user = await CRUDUsers.get_user_id(user_id=dialog.user_id)
            get_admin = await CRUDAdmin.get_admin_id(admin_id=dialog.admin_id)
            data.append({
                'id': dialog.id,
                'Пользователь': f"{get_user.last_name} {get_user.first_name} {get_user.middle_name}",
                'Админ': f"{get_admin.last_name} {get_admin.first_name} {get_admin.middle_name}",
                "Создан": dialog.created_at,
                "Активный": dialog.is_active,
                "Закрытие диалога": dialog.updated_at,
                "Кто закрыл": dialog.who_closed,
                "Оценка Продавца": dialog.gradeUser,
                "Оценка Саппорта": dialog.gradeAdmin,
                "Название чата": dialog.chat_name,
                "Продолжительность диалога (сек)": dialog.dialogue_time,
                "Время реакции (сек)": dialog.reaction_time,
            })
        df = pd.DataFrame(data)

        filename = secure_filename(self.get_export_name(export_type="csv"))

        df.to_excel('Statistics.xlsx')

        file_path = "Statistics.xlsx"
        if os.path.exists(file_path):
            return FileResponse(file_path,
                                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                filename=filename)
        else:
            raise HTTPException(status_code=404, detail="File not found")


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
    # form_excluded_columns = [Groups.user_groups, Groups.admin_groups]


class SalesChannelAdmin(ModelView, model=SalesChannel):
    column_list = [SalesChannel.name]

    name = "Канал продаж"
    name_plural = "Канал продаж"
    icon = "fa-solid fa-cloud"

    column_labels = {
        SalesChannel.name: "Название",
    }
    can_export = False
    # form_excluded_columns = [SalesChannel.dialogue]


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


