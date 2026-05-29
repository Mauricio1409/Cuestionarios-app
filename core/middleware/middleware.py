import logging
import time

logger = logging.getLogger('api.requests')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Info básica de la request para el log inicial
        client_ip = self._get_client_ip(request)

        logger.info(f"REQUEST: {request.method} {request.path} - IP: {client_ip}")

        # Dejamos que Django procese la request
        response = self.get_response(request)

        # Calculamos cuánto tardó en procesarse
        duration_ms = round((time.time() - start_time) * 1000, 2)

        # Info del usuario (puede ser anónimo si no está autenticado)
        user = str(request.user) if hasattr(request, 'user') else 'Anonymous'

        # El nivel de log depende de si la request fue exitosa o no
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': duration_ms,
            'user': user,
        }

        if response.status_code >= 500:
            # Error del servidor, hay que investigar
            logger.error(f"RESPONSE: {log_data}")
        elif response.status_code >= 400:
            # Error del cliente, menos grave pero lo registramos
            logger.warning(f"RESPONSE: {log_data}")
        else:
            # Todo bien
            logger.info(
                f"RESPONSE: {request.method} {request.path} - "
                f"Status: {response.status_code} - Duration: {duration_ms}ms"
            )

        return response

    def _get_client_ip(self, request):
        """
        Obtiene la IP real del cliente.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Puede venir una lista de IPs separadas por coma, la primera es el cliente
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip
