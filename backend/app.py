from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import whois
import datetime
import re

app = Flask(__name__)
CORS(app)

# Load the AI Brain
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def check_domain_age(url):
    """
    FORENSIC CHECK: Returns True if domain is < 30 days old (High Risk).
    """
    try:
        # Extract domain from link (e.g., http://evil.com/login -> evil.com)
        domain = re.findall(r'://([^/]+)', url)
        if not domain: return False
        
        domain_name = domain[0]
        w = whois.whois(domain_name)
        
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days
            print(f"Domain: {domain_name}, Age: {age} days")
            if age < 30: # Flag domains younger than a month
                return True
    except Exception as e:
        print(f"Whois Error: {e}")
    return False

@app.route('/scan', methods=['POST'])
def scan_email():
    data = request.json
    email_text = data.get('email_text', '')
    links = data.get('links', []) # List of URLs found in email

    response_details = []
    risk_score = 0

    # 1. AI ANALYSIS
    # Transform text to numbers and predict
    text_vector = vectorizer.transform([email_text])
    ai_prediction = model.predict(text_vector)[0] # 0 or 1
    ai_prob = model.predict_proba(text_vector)[0][1] * 100 # Probability %
    
    if ai_prediction == 1:
        risk_score += 50
        response_details.append(f"AI Detection: Language patterns indicate phishing ({int(ai_prob)}% confidence).")

    # 2. FORENSIC ANALYSIS (Domain Age)
    # Check the first link found in the email
    if links:
        is_new_domain = check_domain_age(links[0])
        if is_new_domain:
            risk_score += 40
            response_details.append("Forensic Alert: Linked domain is less than 30 days old.")

    # 3. CALCULATE VERDICT
    verdict = "Safe"
    color = "green"
    
    if risk_score >= 80:
        verdict = "MALICIOUS"
        color = "red"
    elif risk_score >= 40:
        verdict = "SUSPICIOUS"
        color = "orange"

    if not response_details:
        response_details.append("No threats detected.")

    return jsonify({
        "verdict": verdict,
        "score": risk_score,
        "color": color,
        "reasons": response_details
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    