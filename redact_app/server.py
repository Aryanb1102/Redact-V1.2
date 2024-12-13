import os
import re
import subprocess
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Environment Variables for Real Queries
HIBP_API_KEY = os.environ.get("HIBP_API_KEY")     # Must be set
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") # Must be set
GOOGLE_CX = os.environ.get("GOOGLE_CX_ID")        # Must be set

def haveibeenpwned_check(email):
    """Check if an email is found in known data breaches via Have I Been Pwned."""
    if not HIBP_API_KEY:
        return []
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"User-Agent": "DataPrivacyApp", "hibp-api-key": HIBP_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()  # List of breach objects
    return []

def google_custom_search(query):
    """Use Google Custom Search API to find references of the query."""
    if not GOOGLE_API_KEY or not GOOGLE_CX:
        return []
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={query}"
    r = requests.get(url)
    if r.status_code == 200:
        items = r.json().get("items", [])
        return [i["link"] for i in items]
    return []

def run_spiderfoot(email):
    """
    Run SpiderFoot as a subprocess to find leaked/pasted references for the given email.
    Using relevant modules: sfp_leaks, sfp_breaches, sfp_pastes, sfp_search
    """
    command = [
        "spiderfoot",
        "-s", email,
        "-q", "sfp_leaks,sfp_breaches,sfp_pastes,sfp_search",
        "-t", "email"
    ]
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate(timeout=60)  # Wait up to 60s
        output = out.decode(errors='ignore')
        results = []
        for line in output.split('\n'):
            # We'll collect lines containing the email
            if email.lower() in line.lower():
                results.append(line.strip())
        return results
    except subprocess.TimeoutExpired:
        proc.kill()
        return []
    except FileNotFoundError:
        # If spiderfoot command not found in PATH
        return []

def comprehensive_search(name, email):
    """Perform OSINT-based search with Have I Been Pwned, Google Dorking, and SpiderFoot."""
    results = []

    # 1. Have I Been Pwned
    hibp_results = haveibeenpwned_check(email)
    if hibp_results:
        breach_names = [b['Name'] for b in hibp_results if 'Name' in b]
        results.append({
            "website": "Have I Been Pwned",
            "url": "https://haveibeenpwned.com/",
            "deletion_possible": False,
            "manual_steps": f"Email found in {', '.join(breach_names)} breach(es).",
            "contact_method": "Contact each breach source for removal."
        })

    # 2. Google Dorking (example: searching pastebin)
    paste_results = google_custom_search(f'site:pastebin.com "{email}"')
    for link in paste_results:
        results.append({
            "website": "Pastebin Leak",
            "url": link,
            "deletion_possible": False,
            "manual_steps": "Check the paste for personal info. Request removal from pastebin if needed.",
            "contact_method": link
        })

    # 3. SpiderFoot
    spiderfoot_data = run_spiderfoot(email)
    for line in spiderfoot_data:
        results.append({
            "website": "SpiderFoot OSINT",
            "url": "N/A",
            "deletion_possible": False,
            "manual_steps": f"Reference found: {line}",
            "contact_method": "Review source for removal."
        })

    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_data():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and Email required"}), 400

    final_results = comprehensive_search(name, email)
    return jsonify({"results": final_results})

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    website = data.get("website")
    user_name = data.get("name")
    user_email = data.get("email")

    if not website or not user_name or not user_email:
        return jsonify({"error": "Website, Name, and Email required"}), 400

    contact_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', website)
    if contact_email:
        target_email = contact_email.group(0)
    else:
        clean_domain = website.replace("https://", "").replace("http://", "").split("/")[0]
        target_email = "support@" + clean_domain

    email_template = f"""
Subject: Request for Data Deletion (DPDPA / GDPR / CCPA Compliance)

Dear {website},

I am writing to request the deletion of all personal data associated with my account and personal information.
My email is {user_email} and my name is {user_name}.

In compliance with the Indian Digital Personal Data Protection Act (DPDPA) as well as GDPR and CCPA, 
please remove all my personal data from your systems. Confirm once the deletion is complete.

Thank you,
{user_name}
""".strip()
    return jsonify({"email_template": email_template, "contact_email": target_email})

if __name__ == '__main__':
    app.run(debug=True)