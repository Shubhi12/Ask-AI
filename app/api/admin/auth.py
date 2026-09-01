from fastapi import APIRouter
from models.users import Users
from app.schemas.requests import UserLoginRequest,UserRegisterRequest

router = APIRouter()

@router.post("/login",tags=["admin"])
def login(request:UserLoginRequest):
    try:
        user = Users.get_user_by_email(request.email)
        if not user:
            return {"error": "User not found",
                    "status": "error",
                    "http_code": 404}
        if user.password != request.password:
            return {"error": "Invalid password",
                    "status": "error",
                    "http_code": 401}
        return {"message": "User logged in successfully"}
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}

@router.post("/register",tags=["admin"])
def register(request:UserRegisterRequest):
    try:
        user_data = request.dict(exclude_unset=True)
        user = Users.get_user_by_email(user_data["email"])
        if user:
            return {"error": "User already exists",
                    "status": "error",
                    "http_code": 400}
        user = Users.create(user_data)
        return {"message": "User registered successfully",
                "data": user,
                "status": "success",
                "http_code": 201}
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}
    
    