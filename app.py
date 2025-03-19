from flask import Flask, request, render_template
import joblib
import numpy as np
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Load the XGBoost model
def load_model(model_path='xgb_model.pkl'):
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        print("Model file not found!")
        return None

# Feature extraction function
def extract_features(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname if parsed_url.hostname else ""
    path = parsed_url.path if parsed_url.path else ""

    features = {
        'Have_IP': 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 0,
        'Have_At': 1 if '@' in url else 0,
        'URL_Length': len(url),
        'URL_Depth': path.count('/'),
        'Redirection': 1 if '//' in url[7:] else 0,
        'https_Domain': 1 if 'https' in parsed_url.scheme else 0,
        'TinyURL': 1 if 'tinyurl' in url else 0,
        'Prefix/Suffix': 1 if '-' in hostname else 0,
        'DNS_Record': 1 if hostname != '' else 0,
        'Web_Traffic': 1 if len(url) > 20 else 0, 
        'Domain_Age': 1 if len(hostname.split('.')) > 2 else 0,
        'Domain_End': 1 if hostname.endswith(('.com', '.org', '.net')) else 0,
        'iFrame': 1 if '<iframe' in url else 0,
        'Mouse_Over': 1 if 'mouseover' in url else 0,
        'Right_Click': 1 if 'rightclick' in url else 0,
        'Web_Forwards': 1 if 'forward' in url else 0,
    }
    return list(features.values())

# Predict URL safety
def predict_url_safety(url):
    model = load_model()
    if model is None:
        return "Model not found. Train the model first."
    
    features = extract_features(url)
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)
    
    return "safe" if prediction[0] == 0 else "not safe"

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        url = request.form['url']
        prediction = predict_url_safety(url)
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
