# AI-Powered Abroad Job Scraping & Auto-Mailing System

An automated tool to find international job opportunities, rank them using AI, and deliver a daily report via email.

## Setup

1.  **Clone the repository**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```
3.  **Configure environment variables**:
    Create a `.env` file based on `.env.example`.
4.  **Run the application**:
    ```bash
    python src/main.py
    ```

## Features
- **Global Job Scraping**: Automated collection from LinkedIn and RemoteOK (expandable).
- **AI-Powered Filtering**: Uses Gemini 1.5 Flash to rank jobs against your resume.
- **Visa Sponsorship Detection**: AI-inferred likelihood of sponsorship for international roles.
- **Excel Reporting**: Structured `.xlsx` report with job details, AI summaries, and custom cover letter drafts.
- **Email Automation**: Automatic daily delivery to your inbox.
- **Scheduling**: Windows batch file included for easy task scheduling.

## Technical Architecture
1. **Scraper**: Uses Playwright for robust web interaction.
2. **Processor**: Leverages Google Gemini for NLP tasks (ranking, summarizing, cover letters).
3. **Exporter**: Pandas and OpenPyXL for data processing and Excel generation.
4. **Notifier**: Python's `smtplib` for secure email transmission.

## Setup Instructions
1. Install Requirements: `python setup.py`
2. Configure `.env`: Copy `.env.example` to `.env` and fill in your keys and preferences.
3. Run Manually: `python main.py`
4. Schedule: Use `run_daily.bat` with Windows Task Scheduler to automate.
