# Platform module STUB for Meridian J.D. RAG.
#
# Shows the resource boundary a real deployment fills in:
#   - aws_rds_cluster (Aurora PostgreSQL) with the pgvector extension, OR
#     aws_db_instance running a Postgres engine version that supports pgvector,
#   - a container service (ECS Fargate / App Runner) for api/Dockerfile.api,
#   - a static host (S3 + CloudFront) or container service for the UI,
#   - aws_secretsmanager_secret entries for the optional cloud provider keys,
#     mounted to the API task and resolved by providers/secrets.py.
#
# Resources are intentionally NOT declared so `terraform validate` stays clean
# without cloud credentials. The variables and outputs are the real contract.

variable "region" {
  type = string
}

variable "environment" {
  type = string
}

variable "image_tag" {
  type = string
}

locals {
  name_prefix = "mjd-rag-${var.environment}"
}

# Placeholder outputs so the root module wiring is exercised. A real module wires
# these to the actual service URL and database endpoint.
output "api_url" {
  description = "Public URL of the API service (filled by the real module)."
  value       = "https://${local.name_prefix}.example.invalid"
}

output "database_endpoint" {
  description = "Managed Postgres endpoint (filled by the real module)."
  value       = "${local.name_prefix}-pg.example.invalid:5432"
}
