# dcx_dashboard

## Obtain API Keys
Sign Up:

Visit the CoinDCX API Dashboard and sign up for an account.
https://coindcx.com/api-dashboard
Generate API Keys:

After logging in, navigate to the API section and generate your API keys (API Key and API Secret).


Installation
Clone the Repository:
```bash
git clone https://github.com/your-repo/coindcx-api-tutorial.git
cd coindcx-api-tutorial
```

Create and Activate a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use 'venv\Scripts\activate'
```
Install Dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Create a .env File:

In the project root directory, create a .env file and add your API keys:

COINDCX_API_KEY=your_api_key
COINDCX_API_SECRET=your_api_secret
DB_CONN_String=connection_string_for_mongoDb




## Deploying on render
```bash
gunicorn --bind 0.0.0.0:8000 coin_dashboard.wsgi:application
```
