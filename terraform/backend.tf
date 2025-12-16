terraform {
  backend "s3" {
    bucket       = "eks-shared-remote-backend"
    key          = "event-driven/sujal/terraform.tfstate"
    region       = "us-west-1"
    encrypt      = true
    use_lockfile = true
  }
}