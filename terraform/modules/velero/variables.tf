# ------------------------------------------------------------------------------
# AWS Provider Variables
# ------------------------------------------------------------------------------
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}


# ------------------------------------------------------------------------------
# S3 Bucket Variables
# ------------------------------------------------------------------------------

variable "velero_bucket_name" {
  description = "S3 bucket name for Velero backups"
  type        = string
  default = "velero-cluster-backup-s3-bucket" # Needs to be globally unique

}

variable "velero_bucket_tags" {
  description = "Tags to apply to the Velero S3 bucket"
  type        = map(string)
  default     = {
    Name = "home-cluster-velero-backup-bucket"
    ManagedBy = "Terraform"
  }
}

variable "backup_retention_days" {
  description = "Number of days to retain old backups"
  type        = number
  default     = 30
}

# ------------------------------------------------------------------------------
# Minimal IAM Bucket User Variables
# ------------------------------------------------------------------------------
variable "velero_iam_user_tags" {
  description = "Tags to apply to the Velero IAM user"
  type        = map(string)
  default     = {
    Name = "home-cluster-velero-backup-user"
    ManagedBy = "Terraform"
  }
}