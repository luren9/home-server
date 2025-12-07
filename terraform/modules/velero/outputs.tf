output "velero_bucket_name" {
  description = "The Velero S3 bucket name"
  value       = aws_s3_bucket.velero.bucket
}

output "velero_access_key_id" {
  description = "Access key for Velero"
  value       = aws_iam_access_key.velero.id
  sensitive   = true
}

output "velero_secret_access_key" {
  description = "Secret key for Velero"
  value       = aws_iam_access_key.velero.secret
  sensitive   = true
}