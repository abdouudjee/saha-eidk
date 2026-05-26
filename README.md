# SAHA EIDK

## A Python-based CLI tool to automate sending customized greetings to your Telegram contacts, active direct messages, and archived chats.

## Setup Guide

### 1. Get Telegram API Credentials

To communicate with the Telegram API, you need to obtain an API ID and Hash:

1. Go to [my.telegram.org](https://my.telegram.org/) and log in with your Telegram phone number.
2. Navigate to **API development tools**.
3. Create a new application (fill in the app title and short name as desired).
4. Copy your **App api_id** and **App api_hash**.
5. Paste these values directly into the configuration variables at the top of `src/main.py`.

### 2. Clone the Repository

Clone the codebase to your local machine using git:

```bash
git clone https://github.com/abdouudjee/saha-eidk.git
cd saha-eidk
```
````

### 3. Initialize a Virtual Environment

Create and activate an isolated virtual environment to keep your project dependencies clean:

- **Windows (PowerShell/CMD):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **mac/linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Project Dependencies

Ensure your environment is active (venv), then install the required packages from the root directory:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Navigate into the source folder where your code lives and execute the main script:

```bash
cd src
```

change the greeting message in main.py

```bash
greeting = "hello"
```

then run

```bash
py main.py
```
