import fastapi

# import pydantic
from src.api.dependencies.repository import get_repository
from src.models.db.models import User
from src.models.schemas.account import (  # AccountInUpdate,; AccountWithToken,
    AccountInCreate,
    AccountInResponse,
    UserInResponse,
)
from src.repository.crud.user import UserCRUDRepository

# from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist

# from src.utilities.exceptions.http.exc_404 import (
#     http_404_exc_email_not_found_request,
#     http_404_exc_id_not_found_request,
#     http_404_exc_username_not_found_request,
# )


router = fastapi.APIRouter(prefix="/accounts", tags=["accounts"])


@router.get(
    path="",
    name="users:read-all-users",
    response_model=list[UserInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_all_users(
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> list[UserInResponse]:
    all_users = await user_repo.read_all_users()

    return all_users


@router.get(
    path="/{username}",
    name="users:read-user-by-username",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user_by_username(
    username: str,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        user = await user_repo.read_account_by_username(username=username)
    except EntityDoesNotExist:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Username {username} not found",
        )

    return user


@router.post(
    path="/createuser",
    name="users:create-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_user(
    user_create: AccountInCreate,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        new_user = await user_repo.create_user(user_create=user_create)

    except EntityAlreadyExists:
        fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Username {user_create.username} or {user_create.email} already taken",
        )
    return new_user


# @router.get(
#     path="/{id}",
#     name="accountss:read-account-by-id",
#     response_model=AccountInResponse,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def get_account(
#     id: int,
#     account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
# ) -> AccountInResponse:
#     try:
#         db_account = await account_repo.read_account_by_id(id=id)
#         access_token = jwt_generator.generate_access_token(account=db_account)

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=id)

#     return AccountInResponse(
#         id=db_account.id,
#         authorized_account=AccountWithToken(
#             token=access_token,
#             username=db_account.username,
#             email=db_account.email,  # type: ignore
#             is_verified=db_account.is_verified,
#             is_active=db_account.is_active,
#             is_logged_in=db_account.is_logged_in,
#             created_at=db_account.created_at,
#             updated_at=db_account.updated_at,
#         ),
#     )


# @router.patch(
#     path="/{id}",
#     name="accountss:update-account-by-id",
#     response_model=AccountInResponse,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def update_account(
#     query_id: int,
#     update_username: str | None = None,
#     update_email: pydantic.EmailStr | None = None,
#     update_password: str | None = None,
#     account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
# ) -> AccountInResponse:
#     account_update = AccountInUpdate(username=update_username, email=update_email, password=update_password)
#     try:
#         updated_db_account = await account_repo.update_account_by_id(id=query_id, account_update=account_update)

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=query_id)

#     access_token = jwt_generator.generate_access_token(account=updated_db_account)

#     return AccountInResponse(
#         id=updated_db_account.id,
#         authorized_account=AccountWithToken(
#             token=access_token,
#             username=updated_db_account.username,
#             email=updated_db_account.email,  # type: ignore
#             is_verified=updated_db_account.is_verified,
#             is_active=updated_db_account.is_active,
#             is_logged_in=updated_db_account.is_logged_in,
#             created_at=updated_db_account.created_at,
#             updated_at=updated_db_account.updated_at,
#         ),
#     )


# @router.delete(path="", name="accountss:delete-account-by-id", status_code=fastapi.status.HTTP_200_OK)
# async def delete_account(
#     id: int, account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository))
# ) -> dict[str, str]:
#     try:
#         deletion_result = await account_repo.delete_account_by_id(id=id)

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=id)

#     return {"notification": deletion_result}
