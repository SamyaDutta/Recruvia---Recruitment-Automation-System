# Recruvia

Recruvia is an AI-assisted recruitment workflow for searching candidate profiles, screening applicants, scheduling interviews, and generating recruitment reports.

## Live Application

Open the deployed app:

**https://recruvia20-ly8xstqgb8uex4gb9hyhnm.streamlit.app/**

## Features

- Load candidate profiles from the local Excel database.
- Interpret natural-language job-role requests.
- Search candidate profiles stored in ChromaDB.
- Screen and rank candidates against a job description.
- Send interview invitations through Gmail SMTP.
- Generate recruitment reports and export them as PDF.
- Ask follow-up questions through the HR Assistant chat.

## Workflow

1. Open the **Dashboard**.
2. Click **Load Candidate Database**.
3. Enter a job role and click **Start Recruitment Process**.
4. Use **Find Profiles** to search the candidate database.
5. Use **Screen CVs** to rank candidates.
6. Use **Schedule Interviews** to send Gmail invitations.
7. Generate and download the final recruitment report.

The **Chat Assistant** can answer questions about candidates and the current recruitment workflow after the database has been loaded.

## Technology

- Python 3.11
- Streamlit
- CrewAI
- Groq API with `openai/gpt-oss-120b`
- ChromaDB
- Pandas and OpenPyXL
- Gmail SMTP
- FPDF

## Project Structure

```text
.
├── agents/                 # CrewAI agents and recruitment tools
├── data/
│   ├── cs_engineers.xlsx   # Candidate source database
│   └── chromadb_data/      # Local runtime vector-store data
├── tasks/                  # CrewAI task definitions
├── utils/                  # Database helpers
├── app2.py                 # Streamlit application entry point
├── main3.py                # Command-line workflow entry point
├── requirements.txt        # Python dependencies
├── runtime.txt             # Streamlit Cloud Python version
└── .env.example            # Local environment variable template
```

## Run Locally

Use Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root using `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key
GMAIL_SENDER=your_gmail_address@gmail.com
GMAIL_PASSWORD=your_gmail_app_password
```

Start the Streamlit application:

```powershell
streamlit run app2.py
```

Open `http://localhost:8501` in your browser.

The command-line workflow can be started with:

```powershell
python main3.py
```

## Streamlit Community Cloud Deployment

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Create or select the app connected to this GitHub repository.
3. Use branch `main` and main file `app2.py`.
4. Open the deployed app's **Manage app** menu.
5. Go to **Settings > Secrets**.
6. Add the following TOML values:

```toml
GROQ_API_KEY = "your_groq_api_key"
GMAIL_SENDER = "your_gmail_address@gmail.com"
GMAIL_PASSWORD = "your_gmail_app_password"
```

7. Save the secrets and reboot the app.

The repository includes `runtime.txt` to keep Streamlit Cloud on Python 3.11, which is required by the current CrewAI and ChromaDB dependency combination.

## Credentials and Security

- Never commit `.env` or real API keys to GitHub.
- Use Streamlit Cloud Secrets for deployed credentials.
- Use a Gmail App Password rather than a normal Gmail password.
- Rotate any API key or password that has been exposed publicly.
- The application uses synthetic candidate data from `data/cs_engineers.xlsx`.

## Data and Persistence

Candidate profiles are loaded from `data/cs_engineers.xlsx` into ChromaDB when **Load Candidate Database** is clicked. Generated ChromaDB files are local runtime data and are excluded from Git tracking.

Streamlit Cloud uses an ephemeral filesystem, so reload the candidate database after an app restart if necessary.

## Troubleshooting

### `GROQ_API_KEY is missing`

Add `GROQ_API_KEY` in Streamlit Cloud under **Manage app > Settings > Secrets**, then reboot the app.

### Pydantic or ChromaDB import errors

Ensure the deployment uses Python 3.11. This repository provides `runtime.txt` with the required version.

### Gmail authentication fails

Check that:

- 2-Step Verification is enabled on the Gmail account.
- `GMAIL_SENDER` is the correct Gmail address.
- `GMAIL_PASSWORD` is a current 16-character Gmail App Password.
- The App Password is entered without spaces.

### Candidate database is empty

Click **Load Candidate Database** from the Dashboard before searching or screening profiles.

## License

This project is provided for educational and internal demonstration purposes.
