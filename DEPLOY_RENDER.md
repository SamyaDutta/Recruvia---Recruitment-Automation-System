# Deploy Recruvia to Render

## 1. Push the project to GitHub

From the project folder:

```powershell
git add Dockerfile .dockerignore render.yaml DEPLOY_RENDER.md requirements.txt app2.py main3.py agents tasks utils
git commit -m "Add Docker and Render deployment"
git push origin main
```

Do not commit `.env`. It is excluded by `.gitignore` and `.dockerignore`.

## 2. Create the Render service

1. Open [Render](https://dashboard.render.com/) and sign in.
2. Select **New > Blueprint**.
3. Connect the GitHub repository containing this project.
4. Select the branch containing `render.yaml`.
5. Review the `recruvia` web service and deploy it.

Render will detect the Dockerfile and build the image. The service listens on Render's `$PORT` value automatically.

## 3. Add secrets

When Render prompts for the unsynchronized environment variables, enter:

```text
GROQ_API_KEY       your Groq API key
GMAIL_SENDER       the Gmail address that sends invitations
GMAIL_PASSWORD     the Gmail App Password, without spaces
```

These values are injected at runtime and are not stored in the repository.

## 4. Verify the deployment

After deployment, open the Render URL and check:

1. The dashboard loads.
2. **Load Candidate Database** succeeds.
3. A job role can be interpreted.
4. Profile search and CV screening work.
5. Only test interview scheduling after confirming the Gmail App Password is valid.

## Important persistence note

Render's default filesystem is ephemeral. ChromaDB data written during runtime can be lost when the service restarts. This app reloads the candidate database from `data/cs_engineers.xlsx`, so use **Load Candidate Database** after a restart. Add a Render persistent disk or external database later if runtime data must survive deployments.