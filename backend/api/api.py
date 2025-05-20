from django.http import Http404, JsonResponse
from ninja.errors import HttpError as NinjaHttpError, ValidationError as NinjaValidationError
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

from .error_handlers import get_error_handler
from .routers.auth import auth
from .routers.companies import companies
from .routers.jobs import jobs
from .routers.users import users

api = NinjaExtraAPI(
    title="Ethan's TalentLabs API",
    version="1.0",
    description="Ethan's TalentLabs Job Platform API",
    auth=JWTAuth(),
    csrf=False,
    urls_namespace="api",
)

# 註冊 JWT 控制器
api.register_controllers(NinjaJWTDefaultController)

# 註冊其他路由
api.add_router("/auth", auth, tags=["Auth"])
api.add_router("/users", users, tags=["Users"])
api.add_router("/companies", companies, tags=["Companies"])
api.add_router("/jobs", jobs, tags=["Jobs"])


@api.exception_handler(NinjaHttpError)
def handle_ninja_http_error(request, exc: NinjaHttpError):
    error_message = str(exc)
    if "Expecting value" in error_message or "JSONDecodeError" in str(type(exc)):
        return JsonResponse(
            {
                "message": "Invalid JSON format",
                "code": "BAD_REQUEST",
                "details": {
                    "error": "The request body contains invalid JSON",
                    "message": error_message,
                },
            },
            status=400,
        )

    return JsonResponse({"message": str(exc), "code": "BAD_REQUEST", "details": None}, status=400)


@api.exception_handler(Http404)
def custom_404_handler(request, exc: Http404):
    status_code, error_response = get_error_handler(exc)
    return JsonResponse(error_response.dict(), status=status_code)


@api.exception_handler(NinjaValidationError)
def handle_validation_error(request, exc: NinjaValidationError):
    error_details = []
    for err in exc.errors:
        field = ".".join(str(x) for x in err["loc"][1:])
        error_details.append({"field": field, "message": err["msg"], "type": err["type"]})
    return JsonResponse(
        {
            "message": "Validation error",
            "code": "VALIDATION_ERROR",
            "details": {"errors": error_details},
        },
        status=422,
    )


@api.exception_handler(Exception)
def custom_exception_handler(request, exc: Exception):
    status_code, error_response = get_error_handler(exc)
    return JsonResponse(error_response.dict(), status=status_code)


@api.get("/hello", tags=["Default"])
def hello(request):
    return {"message": "Hello, World!"}
