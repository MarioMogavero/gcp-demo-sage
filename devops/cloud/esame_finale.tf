# ==============================================
# Bucket di Sage come risorsa Terraform
# ==============================================

resource "google_storage_bucket" "bucket_instructions" {
  name          = "${var.resource_prefix}-instructions"
  project       = var.project_id
  location      = "EUROPE-WEST6"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  force_destroy = true
}

resource "google_storage_bucket_iam_member" "bucket_instructions_viewer" {
  bucket = google_storage_bucket.bucket_instructions.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.sage_run.email}"
}