terraform {
  required_version = ">= 1.14.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- S3 Bucket ---
resource "aws_s3_bucket" "velero" {
  bucket = var.velero_bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "velero" {
  bucket = aws_s3_bucket.velero.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "velero" {
  bucket = aws_s3_bucket.velero.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "velero" {
  bucket                  = aws_s3_bucket.velero.id
  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}

# Optional: Bucket lifecycle rule (Velero compatible)
resource "aws_s3_bucket_lifecycle_configuration" "velero" {
  bucket = aws_s3_bucket.velero.id

  rule {
    id     = "cleanup-old-backups"
    status = "Enabled"

    expiration {
      days = var.backup_retention_days
    }
  }
}

# --- IAM User for Velero ---
resource "aws_iam_user" "velero" {
  name = "velero-backup-user"
  tags = var.tags
}

resource "aws_iam_access_key" "velero" {
  user = aws_iam_user.velero.name
}

# Policy granting minimal S3 access
data "aws_iam_policy_document" "velero_s3_policy" {
  statement {
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.velero.arn
    ]
  }

  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = [
      "${aws_s3_bucket.velero.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "velero_s3_policy" {
  name        = "velero-s3-access-policy"
  description = "Least privilege access for Velero backups to S3 bucket"
  policy      = data.aws_iam_policy_document.velero_s3_policy.json
}

resource "aws_iam_user_policy_attachment" "velero_attachment" {
  user       = aws_iam_user.velero.name
  policy_arn = aws_iam_policy.velero_s3_policy.arn
}