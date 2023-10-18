from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from hashing import Hash
from jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter();

@router.post('/register')
async def create_user(request: User):
    user_found = await User.find_one({ "username":request.username })
    if user_found:
        raise HTTPException(
                status_code=409, detail="User already exists")
    request.password = Hash.bcrypt(request.password)
    user = await request.create()
    access_token = create_access_token(data={"username": user.username, "user_id": str(user.id) })
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends()):
	user = await User.find_one({"username":request.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
	if not Hash.verify(user.password, request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
	access_token = create_access_token(data={"username": user.username, "user_id": str(user.id) })
	return {"access_token": access_token, "token_type": "bearer"}