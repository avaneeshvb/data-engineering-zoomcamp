terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "google" {
  project = var.project
  region  = var.location
}

# Create a Google Cloud Storage bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

# Create a BigQuery dataset
resource "google_bigquery_dataset" "datawarehouse_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location

  # optionally allow Terraform destroy without manual cleanup
  delete_contents_on_destroy = true
}
