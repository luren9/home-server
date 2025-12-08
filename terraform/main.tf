module "s3_velero_backup" {
  source = "./modules/velero"
}


output "velero_bucket_name" {
  description = "The Velero S3 bucket name"
  value       = module.s3_velero_backup.velero_bucket_name
}

output "velero_access_key_id" {
  description = "Access key for Velero (like a username)"
  value       = module.s3_velero_backup.velero_access_key_id
  sensitive   = true
}

output "velero_secret_access_key" {
  description = "Secret key for Velero (like a password)"
  value       = module.s3_velero_backup.velero_secret_access_key
  sensitive   = true
}