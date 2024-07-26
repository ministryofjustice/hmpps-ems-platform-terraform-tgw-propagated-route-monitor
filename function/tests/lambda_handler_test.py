import os

import boto3
from moto import mock_aws
from moto.core import DEFAULT_ACCOUNT_ID
from moto.ec2 import ec2_backends
from moto.sns import sns_backends

from src.lambda_handler import handle_event


@mock_aws
def test_all_routes_as_expected(lambda_context):
    ec2_client = boto3.client("ec2", region_name="eu-west-2")
    sns_client = boto3.client("sns", region_name="eu-west-2")

    # Setup transit gateway, route table
    tgw = ec2_client.create_transit_gateway(Description="Test transit gateway")
    tgw_id = tgw["TransitGateway"]["TransitGatewayId"]
    route_table = ec2_client.create_transit_gateway_route_table(
        TransitGatewayId=tgw_id,
    )
    route_table_id = route_table["TransitGatewayRouteTable"][
        "TransitGatewayRouteTableId"
    ]

    # Setup routes
    # Moto doesn't provide a way of creating propagated routes
    # So they are manually created by modifying moto internals
    ec2_backend = ec2_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]
    ec2_backend_route_table = ec2_backend.transit_gateways_route_tables[route_table_id]
    ec2_backend_route_table.routes["10.100.0.0/14"] = {
        "destinationCidrBlock": "10.100.0.0/14",
        "state": "active",
        "type": "propagated",
        "transitGatewayAttachments": {
            "resourceId": "123456789",
            "transitGatewayAttachmentId": "tgw-attach-123456789",
            "resourceType": "direct-connect-gateway",
        },
    }

    # Setup sns topic to publish notifications
    topic = sns_client.create_topic(
        Name="test-topic",
    )
    topic_arn = topic["TopicArn"]

    # Moto persists published messages in the backend
    # which can be used to check messages are published
    sns_backend = sns_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]

    # Ensure SNS_TOPIC_ARN is availble in lambda environment
    os.environ["SNS_TOPIC_ARN"] = topic_arn

    # Invoke the lambda
    handle_event(
        {
            "transit-gateway-route-table-id": route_table_id,
            "known-routes": [
                {
                    "DestinationCidrBlock": "10.100.0.0/14",
                    "State": "active",
                    "Type": "propagated",
                }
            ],
        },
        lambda_context,
    )

    # Verify no messages were published
    assert (
        len(sns_backend.topics[topic_arn].sent_notifications) == 0
    ), "An unexpected message was published to sns topic"


@mock_aws
def test_new_route_is_identified(lambda_context):
    ec2_client = boto3.client("ec2", region_name="eu-west-2")
    sns_client = boto3.client("sns", region_name="eu-west-2")

    # Setup transit gateway, route table
    tgw = ec2_client.create_transit_gateway(Description="Test transit gateway")
    tgw_id = tgw["TransitGateway"]["TransitGatewayId"]
    route_table = ec2_client.create_transit_gateway_route_table(
        TransitGatewayId=tgw_id,
    )
    route_table_id = route_table["TransitGatewayRouteTable"][
        "TransitGatewayRouteTableId"
    ]

    # Setup routes
    # Moto doesn't provide a way of creating propagated routes
    # So they are manually created by modifying moto internals
    ec2_backend = ec2_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]
    ec2_backend_route_table = ec2_backend.transit_gateways_route_tables[route_table_id]
    ec2_backend_route_table.routes["10.100.0.0/14"] = {
        "destinationCidrBlock": "10.100.0.0/14",
        "state": "active",
        "type": "propagated",
        "transitGatewayAttachments": {
            "resourceId": "123456789",
            "transitGatewayAttachmentId": "tgw-attach-123456789",
            "resourceType": "direct-connect-gateway",
        },
    }

    # Setup sns topic to publish notifications
    topic = sns_client.create_topic(
        Name="test-topic",
    )
    topic_arn = topic["TopicArn"]

    # Ensure SNS_TOPIC_ARN is availble in lambda environment
    os.environ["SNS_TOPIC_ARN"] = topic_arn

    # Moto persists published messages in the backend
    # which can be used to check messages are published
    sns_backend = sns_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]

    # Invoke the lambda
    handle_event(
        {
            "transit-gateway-route-table-id": route_table_id,
            "known-routes": [],
        },
        lambda_context,
    )

    # Verify a message was published
    assert (
        len(sns_backend.topics[topic_arn].sent_notifications) == 1
    ), "No messages published to sns topic"

    # Verify the correct message was published
    assert (
        sns_backend.topics[topic_arn].sent_notifications[0][1]
        == f"Routes for transit gateway ({route_table_id}) have changed."
    ), "Incorrect message published to sns topic"

    # Verify the correct subject was published
    assert (
        sns_backend.topics[topic_arn].sent_notifications[0][2]
        == f"{DEFAULT_ACCOUNT_ID} - Transit Gateway Route Table Monitor"
    ), "Incorrect subject published to sns topic"


