from fastapi.responses import JSONResponse
from fastapi import APIRouter

router = APIRouter(prefix="/auth/guest")


@router.post("")
def set_guest_cookie():
    res = JSONResponse({"ok": True})
    res.set_cookie(
        key="guest",
        value="true",
        path="/",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )
    return res


@router.post("/clear")
def clear_guest_cookie():
    res = JSONResponse({"ok": True})
    res.set_cookie(
        key="guest",
        value="",
        path="/",
        max_age=0,      # clears the cookie
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return res
