# Meridian J.D. RAG: minimal Terraform stub (devops-packaging contract item 4).
#
# This is a STUB that shows WHERE the stack lands in cloud, not a production
# deployment. It declares the provider and a single module boundary so a reviewer
# sees the intended cloud shape: a managed Postgres with pgvector, a container
# service for the API, and a static/site host for the UI. Fill the module in for a
# real environment; the variables and outputs below are the contract a real module
# must satisfy.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  # Credentials come from the environment / instance profile, never hardcoded.
}

variable "region" {
  description = "Cloud region for the Meridian J.D. RAG stack."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name (dev | staging | prod)."
  type        = string
  default     = "dev"
}

variable "image_tag" {
  description = "Container image tag for the API service."
  type        = string
  default     = "latest"
}

# The platform module is where the real resources live (managed Postgres with the
# pgvector extension, the API container service, the UI host, secrets, and the
# network). It is intentionally a stub here.
module "platform" {
  source      = "./modules/platform"
  region      = var.region
  environment = var.environment
  image_tag   = var.image_tag
}

output "api_url" {
  description = "Public URL of the API service once deployed."
  value       = module.platform.api_url
}

output "database_endpoint" {
  description = "Managed Postgres (pgvector) endpoint."
  value       = module.platform.database_endpoint
  sensitive   = true
}
