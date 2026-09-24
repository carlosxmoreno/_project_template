"""

{{PROJECT_NAME}} - api_errors.py - Clasificacion y mensajes para errores HTTP de la API LLM.
Version: 1.0.0
Component: utilities

Exposes:
    is_retryable(error) -> bool        -- True si el error es transitorio y vale la pena reintentar
    error_message(error) -> str        -- mensaje legible para log
    retry_wait_seconds(error) -> float -- segundos a esperar antes de reintentar

Compatible con ModelHTTPError de pydantic-ai (status_code, model_name, retry_after).

External dependencies: none
"""

_RETRYABLE_CODES = {429, 503, 502, 504}

_DEFAULT_WAIT = 10.0

_MESSAGES = {
    429: "quota or rate limit reached",
    503: "model temporarily unavailable (high demand)",
    502: "API gateway error",
    504: "API gateway timeout",
    401: "invalid credentials — check the API key",
    400: "invalid request — check model name and configuration parameters",
}


def is_retryable(error) -> bool:
    """Devuelve True si el error es transitorio y puede resolverse reintentando.

    Args:
        error: Excepcion con atributo status_code (ej. ModelHTTPError de pydantic-ai).

    Returns:
        True si el codigo de error esta en el conjunto de reintentables.
    """
    return getattr(error, "status_code", None) in _RETRYABLE_CODES


def error_message(error) -> str:
    """Devuelve un mensaje legible para log a partir del error.

    Args:
        error: Excepcion con atributos status_code y model_name.

    Returns:
        String formateado con codigo, modelo y descripcion.
    """
    status_code = getattr(error, "status_code", "?")
    model_name = getattr(error, "model_name", "unknown")
    description = _MESSAGES.get(status_code, f"unexpected error: {error}")
    return f"API error {status_code} ({model_name}): {description}"


def retry_wait_seconds(error, default: float = _DEFAULT_WAIT) -> float:
    """Devuelve los segundos a esperar antes de reintentar.

    Usa el header Retry-After de la respuesta si esta disponible (ModelHTTPError
    expone esto como retry_after). Si no, devuelve el valor por defecto.

    Args:
        error: Excepcion con atributo retry_after opcional (float | None).
        default: Segundos a usar si retry_after no esta disponible.

    Returns:
        Segundos a esperar como float.
    """
    retry_after = getattr(error, "retry_after", None)
    if retry_after is not None and retry_after > 0:
        return float(retry_after)
    return default
