# Gemini Secrets Game
For ISE 3.3.2 - AI Playground in-class activity

## Note


### Make sure there is a SINGLE copy deployed and running somewhere before class, that you can link the students to. This can be used across multiple classes, but may be unnecessary to copy into every GitHub org.


Setup:

```bash
git clone git@github.com:ISE-GenAI-Starter/ise-3.3.2-ai-playground.git # Clone this repo

cd ise-3.3.2-ai-playground.git # cd into dir

python -m venv venv # Install venv

source venv/bin/activate # Activate venv

pip install -r requirements.txt # Install libraries
```


Run locally:

```bash
source venv/bin/activate # Once
export FLASK_DEBUG=True # Once, optional

flask run
```

Deploy:

```bash
gcloud run deploy --source .
```

(pick us-central1)

