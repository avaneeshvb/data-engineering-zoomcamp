variable "project" {
  description = "GCP Project ID"
  type        = string
}

variable "location" {
  description = "Location for resources (multi-region or region)"
  type        = string
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "Name of the GCS bucket to create"
  type        = string
}

variable "bq_dataset_name" {
  description = "Name of the BigQuery dataset to create"
  type        = string
}
