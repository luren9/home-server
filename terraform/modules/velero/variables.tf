variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "velero_bucket_name" {
  description = "S3 bucket name for Velero backups"
  type        = string
}

variable "backup_retention_days" {
  description = "Number of days to retain old backups"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {
    Project = "Velero-Backup"
  }
}