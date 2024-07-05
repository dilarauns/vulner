from langchain_community.llms import Ollama
import openai
import os


ollama = Ollama(model="llama3")


openai.api_key = 'YOUR_API_KEY'

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
    response = ollama.invoke(prompt + " " + code , server_url="http://127.0.0.1:11434")
    return response

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
    print(f"Security Vulnerabilities in {file_path}:")
    print(vulnerabilities)


    fix_suggestions = get_fix_suggestions(vulnerabilities)
    print(f"Fix Suggestions for {file_path}:")
    print(fix_suggestions)

def analyze_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                analyze_and_fix_code(file_path)

if __name__ == "__main__":
    directory_path = "your_folder_path" 
    analyze_directory(directory_path)
