import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, SQLModel, Session, create_engine, select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

load_dotenv()
PEPPER = os.getenv("SECRET_PEPPER", "ClaveSecretaGlobal123!")
ph = PasswordHasher()

def get_password_with_pepper(password: str) -> str:
    return f"{password}{PEPPER}"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI(title="API de Autenticación Segura")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/register")
def register(user: User, session: Session = Depends(get_session)): 
    statement = select(User).where(User.username == user.username)
    if session.exec(statement).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    ready_password = get_password_with_pepper(user.hashed_password)
    user.hashed_password = ph.hash(ready_password)
    
    session.add(user)
    session.commit()
    return {"status": "success", "message": f"Usuario {user.username} registrado."}

@app.post("/login")
def login(user_data: User, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == user_data.username)
    db_user = session.exec(statement).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

    try:
        ready_password = get_password_with_pepper(user_data.hashed_password)
        ph.verify(db_user.hashed_password, ready_password)
    except VerifyMismatchError:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
    
    return {"status": "success", "message": "Bienvenido al sistema."}