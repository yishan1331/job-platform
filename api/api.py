from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth
from .auth import auth
from .jobs import jobs

api = NinjaAPI(auth=JWTAuth())

api.add_router("/auth/", auth)
api.add_router("/jobs/", jobs)

@api.get("/hello")
def hello(request):
    return {"message": "Hello, World!"}