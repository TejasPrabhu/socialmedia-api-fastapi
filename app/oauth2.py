from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b99e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwt_token


def verify_jwt_token(token: str, exception):
    try:
        decoded_data = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_data is None:
            raise exception
        return schemas.TokenData(decoded_data.get('user_id'))
    except JWTError:
        raise exception


def get_current_user(token: str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_jwt_token(token=token, exception=credentials_exception)