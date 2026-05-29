from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers.logout_serializer import LogOutSerializer
from apps.users.exceptions.user_exceptions import RefreshTokenRequiredError, InvalidTokenError
import logging
logger = logging.getLogger(__name__)


class LogOutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication,]

    def post(self, request):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")
        if not refresh_token:
            raise RefreshTokenRequiredError("No se envió el refresh token.")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise InvalidTokenError("Token inválido o ya fue utilizado.")

        logger.info(f"User {request.user.email} logged out successfully")

        return Response(status=status.HTTP_205_RESET_CONTENT)
