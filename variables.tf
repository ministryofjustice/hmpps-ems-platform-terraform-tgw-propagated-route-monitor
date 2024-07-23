variable "create" {
  default     = true
  description = "Controls whether resources should be created."
  type        = bool
}

variable "create_package" {
  description = "Controls whether Lambda package should be created. Can be used with var.create=false to ensure the function package builds during CI."
  type        = bool
  default     = true
}

variable "name_prefix" {
  default     = ""
  description = "Prefix to apply to all resource names."
  type        = string
}

variable "schedule" {
  default     = "rate(60 minutes)"
  description = "Defines how frequently the route tables are checked."
  type        = string
}

variable "sns_topic_arn" {
  description = "The ARN of the SNS topic that messages are published messages to."
  type        = string

  validation {
    error_message = "The value must be the arn of an SNS topic."
    condition     = can(regex("^arn:aws:sns:eu-west-2:\\d{12}:[\\w\\-]{1,256}$", var.sns_topic_arn))
  }
}

variable "tags" {
  description = "A map of tags to assign to resources."
  type        = map(string)
  default     = {}
}

variable "transit_gateway_route_tables" {
  default     = []
  description = "Details of the transit gateway route tables to check."
  type = list(object({
    route_table_id = string,
    known_routes = list(object({
      DestinationCidrBlock = string,
      State                = string
      Type                 = string
    }))
  }))
}
