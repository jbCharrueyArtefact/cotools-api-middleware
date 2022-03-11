from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from app.logger.logger import logger


class CustomRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            body = await request.body()
            bodyJson = {}
            if len(body) > 0:
                bodyJson = await request.json()

            msg = {
                "body": bodyJson,
                "headers": dict(request.headers),
                "direction": "in",
                "method": request.method,
                "path": str(request.url),
            }

            logger.info(msg=msg)
            response: Response = await original_route_handler(request)

            msg["status"] = response.status_code
            msg["direction"] = "out"

            if response.status_code == 200:
                logger.info(msg=msg)
            else:
                logger.error(msg=msg)

            return response

        return custom_route_handler
