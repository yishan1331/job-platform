from ninja import Router
from ninja.pagination import paginate
from typing import List
from django.shortcuts import get_object_or_404
from .models import User
from .schemas import UserCreate, UserUpdate, UserOut, Error
from uuid import UUID

users = Router(tags=["Users"])

@users.post("", response={201: UserOut, 400: Error}, summary="Create a User")
def create_user(request, payload: UserCreate):
    try:
        user = User.objects.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            role=payload.role,
            full_name=payload.full_name
        )
        return 201, user
    except Exception as e:
        return 400, {"message": str(e)}

@users.get("", response=List[UserOut], summary="Get User List")
@paginate
def list_users(request):
    return User.objects.filter(is_active=True)

@users.get("/{user_id}", response={200: UserOut, 404: Error}, summary="Get a User")
def get_user(request, user_id: UUID):
    user = get_object_or_404(User, id=user_id, is_active=True)
    return user

@users.put("/{user_id}", response={200: UserOut, 400: Error, 404: Error}, summary="Update a User")
def update_user(request, user_id: UUID, payload: UserUpdate):
    try:
        user = get_object_or_404(User, id=user_id, is_active=True)
        for key, value in payload.dict(exclude_unset=True).items():
            if key == "password" and value:
                user.set_password(value)
            else:
                setattr(user, key, value)
        user.save()
        return user
    except Exception as e:
        return 400, {"message": str(e)}

@users.delete("/{user_id}", response={204: None, 404: Error}, summary="Delete a User")
def delete_user(request, user_id: UUID):
    user = get_object_or_404(User, id=user_id, is_active=True)
    user.is_active = False
    user.save()
    return 204, None