from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import (create_user, verify_user, get_user_by_email, update_password,
                      generate_otp, verify_otp, save_history, get_history, get_history_by_id, delete_history_by_id, delete_all_history)
from config import SECRET_KEY, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, GROQ_API_KEY, MISTRAL_API_KEY
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import re

app = Flask(__name__)
app.secret_key = SECRET_KEY

GROQ_MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B (Versatile)",
    "llama-3.1-8b-instant": "Llama 3.1 8B (Fast)",
    "mixtral-8x7b-32768": "Mixtral 8x7B",
    "gemma2-9b-it": "Gemma2 9B"
}

MISTRAL_MODELS = {
    "mistral-large-latest": "Mistral Large",
    "mistral-small-latest": "Mistral Small",
    "open-mixtral-8x7b": "Open Mixtral 8x7B"
}

def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def call_groq(model, messages, temperature=0.1, max_tokens=3000):
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def call_mistral(model, messages, temperature=0.1, max_tokens=3000):
    import requests
    resp = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {MISTRAL_API_KEY}"},
        json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def ai_call(provider, model, messages, temperature=0.1, max_tokens=3000):
    if provider == "mistral":
        return call_mistral(model, messages, temperature, max_tokens)
    return call_groq(model, messages, temperature, max_tokens)

def analyze_code(code, language, provider, model):
    prompt = f"""You are an expert code reviewer. Analyze the following {language} code and return ONLY valid JSON.

Return exactly this JSON structure:
{{
  "has_errors": true or false,
  "score": integer 0-100,
  "summary": "brief summary string",
  "errors": [
    {{
      "type": "Bug or Security or Performance or BestPractice",
      "severity": "Critical or High or Medium or Low",
      "line": "line number or N/A",
      "description": "what the issue is",
      "fix": "how to fix it"
    }}
  ]
}}

If code has no issues at all, set has_errors to false and errors to empty array.
Do not include any text outside the JSON.

Code to review:
```{language}
{code}
```"""
    result = ai_call(provider, model, [{"role": "user", "content": prompt}], 0.1, 3000)
    result = result.strip()
    if result.startswith("```"):
        result = re.sub(r"^```[a-z]*\n?", "", result)
        result = re.sub(r"\n?```$", "", result)
    return json.loads(result.strip())

def rewrite_code(code, language, provider, model):
    prompt = f"""You are an expert {language} developer. Rewrite the following code to be clean, optimized, secure, and production-ready with proper documentation. Return only the improved code inside a single code block.

```{language}
{code}
```"""
    result = ai_call(provider, model, [{"role": "user", "content": prompt}], 0.2, 4000)
    match = re.search(r"```(?:\w+)?\n([\s\S]+?)\n```", result)
    if match:
        return match.group(1)
    return result

def chat_assistant(messages, provider, model):
    system = {"role": "system", "content": "You are CodeBot, an expert AI assistant for code review, debugging, and programming help. Be concise, helpful, and friendly."}
    return ai_call(provider, model, [system] + messages, 0.7, 1024)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/auth")
def auth():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("auth.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields required"})
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters"})
    ok, msg = create_user(name, email, password)
    return jsonify({"success": ok, "message": msg})

@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    user = verify_user(email, password)
    if user:
        session["user"] = {"name": user["name"], "email": user["email"]}
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid email or password"})

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email", "").strip()
    user = get_user_by_email(email)
    if not user:
        return jsonify({"success": False, "message": "Email not found"})
    otp = generate_otp(email)
    sent = send_email(email, "Your OTP - AI Code Review", f"Your OTP is: {otp}\nValid for 10 minutes.")
    if sent:
        return jsonify({"success": True, "message": "OTP sent to your email"})
    return jsonify({"success": False, "message": "Failed to send email. Check SMTP config in config.py"})

