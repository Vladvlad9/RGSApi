from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from datetime import datetime, timedelta

from crud.dialogCRUD import CRUDDialog

router = APIRouter(
    prefix='/admin_view',
    tags=['Admin View']
)


@router.get("/today")
async def statistic_today(request: Request):
    # today = datetime.now().strftime("%Y-%m-%d")
    gradeUser = 0
    gradeAdmin = 0

    allDialogs = await CRUDDialog.get_all_td()

    allDialogsLen = len(await CRUDDialog.get_all_td())
    openDialogs = len(await CRUDDialog.get_all_today(is_active=True))
    closeDialogs = len(await CRUDDialog.get_all_today(is_active=False))

    for getGrade in allDialogs:
        gradeUser += getGrade.gradeUser
        gradeAdmin += getGrade.gradeAdmin

    context = {
        "allDialogs": allDialogsLen,
        "openDialogs": openDialogs,
        "closeDialogs": closeDialogs,
        "gradeUser": gradeUser / allDialogsLen,
        "gradeAdmin": gradeAdmin / allDialogsLen
    }

    return JSONResponse(content=context)


@router.get("/week")
async def statistic_week(request: Request):
    # today = datetime.now()
    # start_of_week = today - timedelta(days=today.weekday())
    # end_of_week = start_of_week + timedelta(days=6)

    gradeUser = 0
    gradeAdmin = 0

    allDialogs = await CRUDDialog.get_all_wk()

    allDialogsLen = len(await CRUDDialog.get_all_wk())
    openDialogs = len(await CRUDDialog.get_all_week(is_active=True))
    closeDialogs = len(await CRUDDialog.get_all_week(is_active=False))

    for getGrade in allDialogs:
        gradeUser += getGrade.gradeUser
        gradeAdmin += getGrade.gradeAdmin

    context = {
        "allDialogs": allDialogsLen,
        "openDialogs": openDialogs,
        "closeDialogs": closeDialogs,
        "gradeUser": gradeUser / allDialogsLen,
        "gradeAdmin": gradeAdmin / allDialogsLen
    }

    return JSONResponse(content=context)


@router.get("/month")
async def statistic_month(request: Request):
    # today = datetime.now()
    # start_of_month = today.replace(day=1)
    # end_of_month = (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    gradeUser = 0
    gradeAdmin = 0

    allDialogs = await CRUDDialog.get_all_mn()

    allDialogsLen = len(await CRUDDialog.get_all_mn())
    openDialogs = len(await CRUDDialog.get_all_month(is_active=True))
    closeDialogs = len(await CRUDDialog.get_all_month(is_active=False))

    for getGrade in allDialogs:
        gradeUser += getGrade.gradeUser
        gradeAdmin += getGrade.gradeAdmin

    context = {
        "allDialogs": allDialogsLen,
        "openDialogs": openDialogs,
        "closeDialogs": closeDialogs,
        "gradeUser": gradeUser / allDialogsLen,
        "gradeAdmin": gradeAdmin / allDialogsLen
    }

    return JSONResponse(content=context)