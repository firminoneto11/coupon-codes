from fastapi.middleware.trustedhost import TrustedHostMiddleware

from config import settings

allowed_hosts_middleware_configuration = {
    "middleware_class": TrustedHostMiddleware,
    "allowed_hosts": settings.ALLOWED_HOSTS,
}
