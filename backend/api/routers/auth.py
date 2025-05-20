# api/routers/auth.py
from ninja import Router

auth = Router(tags=["Auth"])


@auth.get("/me")
def get_current_user(request):
    user = request.user
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
