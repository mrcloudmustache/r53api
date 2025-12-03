// Add terraform provider version constraint
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    region         = "us-east-2"
    key            = "global/r53api/terraform.tfstate"
    dynamodb_table = "mcmgithubactions-state-locking"

  }
}

provider "aws" {
  region = var.aws_region

    assume_role {
    role_arn = "arn:aws:iam::${var.aws_account_id}:role/${var.aws_role_name}"
    }

  default_tags {
    tags = {
      Environment = var.env
    }
  }
}