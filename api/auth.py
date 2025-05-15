from ninja import Router
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja.security import HttpBearer
from typing import Optional
from .schemas import Error

auth = Router()
auth.add_controller(NinjaJWTDefaultController)

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

@auth.get("/me", response={200: dict, 401: Error})
def get_user_info(request):
    if not request.auth:
        return 401, {"message": "Unauthorized"}
    return {
        "id": str(request.auth.id),
        "email": request.auth.email,
        "role": request.auth.role,
        "full_name": request.auth.full_name
    }