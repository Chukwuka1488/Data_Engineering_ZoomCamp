terraform {
  required_version = ">= 1.0"
  backend "local" {}
  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  credentials = file("/Users/haykay14/Desktop/dtc-de-course-338518-d44b189574e3.json")

  project = var.project
  region  = var.region
  #  zone = "us-east-1"
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}"
  location = var.region

  #Optional but recommended settings:
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

# There will be more such tables for transformed data
#resource "google_bigquery_table" "table" {
#  dataset_id = google_bigquery_dataset.dataset.dataset_id
#  project    = var.project
#  table_id   = var.TABLE_NAME
#}