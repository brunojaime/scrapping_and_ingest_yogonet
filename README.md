
# News Web Scraper – Cloud Run Job

This project runs an automated scraping process on a news website, processes the data using Pandas, and loads it into BigQuery. It's fully Dockerized and deployed as a **Cloud Run Job**.

---

## What does it do?

1. Uses Selenium to scrape news articles from a specific website.
2. Processes the data using Pandas (e.g., word count, character count, etc.).
3. Uploads the results into a BigQuery table.
4. Runs as a Cloud Run Job using a custom Docker image.

---

## Prerequisites

- Google Cloud CLI (`gcloud`) installed and authenticated
- Permissions to:
  - Create and push to Artifact Registry
  - Use Cloud Run and BigQuery
- The following APIs enabled:

#### bash:
gcloud services enable artifactregistry.googleapis.com run.googleapis.com bigquery.googleapis.com


## Installation and Setup

### 1. Clone the repository

#### bash:
git clone https://github.com/brunojaime/scrapping_and_ingest_yogonet
cd yogonet-scraper



### 3. Create the `.env` file
Create a `.env` file at the root of the project with the following content:
PROJECT_ID=<your-project-id>

This following variables can be customized:

DATASET_ID=news_data
TABLE_ID=yogonet_articles
REGION=us-central1
REPO_NAME=yogonet-repo
SERVICE_NAME=yogonet-scraper


Make sure that `PROJECT_ID` matches the currently active project. You can verify it with this command:

#### bash:
gcloud config get-value project

## Deployment
Run the following script to automatically build, push, and run everything:
./deploy.sh

### This script:

Validates your environment (gcloud, docker, variables)
Builds and uploads the Docker image
Creates or updates the Cloud Run Job
Executes the Job using the values from the .env file

## View Job Executions
To see the execution history of the Job:

(See the region selected, in this case is with us-central1)
gcloud beta run jobs executions list --region=us-central1 --job=yogonet-scraper
You can also view it in the Google Cloud Console web UI.

 ## View Data in BigQuery
Go to your project in BigQuery and look for the dataset and table defined in your .env file.
