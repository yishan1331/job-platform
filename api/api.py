from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from .users import users
from .companies import companies
from .jobs import jobs

api = NinjaAPI(
    title="Ethan's TalentLabs API",
    version="1.0",
    description="Ethan's TalentLabs Job Platform API",
    auth=JWTAuth(),
    csrf=False,
)

# 註冊路由
api.add_router("/users/", users, tags=["Users"])
api.add_router("/companies/", companies, tags=["Companies"])
api.add_router("/jobs/", jobs, tags=["Jobs"])

@api.get("/hello", tags=["Default"])
def hello(request):
    return {"message": "Hello, World!"}