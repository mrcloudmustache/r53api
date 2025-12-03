variable "aws_region" {
  default = "us-east-1"
}

variable "aws_account_id" {
  type        = string
  description = "The AWS Account ID where resources will be created."
}

variable "aws_role_name" {
  type        = string
  description = "The name of the IAM role to assume for AWS operations."
}

variable "project" {
  default = "r53api"
}
variable "env" {
  default = "dev"
}

# new API hostname
variable "api_subdomain" {
  default = "r53api.cld1.mrcloudmustache.com"
}

variable "hosted_zone_id" {
  type        = string
  description = "If you want to target an existing hosted zone, set this to that zone id; otherwise Terraform will create a new zone for the subdomain."
  default     = ""
}


