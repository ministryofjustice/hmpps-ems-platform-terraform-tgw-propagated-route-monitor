from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

from typing import Any


@logger.inject_lambda_context
def handle_event(event: dict, context: LambdaContext) -> dict[Any, Any]:
    logger.info("Hello world")

    return event
