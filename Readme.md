🧠 AutoFormFiller – Smart Form Automation with AI
This project is a modular, Python-based automation tool designed to fill out web forms intelligently using a language model and Selenium. It scrapes form fields, matches them against structured user info, and uses LLM reasoning to auto-complete and navigate forms like a human would.

🚀 Features
✅ Dynamic form field extraction using Selenium

🧠 LLM-assisted reasoning to select values for each field

🎯 Smart button/link decisioning (e.g., choosing "Next", "Submit", etc.)

🧩 Modular architecture using just two files: main.py and form_engine.py

📁 File Structure
bash
Copy
Edit
.
├── main.py            # Main script – handles logic flow, automation loop
├── core.py     # Shared components: schemas, driver/model setup, helpers
└── README.md
🛠️ Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/RohanDisa/autoformfiller.git
cd autoformfiller
2. Install dependencies
Make sure you’re using Python 3.9+

bash
Copy
Edit
pip install -r requirements.txt
Example packages used:

undetected-chromedriver

selenium

pydantic

pydantic-ai

pydantic-ai[groq]

3. Add your Groq API key
In form_engine.py, replace:

python
Copy
Edit
GroqProvider(api_key="<your_groq_api_key>")
with your actual key.

🧪 Usage
Just run the main script:

bash
Copy
Edit
python main.py
It will launch a browser, navigate to the form, analyze the inputs, and intelligently fill and proceed through the pages.

📌 Notes
Currently configured for ApplyWeb forms, but extensible.

Add logic as needed in main.py to fit additional forms or field types.

Make sure form fields are visible and not behind CAPTCHAs or logins.


