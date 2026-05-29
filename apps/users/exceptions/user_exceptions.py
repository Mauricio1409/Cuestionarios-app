from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidUserDataError(APIException):
    """Se lanza cuando los datos enviados para crear/actualizar un usuario son inválidos."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Los datos del usuario son inválidos."
    default_code = "invalid_user_data"


class UserNotFoundError(APIException):
    """Se lanza cuando no se encuentra un usuario por email o ID."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "El usuario no fue encontrado."
    default_code = "user_not_found"


class RefreshTokenRequiredError(APIException):
    """Se lanza cuando no se envía el refresh token en el logout."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No se envió el refresh token."
    default_code = "refresh_token_required"


class InvalidTokenError(APIException):
    """Se lanza cuando el refresh token enviado es inválido o ya fue usado."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Token inválido o ya fue utilizado."
    default_code = "invalid_token"


class InvalidCredentialsError(APIException):
    """Credenciales de autenticación inválidas."""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Las credenciales proporcionadas son inválidas."
    default_code = "invalid_credentials"


class UserAlreadyExistsError(APIException):
    """El email ya está registrado en el sistema."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ya existe un usuario con este email."
    default_code = "user_already_exists"
