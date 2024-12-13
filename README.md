# Redact-V1.2

**Redact - OSINT Data Finder**
==============================

Redact is a Flask-based web application that uses Open Source Intelligence (OSINT) techniques to help users identify where their personal data might be exposed on the internet. The app integrates with **SpiderFoot**, **Google Custom Search**, and (optionally) **Have I Been Pwned (HIBP)** to provide actionable insights.

**Features**
------------

*   **Search for Personal Data Exposure**:
    
    *   Identifies potential data breaches and public mentions of your email on paste sites or other sources.
        
    *   Displays results with actionable steps for data deletion.
        
*   **Generate Data Deletion Requests**:
    
    *   Create pre-filled emails compliant with **DPDPA**, **GDPR**, and **CCPA** to request personal data deletion.
        
*   **Integration Options**:
    
    *   **SpiderFoot**: Leverages free modules for OSINT.
        
    *   **Google Custom Search**: Enables targeted searches for leaks and breaches.
        
    *   **Have I Been Pwned (Optional)**: Checks for email breaches in known datasets.
        

**Requirements**
----------------

### **Prerequisites**

*   Python 3.7+
    
*   Pip (Python Package Manager)
    

### **Libraries**

Install the required Python packages by running:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy codepip install -r requirements.txt   `

### **Optional API Keys**

*   **Have I Been Pwned (HIBP)**: Obtain an API key here.
    
*   **Google Custom Search**: Get a key and CX ID from Google Custom Search API.
    

Set these keys as environment variables:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopy code# Linux/Mac  export HIBP_API_KEY="your_hibp_api_key"  export GOOGLE_API_KEY="your_google_api_key"  export GOOGLE_CX_ID="your_google_cx_id"  # Windows (Powershell)  $env:HIBP_API_KEY="your_hibp_api_key"  $env:GOOGLE_API_KEY="your_google_api_key"  $env:GOOGLE_CX_ID="your_google_cx_id"   `

If the keys are not provided, these services will be skipped without affecting the other functionalities.

**Installation**
----------------

1.  bashCopy codegit clone https://github.com/your-repository/redact-osint.gitcd redact-osint
    
2.  bashCopy codepython -m venv .venvsource .venv/bin/activate # On Linux/Mac.\\.venv\\Scripts\\activate # On Windows
    
3.  bashCopy codepip install -r requirements.txt
    
4.  Ensure that the spiderfoot command is accessible via PATH.
    
    *   bashCopy codewget https://github.com/smicallef/spiderfoot/archive/v4.0.tar.gztar zxvf v4.0.tar.gzcd spiderfoot-4.0pip install -r requirements.txt
        
    *   bashCopy codegit clone https://github.com/smicallef/spiderfoot.gitcd spiderfootpip install -r requirements.txt
        

**Usage**
---------

### **Running the Application**

1.  bashCopy codepython server.py
    
2.  Open the app in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).
    

### **Searching for Personal Data**

1.  Enter your name and email on the search form.
    
2.  Click **Search**.
    
3.  View the results showing:
    
    *   Websites where your data may be exposed.
        
    *   Steps for data deletion or further investigation.
        

### **Generating Deletion Emails**

1.  Enter the website, your name, and your email in the email generator form.
    
2.  Click **Generate Email**.
    
3.  Copy the pre-filled email and send it to the suggested contact address.
    

**Project Structure**
---------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   plaintextCopy coderedact_app/  ├── requirements.txt          # Dependencies for the project  ├── server.py                 # Flask backend handling OSINT searches  ├── templates/  │   └── index.html            # Frontend HTML interface  └── static/      ├── main.js               # JavaScript for interactivity      └── spinner.gif           # Loading animation   `

**API Integrations**
--------------------

### **1\. SpiderFoot**

*   Modules used:
    
    *   sfp\_leaks: Finds leaked data.
        
    *   sfp\_breaches: Checks for data breaches.
        
    *   sfp\_pastes: Scans paste sites for mentions.
        
    *   sfp\_search: Performs general searches.
        
*   SpiderFoot runs locally without additional API keys.
    

### **2\. Google Custom Search**

*   Requires an API key and CX ID for querying specific domains like pastebin.com.
    
*   Results show URLs where the email is mentioned.
    

### **3\. Have I Been Pwned**

*   Provides breach data associated with your email.
    
*   Requires an API key (free tier available with limited queries).
    

**Known Limitations**
---------------------

*   **Paid API Requirements**: Google Custom Search and HIBP require user-provided API keys for full functionality.
    
*   **Free SpiderFoot Limitations**: SpiderFoot’s free modules provide limited coverage. Additional modules may require configuration.
    
*   **DPDPA Compliance**: While the app generates DPDPA-compliant emails, manual confirmation is required for each data deletion request.
    

**Future Enhancements**
-----------------------

*   Add support for more OSINT modules (e.g., Shodan, VirusTotal).
    
*   Enable multi-language support for data deletion emails.
    
*   Integrate a centralized database of Indian data brokers for targeted searches.
    

**License**
-----------

This project is licensed under the MIT License. See the LICENSE file for details.

**Redact - Empowering Individuals to Take Control of Their Data.**
