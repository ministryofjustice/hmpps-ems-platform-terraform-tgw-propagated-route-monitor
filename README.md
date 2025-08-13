# hmpps-ems-platform-terraform-tgw-propagated-route-monitor
Terraform module to monitor changes to propagated transit gateways routes.

## Usage

```hcl

module "tgw_route_propagation_monitor" {
  source = "https://github.com/ministryofjustice/hmpps-ems-platform-terraform-tgw-route-propagtion-monitor"
  version = "v0.1"

  sns_topic_arn = ""
  transit_gateway_route_tables = [
    {
      route_table_id = ""
      known_routes = [{
        DestinationCidrBlock = ""
        State                = "active"
        Type                 = "propagated"
      }]
    }
  ]

  tags             = local.tags
}
```
<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_function"></a> [function](#module\_function) | terraform-aws-modules/lambda/aws | 8.0.1 |

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_scheduler_schedule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [aws_iam_policy_document.assume_role_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_create"></a> [create](#input\_create) | Controls whether resources should be created. | `bool` | `true` | no |
| <a name="input_create_package"></a> [create\_package](#input\_create\_package) | Controls whether Lambda package should be created. Can be used with var.create=false to ensure the function package builds during CI. | `bool` | `true` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | Prefix to apply to all resource names. | `string` | `""` | no |
| <a name="input_schedule"></a> [schedule](#input\_schedule) | Defines how frequently the route tables are checked. | `string` | `"rate(60 minutes)"` | no |
| <a name="input_sns_topic_arn"></a> [sns\_topic\_arn](#input\_sns\_topic\_arn) | The ARN of the SNS topic that messages are published messages to. | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to assign to resources. | `map(string)` | `{}` | no |
| <a name="input_transit_gateway_route_tables"></a> [transit\_gateway\_route\_tables](#input\_transit\_gateway\_route\_tables) | Details of the transit gateway route tables to check. | <pre>list(object({<br/>    route_table_id = string,<br/>    known_routes = list(object({<br/>      DestinationCidrBlock = string,<br/>      State                = string<br/>      Type                 = string<br/>    }))<br/>  }))</pre> | `[]` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda"></a> [lambda](#output\_lambda) | Attributes associated with the lambda function. |
<!-- END_TF_DOCS -->