@mock_aws
def test_deleted_route_is_identified(lambda_context):
    ec2_client = boto3.client("ec2", region_name="eu-west-2")
    sns_client = boto3.client("sns", region_name="eu-west-2")

    # Setup transit gateway, route table
    tgw = ec2_client.create_transit_gateway(Description="Test transit gateway")
    tgw_id = tgw["TransitGateway"]["TransitGatewayId"]
    route_table = ec2_client.create_transit_gateway_route_table(
        TransitGatewayId=tgw_id,
    )
    route_table_id = route_table["TransitGatewayRouteTable"][
        "TransitGatewayRouteTableId"
    ]

    # Setup routes
    # Moto doesn't provide a way of creating propagated routes
    # So they are manually created by modifying moto internals
    ec2_backend = ec2_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]
    ec2_backend_route_table = ec2_backend.transit_gateways_route_tables[route_table_id]
    ec2_backend_route_table.routes["10.100.0.0/14"] = {
        "destinationCidrBlock": "10.100.0.0/14",
        "state": "active",
        "type": "propagated",
        "transitGatewayAttachments": {
            "resourceId": "123456789",
            "transitGatewayAttachmentId": "tgw-attach-123456789",
            "resourceType": "direct-connect-gateway",
        },
    }

    # Setup sns topic to publish notifications
    topic = sns_client.create_topic(
        Name="test-topic",
    )
    topic_arn = topic["TopicArn"]

    # Moto persists published messages in the backend
    # which can be used to check messages are published
    sns_backend = sns_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]

    # Ensure SNS_TOPIC_ARN is availble in lambda environment
    os.environ["SNS_TOPIC_ARN"] = topic_arn

    # Invoke the lambda
    handle_event(
        {
            "transit-gateway-route-table-id": route_table_id,
            "known-routes": [
                {
                    "DestinationCidrBlock": "10.100.0.0/14",
                    "State": "active",
                    "Type": "propagated",
                },
                {
                    "DestinationCidrBlock": "10.104.0.0/14",
                    "State": "active",
                    "Type": "propagated",
                },
            ],
        },
        lambda_context,
    )

    # Verify a message was published
    assert (
        len(sns_backend.topics[topic_arn].sent_notifications) == 1
    ), "No messages published to sns topic"

    # Verify the correct message was published
    assert (
        sns_backend.topics[topic_arn].sent_notifications[0][1]
        == f"Routes for transit gateway ({route_table_id}) have changed."
    ), "Incorrect message published to sns topic"

    # Verify the correct subject was published
    assert (
        sns_backend.topics[topic_arn].sent_notifications[0][2]
        == f"{DEFAULT_ACCOUNT_ID} - Transit Gateway Route Table Monitor"
    ), "Incorrect subject published to sns topic"


@mock_aws
def test_changed_route_is_identified(lambda_context):
    ec2_client = boto3.client("ec2", region_name="eu-west-2")
    sns_client = boto3.client("sns", region_name="eu-west-2")

    # Setup transit gateway, route table, no routes
    tgw = ec2_client.create_transit_gateway(Description="Test transit gateway")
    tgw_id = tgw["TransitGateway"]["TransitGatewayId"]
    route_table = ec2_client.create_transit_gateway_route_table(
        TransitGatewayId=tgw_id,
    )
    route_table_id = route_table["TransitGatewayRouteTable"][
        "TransitGatewayRouteTableId"
    ]

    # Setup routes
    # Moto doesn't provide a way of creating propagated routes
    # So they are manually created by modifying moto internals
    ec2_backend = ec2_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]
    ec2_backend_route_table = ec2_backend.transit_gateways_route_tables[route_table_id]
    ec2_backend_route_table.routes["10.104.0.0/14"] = {
        "destinationCidrBlock": "10.104.0.0/14",
        "state": "active",
        "type": "propagated",
        "transitGatewayAttachments": {
            "resourceId": "123456789",
            "transitGatewayAttachmentId": "tgw-attach-123456789",
            "resourceType": "direct-connect-gateway",
        },
    }

    # Setup sns topic to publish notifications
    topic = sns_client.create_topic(
        Name="test-topic",
    )
    topic_arn = topic["TopicArn"]

    # Ensure SNS_TOPIC_ARN is availble in lambda environment
    os.environ["SNS_TOPIC_ARN"] = topic_arn

    # Moto persists published messages in the backend
    # which can be used to check messages are published
    sns_backend = sns_backends[DEFAULT_ACCOUNT_ID]["eu-west-2"]

    # Invoke the lambda
    handle_event(
        {
            "transit-gateway-route-table-id": route_table_id,
            "known-routes": [
                {
                    "DestinationCidrBlock": "10.100.0.0/14",
                    "State": "active",
                    "Type": "propagated",
                }
            ],
        },
        lambda_context,
    )

    # Verify a message was published
    assert (
        len(sns_backend.topics[topic_arn].sent_notifications) == 1
    ), "No messages published to sns topic"

    # Verify the correct message was published
    assert (
        sns_backend.topics[topic_arn].sent_notifications[0][1]
        == f"Routes for transit gateway ({route_table_id}) have changed."
    ), "Incorrect message published to sns topic"

    # Verify the correct subject was published
    assert (
        sns_backend.topics[topic_arn].sent_notifications[0][2]
        == f"{DEFAULT_ACCOUNT_ID} - Transit Gateway Route Table Monitor"
    ), "Incorrect subject published to sns topic"
