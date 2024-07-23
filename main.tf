module "function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "v7.7.0"

  create_function = var.create
  create_package  = var.create_package
  create_role     = var.create

  function_name = "${var.name_prefix}-tgw-propagated-route-monitor"
  description   = "Monitor changes to propagated transit gateways routes"
  handler       = "lambda_handler.handle_event"
  runtime       = "python3.11"

  source_path = [
    "${path.module}/function/src",
    "${path.module}/function/pyproject.toml"
  ]

  environment_variables = {
    SNS_TOPIC_ARN = var.sns_topic_arn
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-tgw-propagated-route-monitor"
    }
  )
}

resource "aws_scheduler_schedule" "this" {
  for_each = var.create ? { for item in var.transit_gateway_route_tables : item["route_table_id"] => item } : {}

  name = "${var.name_prefix}-tgw-propagated-route-monitor"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = var.schedule

  target {
    arn      = module.function.lambda_function_arn
    role_arn = aws_iam_role.this[0].arn

    input = jsonencode({
      "transit-gateway-route-table-id" : each.value.route_table_id,
      "known-routes" : each.value.known_routes
    })
  }
}

resource "aws_iam_role" "this" {
  count = var.create ? 1 : 0

  name               = "${var.name_prefix}-tgw-propagated-route-monitor-scheduler"
  description        = "IAM role that EventBridge Scheduler assumes to interact with other AWS services"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy[0].json

  tags = var.tags
}

data "aws_iam_policy_document" "assume_role_policy" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  } # TODO: Confused deputy prevention. https://docs.aws.amazon.com/scheduler/latest/UserGuide/cross-service-confused-deputy-prevention.html
}

data "aws_iam_policy_document" "scheduler" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = [
      module.function.lambda_function_arn
    ]
  }
}

resource "aws_iam_policy" "this" {
  count = var.create ? 1 : 0

  name        = "${var.name_prefix}-tgw-propagated-route-monitor-scheduler"
  path        = "/"
  description = "IAM policy that EventBridge Scheduler uses to invoke the lambda function"
  policy      = data.aws_iam_policy_document.scheduler[0].json

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "this" {
  count = var.create ? 1 : 0

  role       = aws_iam_role.this[0].name
  policy_arn = aws_iam_policy.this[0].arn
}
