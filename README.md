# Grammar & Style Helper

A simple web tool that checks a paragraph of text for grammar mistakes and suggests better word choices.

## What it does
- You paste text into a box on a webpage.
- It checks grammar using the free LanguageTool API.
- It checks for weak/overused words (like "good", "very", "thing") and suggests stronger alternatives, using logic you wrote yourself.

## Step 1: Install Python
If you don't already have Python installed:
1. Go to https://www.python.org/downloads/
2. Download and install the latest version (check "Add Python to PATH" during install on Windows).
3. Confirm it worked by opening a terminal (Command Prompt / Terminal app) and typing:
   ```
   python --version
   ```

## Step 2: Get the project files
Download this folder (`grammar-helper`) to your computer, e.g. to your Desktop.

## Step 3: Open a terminal in the project folder
- Windows: open the folder, click the address bar, type `cmd`, press Enter.
- Mac: right-click the folder > "New Terminal at Folder" (or use `cd path/to/grammar-helper` in Terminal).

## Step 4: Install the required libraries
In the terminal, run:
```
pip install -r requirements.txt
```
This installs Flask (the tool that runs the website) and Requests (used to call the grammar-check API).

## Step 5: Run the app
```
python app.py
```
You should see something like:
```
Running on http://127.0.0.1:5000
```

## Step 6: Open it in your browser
Go to: http://127.0.0.1:5000

Paste in some text and click "Check". You'll see grammar suggestions and word-choice suggestions appear below.

## How to explain this project in your application
- **Problem it solves:** helps English learners (like yourself, preparing for IELTS) catch grammar mistakes and upgrade weak vocabulary in their writing.
- **What you built yourself:** the weak-word detection logic and the whole web interface — the grammar-checking itself uses an existing free API, which is a completely normal and expected practice in real software engineering (nobody reinvents grammar checking from scratch).
- **What you'd improve next:** you could mention wanting to add synonym suggestions using NLP libraries like spaCy, or support for other languages.

## Extending it further (optional, if you want to go further)
- Add more words to the `WEAK_WORD_SUGGESTIONS` dictionary in `app.py`.
- Add a readability score (e.g. Flesch-Kincaid formula) to tell users if their writing is too complex or too simple.
- Deploy it online for free using a service like Render or PythonAnywhere, so you can share a live link in your application instead of just code.
