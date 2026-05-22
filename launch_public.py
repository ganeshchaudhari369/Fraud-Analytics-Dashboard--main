from pyngrok import ngrok
from app import app
import os

# --- INSTRUCTIONS ---
# 1. Get your FREE authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
# 2. Replace the token below with your actual token
# --------------------
NGROK_AUTH_TOKEN = "3CzuATHKtxTcxQmkFIGlifBYNx3_abrrpjpqKzAeZZFU3ARR"

if __name__ == '__main__':
    # Set authtoken
    if NGROK_AUTH_TOKEN and NGROK_AUTH_TOKEN != "3CzuATHKtxTcxQmkFIGlifBYNx3_abrrpjpqKzAeZZFU3ARR":
        print("Applying ngrok auth token...")
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    
    # Open a tunnel on port 8080
    public_url = ngrok.connect(8080)
    print(f" * Public URL: {public_url}")
    print(" * Dashboard is now accessible from anywhere!")
    
    # Run the Dash app
    app.run(host='0.0.0.0', port=8080, debug=False)
