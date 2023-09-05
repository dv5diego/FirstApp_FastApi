from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import uuid
from config.settings import Settings
from db.models.user import User, UserDB
from db.data.user import users_db


######################################################################################################

router=APIRouter()
oauth2=OAuth2PasswordBearer(tokenUrl="login")

crypt=CryptContext(schemes=["bcrypt"])
settings=Settings()

######################################################################################################

def searchUserDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def searchUser(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def authUser(token: str=Depends(oauth2)):
    exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales inválidas.", 
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        username=jwt.decode(token, settings.secret_key, settings.algorithm).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return searchUser(username)


async def currentUser(user: User=Depends(authUser)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo."
        )

    return user

######################################################################################################

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends()):
    user_db=users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto.")
    
    user=searchUserDB(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta.")
    
    access_token={
        "sub": user.username,
        "exp": datetime.utcnow()+timedelta(minutes=settings.token_duration),
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())
    }

    return {
        "access_token": jwt.encode(access_token, settings.secret_key, algorithm=settings.algorithm), 
        "token_type":"bearer"
    }


@router.get("/users/me")
async def me(user: User=Depends(currentUser)):
    return user