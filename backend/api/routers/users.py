from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from django.shortcuts import get_object_or_404
from uuid import UUID


from ..models.user import User
from ..schemas.users import UserCreate, UserUpdate, UserOut
from ..error_handlers import get_error_handler, ErrorResponse

users = Router(tags=["Users"])

@users.post("", response={201: UserOut, 422: ErrorResponse, 409: ErrorResponse, 500: ErrorResponse}, summary="Create a User")
def create_user(request, payload: UserCreate):
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        role=payload.role,
        full_name=payload.full_name
    )
    return 201, user

@users.get("", response={200: List[UserOut], 422: ErrorResponse, 500: ErrorResponse}, summary="Get User List")
@paginate(PageNumberPagination)
def list_users(request):
    return User.objects.filter(is_active=True)

@users.get("/{user_id}", response={200: UserOut, 404: ErrorResponse, 500: ErrorResponse}, summary="Get a User")
def get_user(request, user_id: UUID):
    return get_object_or_404(User, id=user_id, is_active=True)

@users.put("/{user_id}", response={200: UserOut, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse}, summary="Update a User")
def update_user(request, user_id: UUID, payload: UserUpdate):
    user = get_object_or_404(User, id=user_id, is_active=True)
    for key, value in payload.dict(exclude_unset=True).items():
        if key == "password" and value:
            user.set_password(value)
        else:
            setattr(user, key, value)
    user.save()
    return user

@users.delete("/{user_id}", response={204: None, 404: ErrorResponse, 500: ErrorResponse}, summary="Delete a User")
def delete_user(request, user_id: UUID):
    user = get_object_or_404(User, id=user_id, is_active=True)
    user.is_active = False
    user.save()
    return 204, None