# hmpps-ems-platform-terraform-tgw-route-propagtion-monitor
Module to monitor for changes to routes propagated to transit gateways

## Usage

```hcl

module "tgw_route_propagation_monitor" {
  source = "https://github.com/ministryofjustice/hmpps-ems-platform-terraform-tgw-route-propagtion-monitor"

  tags             = local.tags
}
```
<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.1 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

No providers.

## Modules

No modules.

## Resources

No resources.

## Inputs

No inputs.

## Outputs

No outputs.
<!-- END_TF_DOCS -->