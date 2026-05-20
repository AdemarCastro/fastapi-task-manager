from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, TokenRefresh, UserLogin, UserRegister
from app.services.user_service import authenticate_user, create_user, get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        400: {"description": "Requisição inválida"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso proibido"},
    },
)

# ------------------------------------------------------------
# REGISTER
# ------------------------------------------------------------
@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description=(
        "Cria uma nova conta de usuário no sistema.\n\n"
        "O e-mail deve ser único. Caso já exista, a requisição será rejeitada."
    ),
)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=400,
            detail="Email já está registrado",
        )

    user = create_user(db, user_in.email, user_in.password)

    return {
        "message": "Usuário criado com sucesso",
        "user_id": user.id,
    }


# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------
@router.post(
    "/login",
    response_model=Token,
    summary="Autenticar usuário",
    description=(
        "Realiza autenticação do usuário e retorna tokens JWT.\n\n"
        "Retorna:\n"
        "- access_token: usado para autenticar requisições\n"
        "- refresh_token: usado para gerar novos access tokens"
    ),
)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.email, user_in.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuário inativo",
        )

    access_token = create_access_token(
        {"sub": str(user.id), "email": user.email}
    )
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


# ------------------------------------------------------------
# REFRESH TOKEN
# ------------------------------------------------------------
@router.post(
    "/refresh",
    response_model=Token,
    summary="Renovar tokens JWT",
    description=(
        "Gera novos tokens JWT a partir de um refresh token válido.\n\n"
        "Se o refresh token for inválido ou expirado, a requisição será rejeitada."
    ),
)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    payload = decode_token(
        token_data.refresh_token,
        expected_type="refresh",
    )

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido",
        )

    user = db.query(User).filter(User.id == int(payload["sub"])).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado ou inativo",
        )

    new_access = create_access_token(
        {"sub": str(user.id), "email": user.email}
    )
    new_refresh = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
    }