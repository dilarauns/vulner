import requests 
import json
import openai
import os

openai.api_key = 'your_api_key'

def analyze_code_with_ollama(code):
    prompt = (
        "Identify the security vulnerabilities present in this code. "
        "Additionally, check for the following potential vulnerabilities and, if any are found, respond in detail: "
        "1. SQL Injection "
        "2. Cross-Site Scripting (XSS) "
        "3. Cross-Site Request Forgery (CSRF) "
        "4. Insecure Direct Object References (IDOR) "
        "5. Insecure data storage "
        "6. Weak authentication and session management "
        "7. Misconfigurations "
        "8. Known security vulnerabilities "
        "9. Other potential security vulnerabilities."
    )
    url = "http://localhost:11434/api/generate"  # URL'yi uygun şekilde ayarlayın
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt + " " + code,
            "model": "llama3",
            "created_at": "2023-11-03T15:36:02.583064Z",
            "stream": False,
            "done": True,
            }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        try:
            response_text = response.text   
            data = json.loads(response_text)
            actual_response= data["response"]
            print(actual_response)
        except ValueError:
            print("Response is not in JSON format:", response.text)
            return None
    else:
        print("Request failed with status code:", response.status_code)
        return response.text

def get_fix_suggestions(vulnerabilities):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The security vulnerabilities found in this code are: {vulnerabilities}. How can I fix these vulnerabilities? Provide detailed suggestions for each vulnerability with code examples and best security practices."}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    suggestions = response.choices[0].message["content"].strip()
    return suggestions

def analyze_and_fix_code(file_path):
    with open(file_path, 'r') as file:
        code_content = file.read()

    vulnerabilities = analyze_code_with_ollama(code_content)
    
    if vulnerabilities:
        print(f"Security Vulnerabilities in {file_path}:")
        print(vulnerabilities)

        fix_suggestions = get_fix_suggestions(vulnerabilities)
        print(f"Fix Suggestions for {file_path}:")
        print(fix_suggestions)
    else:
        print(f"Failed to analyze {file_path}")

def analyze_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                analyze_and_fix_code(file_path)

if __name__ == "__main__":
    directory_path = "your_directory" 
    analyze_directory(directory_path)
