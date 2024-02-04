from models.user import User

async def get_user_by_id(user_id: str):
    user_found = await User.get(user_id)
    if not user_found:
        return {"error": True, "message": "Not found user with id: {}".format(user_id), "email": None}
    return {"error": False, "message": "User found with id: {}".format(user_id), "email": user_found.email}
    