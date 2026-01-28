#!/bin/bash
# IAM Minimization - USE WITH CAUTION
# Rollback: re-run with original roles

PROJECT="project-83e7d21c-5b76-435e-98f"
SA="890343237671-compute@developer.gserviceaccount.com"

# Downgrade run.admin -> run.developer
gcloud projects remove-iam-policy-binding $PROJECT --member="serviceAccount:$SA" --role="roles/run.admin" --quiet
gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$SA" --role="roles/run.developer" --quiet

# Downgrade storage.admin -> storage.objectViewer (if write not needed)
# gcloud projects remove-iam-policy-binding $PROJECT --member="serviceAccount:$SA" --role="roles/storage.admin" --quiet
# gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$SA" --role="roles/storage.objectViewer" --quiet

echo "Done. Verify with: gcloud projects get-iam-policy $PROJECT"
