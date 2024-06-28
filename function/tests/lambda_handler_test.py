from src.lambda_handler import handle_event


def test_hello_world(lambda_context):
    event = {"foo": "bar"}
    result = handle_event(event, lambda_context)

    assert result == event
