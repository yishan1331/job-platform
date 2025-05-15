from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from .auth import auth
from .jobs import jobs

api = NinjaAPI()
api.add_controller(NinjaJWTDefaultController)

api.add_router("/auth/", auth)
api.add_router("/jobs/", jobs)

@api.get("/hello")
def hello(request):
    return {"message": "Hello, World!"}