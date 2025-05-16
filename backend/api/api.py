from django.http import Http404, JsonResponse
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

from .error_handlers import get_error_handler  # 你寫好的錯誤處理邏輯
from .routers.companies import companies
from .routers.jobs import jobs
from .routers.users import users

api = NinjaExtraAPI(
    title="Ethan's TalentLabs API",
    version="1.0",
    description="Ethan's TalentLabs Job Platform API",
    auth=JWTAuth(),
    csrf=False,
)

# 註冊 JWT 控制器
api.register_controllers(NinjaJWTDefaultController)

# 註冊其他路由
api.add_router("/users", users, tags=["Users"])
api.add_router("/companies", companies, tags=["Companies"])
api.add_router("/jobs", jobs, tags=["Jobs"])


@api.exception_handler(Http404)
def custom_404_handler(request, exc: Http404):
    status_code, error_response = get_error_handler(exc)
    return JsonResponse(error_response.dict(), status=status_code)


@api.exception_handler(Exception)
def custom_exception_handler(request, exc: Exception):
    status_code, error_response = get_error_handler(exc)
    return JsonResponse(error_response.dict(), status=status_code)


@api.get("/hello", tags=["Default"])
def hello(request):
    return {"message": "Hello, World!"}
