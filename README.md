# Fraud-Analytics-Dashboard--main
An interactive Python dashboard built with Dash, Plotly, and Bootstrap to analyze fraud detection data from a managerial perspective.
Features
Interactive KPIs: Real-time tracking of transaction volume, fraud cases, and financial risk.
Hourly Analysis: Line charts visualizing peak fraud hours.
Store Type Risk Profiling: Comparative analysis of fraud incidence across different store types.
Behavioral Analytics: Distribution of transaction amounts and geographical distance risks.
Dynamic Filtering: Filter data by Store Type and Hour of Day.
Preview
The dashboard provides a clean, professional interface using the LUX theme.

Installation
Clone the repository:

git clone <your-repo-url>
cd "Python Dashboard"
Install dependencies:

pip install dash dash-bootstrap-components pandas plotly
Run the application:

python app.py
Open http://localhost:8080 in your browser.

Public Access (via ngrok)
To make your dashboard accessible over the internet:

Install pyngrok:

pip install pyngrok
Get a free authtoken from ngrok.com.

Set your authtoken in your environment or edit launch_public.py.

Run the public launcher:

python launch_public.py
A public URL (e.g., https://xxxx.ngrok-free.app) will be displayed in the terminal.

Data
The project uses fraud.csv. Ensure this file is present in the root directory.
