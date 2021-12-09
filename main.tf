terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.3.0"
    }
  }
}

#Asetetaan credentiaalit, projekti ja oletusalueet
provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

#Asetetaan credentiaalit, projekti ja oletusalueet, google-betaa käytetään apin luomisessa
provider "google-beta" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

#luodaan ämpäri jonne koodi laitetaan
resource "google_storage_bucket" "bucket" {
  provider = google
  name     = "juukeli-ampari"
  location = "EU"
}

#luodaan storage object
resource "google_storage_bucket_object" "movies" {
  provider  = google
  name      = "movies"
  bucket    = google_storage_bucket.bucket.name
  source    = "./movies.zip"
}

#TODO nimea funktio paremmin ja kirjoita parempi kuvaus
resource "google_cloudfunctions_function" "function" {
  provider    = google
  name        = "pick_movie"
  description = "Testataan funtkion tuuppaamista gcp:hen terraformilla"
  runtime     = "python39"

  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.movies.name
  trigger_http          = true
  entry_point           = "check_movie_length"
}

# IAM entry for all users to invoke the function
#tää pitää olla jotta on julkisesti saatavilla
resource "google_cloudfunctions_function_iam_member" "invoker" {
  provider       = google
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

#Luodaan API Gateway
resource "google_api_gateway_api" "elokuva_api" {
  provider = google-beta
  api_id = "elokuva-api"
}

resource "google_api_gateway_api_config" "elokuva_api" {
  provider = google-beta
  api = google_api_gateway_api.elokuva_api.api_id
  api_config_id = "config"

  openapi_documents {
    document {
      path = "spec.yaml"
      contents = filebase64("./api-config.yaml")
    }
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "elokuva_api" {
  provider = google-beta
  api_config = google_api_gateway_api_config.elokuva_api.id
  gateway_id = "elokuva-gateway"
}


#Luodaan placeholder workflow
resource "google_workflows_workflow" "example_workflow" {
  provider      = google-beta
  region        = "us-central1"
  name          = "workflow"
  description   = "This works by magic"
  source_contents = <<-EOF
   - getCurrentTime:
      call: http.get
      args:
          url: https://us-central1-workflowsample.cloudfunctions.net/datetime
      result: CurrentDateTime
  - readWikipedia:
      call: http.get
      args:
          url: https://en.wikipedia.org/w/api.php
          query:
              action: opensearch
              search: $${CurrentDateTime.body.dayOfTheWeek}
      result: WikiResult
  - returnOutput:
      return: $${WikiResult.body[1]}
EOF
}

#ladataan cloudruniin image (jossa nettisivu?)
resource "google_cloud_run_service" "default" {
  name     = "cloudrun-elokuva"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello" //nettisivun dockerimage tähän
      }
    }
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.default.location
  project     = google_cloud_run_service.default.project
  service     = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}