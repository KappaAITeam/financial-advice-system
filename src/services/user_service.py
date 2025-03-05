from src.api.models.user import User, UserCreate, UserLogin
from src.utils.hashing import hash_password, verify_password
from src.utils.jwt_handler import create_access_token

# This part is not yet fully done, this is a structure and should be updated.


async def register_user(user_data: UserCreate):
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        return False
    user = User(email=user_data.email, username=user_data.username,
                password_hash=hash_password(user_data.password))
    await user.insert()
    return True


async def login_user(user_data: UserLogin):
    user = await User.find_one(User.email == user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        return None
    token = create_access_token({"user_id": str(user.id), "email": user.email})
    return token
