import os
from typing import Any, Dict, List

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


def construct_message(route_table_id: str) -> str:
    return f"Routes for transit gateway ({route_table_id}) have changed."


def get_aws_account_id() -> str:
    sts_client = boto3.client("sts")
    caller_identity = sts_client.get_caller_identity()

    return caller_identity["Account"]


def are_routes_equal(route1: Dict[str, str], route2: Dict[str, str]) -> bool:
    return (
        route1["DestinationCidrBlock"] == route2["DestinationCidrBlock"]
        and route1["Type"] == route2["Type"]
        and route1["State"] == route2["State"]
    )


def contains_route(routes: List[Dict[str, str]], route: Dict[str, str]) -> bool:
    return len([r for r in routes if are_routes_equal(r, route)]) > 0


@logger.inject_lambda_context(log_event=True)
def handle_event(event: dict, context: LambdaContext) -> dict[Any, Any]:
    route_table_id = event["transit-gateway-route-table-id"]
    known_routes = event["known-routes"]

    logger.debug(f"Route table id: {route_table_id}")
    logger.debug(f"Expected routes: {known_routes}")

    ec2_client = boto3.client("ec2", region_name="eu-west-2")
    actual_routes = ec2_client.search_transit_gateway_routes(
        TransitGatewayRouteTableId=route_table_id,
        Filters=[{"Name": "type", "Values": ["propagated"]}],
    )["Routes"]

    logger.info(f"Found {len(actual_routes)} route(s) for route table {route_table_id}")

    unknown_routes = [
        route for route in actual_routes if not contains_route(known_routes, route)
    ]

    logger.info(
        f"Found {len(unknown_routes)} unknown route(s) for route table {route_table_id}"
    )

    missing_routes = [
        route for route in known_routes if not contains_route(actual_routes, route)
    ]

    logger.info(
        f"Found {len(missing_routes)} missing route(s) for route table {route_table_id}"
    )

    sns_client = boto3.client("sns", region_name="eu-west-2")

    if len(missing_routes) > 0 or len(unknown_routes) > 0:
        sns_client.publish(
            TopicArn=os.getenv("SNS_TOPIC_ARN"),
            Subject=f"{get_aws_account_id()} - Transit Gateway Route Table Monitor",
            Message=construct_message(route_table_id),
        )

    return event
