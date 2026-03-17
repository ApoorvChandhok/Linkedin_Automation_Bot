# 🤖 LinkedIn Automation Bot

An intelligent, AI-assisted bot designed to automatically search and apply for jobs on LinkedIn using "Easy Apply", saving you hours of mindless scrolling. 

This repository includes a significantly enhanced questionnaire handler and advanced AI integrations (OpenAI, Gemini, DeepSeek) for analyzing Job Descriptions and extracting critical data.

## ✨ Features

- **Automated Applications**: Automates the entire LinkedIn "Easy Apply" process based on customizable search filters.
- **Smart Questionnaire Handling**: Intelligently parses dropdowns, radios, checks, and text boxes. Uses fuzzy-matching to answer forms accurately based on your `config` variables.
- **Advanced AI Integration**: Falls back on OpenAI, Gemini, or DeepSeek to analyze difficult job requirement questions and formulate human-like responses.
- **Detailed Job Tracking (Enhanced)**: Maintains an `all_applied_applications_history.csv` log, mapping out:
  - Job Application Link
  - **Extracted Salary Requirements**
  - **AI-Calculated Profile Match (%)**
  - Resume variant used
- **Browser Isolation**: Run the bot via an isolated "Safe Mode" profile, allowing you to use your regular browser normally while the bot runs in the background.

## 🚀 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ApoorvChandhok/Linkedin_Automation_Bot.git
   ```
2. Make sure you have **Google Chrome** installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have installed standard packages like `selenium`, `pyautogui`, `openai`, and `google-generativeai`)*

## ⚙️ Configuration

All user-specific configurations are stored safely in the `/config` directory. 

1. **`secrets.py`**: Add your LinkedIn Account credentials and API Keys (OpenAI / DeepSeek / Gemini) here.
2. **`personals.py`**: Define your basic information like name, location, and EEO answers.
3. **`questions.py`**: Provide default answers for common application questions (years of experience mapped to specific skills, salary expectations, etc.)
4. **`search.py`**: Configure your desired Job Titles, locations, and LinkedIn filters (e.g., Remote, Entry level, Past 24 hours).
5. **`settings.py`**: Toggle major bot behaviors like `safe_mode` (isolated browser), `run_in_background` (headless mode), and `stealth_mode`.

## 🏃‍♂️ Usage

After filling out the configuration files, simply launch the bot:

```bash
python runAiBot.py
```

Sit back and monitor the terminal as it hunts down job listings, evaluates the descriptions, and submits applications on your behalf! 

## ⚠️ Notes & Disclaimer

- The use of automated bots on LinkedIn violates their Terms of Service. It's recommended to utilize delay timers (`click_gap`) and limit daily application volume to prevent account restrictions.
- You remain entirely responsible for your account's safety.
