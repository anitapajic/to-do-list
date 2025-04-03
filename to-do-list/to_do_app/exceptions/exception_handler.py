from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    view = context.get("view", None)
    logger.warning(f"Exception in view {view.__class__.__name__}: {exc}")

    if isinstance(response.data, dict):
        response.data = {"error": response.data}
    else:
        response.data = {"error": str(response.data.get("detail", str(exc)))}

    return response
