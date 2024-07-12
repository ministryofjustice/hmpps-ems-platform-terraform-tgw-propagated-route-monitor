provider "aws" {
  region                      = "eu-west-2"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  http_proxy                  = "http://localhost:5000"
  https_proxy                 = "http://localhost:5000"
  endpoints {
    sts = "http://localhost:5000"
  }
}
