# Registration Intelligence & Attendee Management System

## Run it

1. Open a terminal in this folder.
2. Create and activate a virtual environment (recommended): `python -m venv .venv`, then `.venv\\Scripts\\activate` on Windows.
3. Install packages: `pip install -r requirements.txt`.
4. Start the system: `python app.py`.
5. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created automatically at `instance/database.db` when you first start the app.

## Gemini (optional)

Set your API key before starting the app:

`$env:GEMINI_API_KEY="your-key"`

You can optionally set `GEMINI_MODEL` if your Google account uses a different Gemini model. Without a key, the Insights page still shows calculated data-driven insights.

## Real attendee email alerts

1. Copy `.env.example` and rename the copy to `.env` in the project folder.
2. Enter the SMTP settings from your email provider in `.env`.
3. Run `pip install -r requirements.txt` once, then restart with `python app.py`.
4. Open **Notifications**. The page will show **Email delivery connected** when the settings are detected. Use **Send test email** before sending attendee notifications.

For providers that use TLS, use port `587` and `SMTP_USE_SSL=false`. For providers that require SSL, use port `465` and `SMTP_USE_SSL=true`. Use an app password where your provider requires one. Never share or commit your `.env` file.

## CSV/Excel import headings

`name,email,phone,age,gender,organization,city,category,event`
