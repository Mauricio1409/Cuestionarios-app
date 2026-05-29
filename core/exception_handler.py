from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Si la respuesta es None, significa que no se manejó la excepción
    if response is None:
        return None

    # Personalizamos la estructura de la respuesta de error
    custom_response_data = {
        "status" : "error",
        "status_code": response.status_code,
        "details" : response.data
    }

    return Response(custom_response_data, status=response.status_code)