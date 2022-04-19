from app.core.users import auth_backend, fastapi_users

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router()
reset_password_router = fastapi_users.get_reset_password_router()
verify_router = fastapi_users.get_verify_router()
