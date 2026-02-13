# Cloud Execution Setup Guide (GitHub Actions)

To ensure your bot runs every day even when your laptop is **shutdown, broken, or offline**, follow these steps to host it on GitHub for free.

### 1. Upload to GitHub
1. Create a new **Private Repository** on your GitHub account.
2. Push this project to that repository.

### 2. Configure Secrets (CRITICAL)
Your API keys and passwords should **NOT** be in the code. I have set up the cloud bot to read them from **GitHub Secrets**:
1. Go to your GitHub repository.
2. Click **Settings** > **Secrets and variables** > **Actions**.
3. Add the following **New repository secrets**:
   - `GEMINI_API_KEY`: Your Google Gemini API Key.
   - `SENDER_EMAIL`: `bhuvanesh0709@gmail.com`
   - `SENDER_PASSWORD`: `wdswyhlevlktbuyd`
   - `RECEIVER_EMAIL`: `bhuvanesh0709@gmail.com`

### 3. How it Works
- **Automation**: The bot will run automatically every day at **9:30 AM IST** (4:00 AM UTC).
- **Manual Trigger**: You can go to the **Actions** tab on GitHub and click "Run workflow" to start it anytime.
- **Reliability**: Since it runs on GitHub's servers, it will never stop even if your laptop is off.

### 4. Emails
The bot will continue to send the Excel report to your Gmail just like the local version does.
