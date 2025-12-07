# This terraform setup should not cover retrieving data from the cluster, it should only setup a bucket which allows for storing data


module "s3_velero_backup" {
  source = "./modules/s3/velero"
}