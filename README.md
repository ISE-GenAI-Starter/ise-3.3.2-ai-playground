Run locally:

```
export FLASK_DEBUG=True (Once, optional)
flask run
```

Deploy:

```
gcloud config set project techexchange-sds-test-project
gcloud run deploy --source .
```

(pick us-central1)