@app.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    data = request.get_json()
    email = data.get("email", "").strip()
    otp = data.get("otp", "").strip()
    if verify_otp(email, otp):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid OTP"})

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email", "").strip()
    new_password = data.get("password", "").strip()
    if len(new_password) < 6:
        return jsonify({"success": False, "message": "Password too short"})
    update_password(email, new_password)
    return jsonify({"success": True, "message": "Password reset successful"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth"))
    return render_template("dashboard.html", user=session["user"],
                           groq_models=GROQ_MODELS, mistral_models=MISTRAL_MODELS)

@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("auth"))
    records = get_history(session["user"]["email"])
    return render_template("history.html", user=session["user"], records=records)

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not authenticated"})
    data = request.get_json()
    code = data.get("code", "").strip()
    language = data.get("language", "python")
    provider = data.get("provider", "groq")
    model = data.get("model", "llama-3.3-70b-versatile")
    if not code:
        return jsonify({"success": False, "message": "No code provided"})
    try:
        result = analyze_code(code, language, provider, model)
        save_history(session["user"]["email"], language, code, result, "")
        return jsonify({"success": True, "data": result})
    except json.JSONDecodeError:
        return jsonify({"success": False, "message": "AI returned invalid response. Try again."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/rewrite", methods=["POST"])
def api_rewrite():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not authenticated"})
    data = request.get_json()
    code = data.get("code", "").strip()
    language = data.get("language", "python")
    provider = data.get("provider", "groq")
    model = data.get("model", "llama-3.3-70b-versatile")
    if not code:
        return jsonify({"success": False, "message": "Code required"})
    try:
        rewritten = rewrite_code(code, language, provider, model)
        from database import history_col
        history_col.update_one(
            {"user_email": session["user"]["email"]},
            {"$set": {"rewritten_code": rewritten}}
        )
        return jsonify({"success": True, "data": rewritten})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    messages = data.get("messages", [])
    provider = data.get("provider", "groq")
    model = "llama-3.3-70b-versatile" if provider == "groq" else "mistral-large-latest"

    try:
        if provider == "mistral":
            import requests as req
            system = {"role": "system", "content": "You are CodeBot, an expert AI assistant for code review, debugging, and programming help. Be concise, helpful, and friendly."}
            resp = req.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"},
                json={"model": model, "messages": [system] + messages, "temperature": 0.7, "max_tokens": 1024},
                timeout=60
            )
            resp.raise_for_status()
            reply = resp.json()["choices"][0]["message"]["content"]
        else:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            system = {"role": "system", "content": "You are CodeBot, an expert AI assistant for code review, debugging, and programming help. Be concise, helpful, and friendly."}
            response = client.chat.completions.create(
                model=model,
                messages=[system] + messages,
                temperature=0.7,
                max_tokens=1024
            )
            reply = response.choices[0].message.content

        return jsonify({"success": True, "reply": reply})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
@app.route("/api/send-history-email", methods=["POST"])
def send_history_email():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not authenticated"})
    data = request.get_json()
    record_id = data.get("record_id")
    to_email = data.get("to_email", "").strip()
    if not to_email:
        return jsonify({"success": False, "message": "Please provide an email address"})
    record = get_history_by_id(record_id)
    if not record:
        return jsonify({"success": False, "message": "Record not found"})
    review_data = record.get("review_data", {})
    if isinstance(review_data, str):
        try:
            review_data = json.loads(review_data)
        except:
            review_data = {}
    body = f"""AI Code Review Report
=====================
Date: {record.get('created_at', 'N/A')}
Language: {record.get('language', 'N/A').upper()}
Score: {review_data.get('score', 'N/A')}/100

SUMMARY:
{review_data.get('summary', 'N/A')}

ORIGINAL CODE:
{'-'*40}
{record.get('original_code', '')}

ISSUES FOUND ({len(review_data.get('errors', []))} total):
{'-'*40}
"""
    for i, err in enumerate(review_data.get('errors', []), 1):
        body += f"\n{i}. [{err.get('severity','N/A')}] {err.get('type','Issue')} — Line {err.get('line','N/A')}\n"
        body += f"   Issue: {err.get('description','')}\n"
        body += f"   Fix:   {err.get('fix','')}\n"
    if record.get('rewritten_code'):
        body += f"\n\nREWRITTEN CODE:\n{'-'*40}\n{record['rewritten_code']}"
    body += f"\n\n{'='*40}\nGenerated by AI Code Review Agent"
    sent = send_email(to_email, f"Code Review Report — {record.get('language','').upper()}", body)
    if sent:
        return jsonify({"success": True, "message": f"Report sent to {to_email}"})
    return jsonify({"success": False, "message": "Failed to send. Check SMTP credentials in config.py"})

@app.route("/api/delete-history", methods=["POST"])
def api_delete_history():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not authenticated"})
    data = request.get_json()
    record_id = data.get("record_id")
    if not record_id:
        return jsonify({"success": False, "message": "No record ID provided"})
    deleted = delete_history_by_id(record_id, session["user"]["email"])
    if deleted:
        return jsonify({"success": True, "message": "Record deleted"})
    return jsonify({"success": False, "message": "Record not found or not authorized"})

@app.route("/api/delete-all-history", methods=["POST"])
def api_delete_all_history():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not authenticated"})
    count = delete_all_history(session["user"]["email"])
    return jsonify({"success": True, "message": f"Deleted {count} records"})

@app.route("/preview")
def preview():
    code = request.args.get("code", "")
    language = request.args.get("language", "html")
    if language == "html":
        return code
    return f"""<!DOCTYPE html><html>
    <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script></head><body style="background:#0d1117;margin:0;padding:20px"><pre>
    <code class="language-{language}" id="code">
    </code></pre><script>document.getElementById('code').textContent={json.dumps(code)};hljs.highlightAll();
    </script>
    </body>
    </html>"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)