curl -X PATCH -H "Content-Type: application/json" \
  -d '{"fields": {"status": {"stringValue": "ACTIVE"}}}' \
  "https://firestore.googleapis.com/v1/projects/phonepe-keys/databases/(default)/documents/activation_keys/Ph-5423-FR?updateMask.fieldPaths=status&key=AIzaSyAXw6__Llt1JYyPz3qv2hNx3VJ33pjhk64"
