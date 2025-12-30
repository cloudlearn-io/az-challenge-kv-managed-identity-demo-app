# app.py
from flask import Flask, render_template_string
import os

# Initialize the Flask application
app = Flask(__name__)

# HTML template for the challenge lab web page
# This displays secrets retrieved from Azure Key Vault via environment variables
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Key Vault Challenge Lab</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        }
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
        }
        .secret-box {
            background: linear-gradient(145deg, #f1f5f9 0%, #e2e8f0 100%);
            border-left: 4px solid #3b82f6;
        }
        .success-box {
            background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
            border-left: 4px solid #10b981;
        }
        .error-box {
            background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
            border-left: 4px solid #ef4444;
        }
        .key-icon {
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
        }
    </style>
</head>
<body class="flex items-center justify-center p-6">
    <div class="card rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
        <!-- Header -->
        <div class="text-center mb-8">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-blue-600 key-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
                </svg>
            </div>
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Key Vault Challenge</h1>
            <p class="text-gray-500">Secrets retrieved from Azure Key Vault</p>
        </div>

        <!-- Secrets Display -->
        <div class="space-y-4">
            <!-- App Name Secret -->
            <div class="{% if app_name and 'not configured' not in app_name.lower() %}success-box{% else %}error-box{% endif %} rounded-lg p-4">
                <div class="flex items-center justify-between">
                    <div>
                        <span class="text-xs font-semibold uppercase tracking-wider {% if app_name and 'not configured' not in app_name.lower() %}text-emerald-600{% else %}text-red-600{% endif %}">APP-NAME</span>
                        <p class="text-lg font-medium text-gray-800 mt-1">{{ app_name }}</p>
                    </div>
                    {% if app_name and 'not configured' not in app_name.lower() %}
                    <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {% else %}
                    <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {% endif %}
                </div>
            </div>

            <!-- Secret Message -->
            <div class="{% if secret_message and 'not configured' not in secret_message.lower() %}success-box{% else %}error-box{% endif %} rounded-lg p-4">
                <div class="flex items-center justify-between">
                    <div>
                        <span class="text-xs font-semibold uppercase tracking-wider {% if secret_message and 'not configured' not in secret_message.lower() %}text-emerald-600{% else %}text-red-600{% endif %}">SECRET-MESSAGE</span>
                        <p class="text-lg font-medium text-gray-800 mt-1">{{ secret_message }}</p>
                    </div>
                    {% if secret_message and 'not configured' not in secret_message.lower() %}
                    <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {% else %}
                    <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {% endif %}
                </div>
            </div>

            <!-- API Key -->
            <div class="{% if api_key and 'not configured' not in api_key.lower() %}success-box{% else %}error-box{% endif %} rounded-lg p-4">
                <div class="flex items-center justify-between">
                    <div>
                        <span class="text-xs font-semibold uppercase tracking-wider {% if api_key and 'not configured' not in api_key.lower() %}text-emerald-600{% else %}text-red-600{% endif %}">API-KEY</span>
                        <p class="text-lg font-medium text-gray-800 mt-1 font-mono">{{ api_key }}</p>
                    </div>
                    {% if api_key and 'not configured' not in api_key.lower() %}
                    <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {% else %}
                    <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Status Summary -->
        <div class="mt-8 pt-6 border-t border-gray-200">
            {% set success_count = 0 %}
            {% if app_name and 'not configured' not in app_name.lower() %}{% set success_count = success_count + 1 %}{% endif %}
            {% if secret_message and 'not configured' not in secret_message.lower() %}{% set success_count = success_count + 1 %}{% endif %}
            {% if api_key and 'not configured' not in api_key.lower() %}{% set success_count = success_count + 1 %}{% endif %}
            
            <div class="flex items-center justify-center space-x-2">
                {% if success_count == 3 %}
                <span class="inline-flex items-center px-4 py-2 rounded-full bg-emerald-100 text-emerald-800 font-medium">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    All secrets loaded successfully!
                </span>
                {% else %}
                <span class="inline-flex items-center px-4 py-2 rounded-full bg-amber-100 text-amber-800 font-medium">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                    </svg>
                    {{ success_count }}/3 secrets configured
                </span>
                {% endif %}
            </div>
        </div>

        <!-- Footer -->
        <div class="mt-6 text-center text-sm text-gray-400">
            CloudLearn Challenge Lab
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """
    Renders the home page displaying secrets from Key Vault.
    Retrieves APP_NAME, SECRET_MESSAGE, and API_KEY from environment variables.
    These should be configured as Key Vault references in the Web App settings.
    """
    app_name = os.environ.get('APP_NAME', 'Not configured - Create APP-NAME secret in Key Vault')
    secret_message = os.environ.get('SECRET_MESSAGE', 'Not configured - Create SECRET-MESSAGE secret in Key Vault')
    api_key = os.environ.get('API_KEY', 'Not configured - Create API-KEY secret in Key Vault')
    
    return render_template_string(
        HTML_TEMPLATE,
        app_name=app_name,
        secret_message=secret_message,
        api_key=api_key
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))