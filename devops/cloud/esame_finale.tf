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
