from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import csv
from datetime import datetime
import os
import subprocess
import threading
import queue
import re
import signal
import sys

app = Flask(__name__)
CORS(app)

PATH = 'all excels/'

# ━━━━━━━━━━━━━━━━━━━  BOT MANAGEMENT ━━━━━━━━━━━━━━━━━━━
bot_processes = {}
linkedin_config_path = os.path.join(os.path.dirname(__file__), "config", "search.py")

def enqueue_output(out, q):
    try:
        for line in iter(out.readline, b''):
            decoded = line.decode('utf-8', errors='replace').strip()
            if decoded:
                q.put(decoded)
    except Exception:
        pass
    finally:
        out.close()
        q.put("STREAM_DONE")


# ━━━━━━━━━━━━━━━━━━━  ROUTES ━━━━━━━━━━━━━━━━━━━
@app.route('/')
def home():
    """Displays the home page of the application."""
    return render_template('index.html')

@app.route('/applied-jobs', methods=['GET'])
def get_applied_jobs():
    try:
        jobs = []
        with open(PATH + 'all_applied_applications_history.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                jobs.append({
                    'Job_ID': row['Job ID'],
                    'Title': row['Title'],
                    'Company': row['Company'],
                    'HR_Name': row['HR Name'],
                    'HR_Link': row['HR Link'],
                    'Job_Link': row['Job Link'],
                    'External_Job_link': row['External Job link'],
                    'Date_Applied': row['Date Applied']
                })
        return jsonify(jobs)
    except FileNotFoundError:
        return jsonify({"error": "No applications history found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/applied-jobs/<job_id>', methods=['PUT'])
def update_applied_date(job_id):
    try:
        data = []
        csvPath = PATH + 'all_applied_applications_history.csv'
        
        if not os.path.exists(csvPath):
            return jsonify({"error": f"CSV file not found at {csvPath}"}), 404
            
        with open(csvPath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldNames = reader.fieldnames
            found = False
            for row in reader:
                if row['Job ID'] == job_id:
                    row['Date Applied'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    found = True
                data.append(row)
        
        if not found:
            return jsonify({"error": f"Job ID {job_id} not found"}), 404

        with open(csvPath, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            writer.writeheader()
            writer.writerows(data)
        
        return jsonify({"message": "Date Applied updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ━━━━━━━━━━━━━━━━━━━  API CONFIG ━━━━━━━━━━━━━━━━━━━
personals_path = os.path.join(os.path.dirname(__file__), "config", "personals.py")
questions_path = os.path.join(os.path.dirname(__file__), "config", "questions.py")
secrets_path = os.path.join(os.path.dirname(__file__), "config", "secrets.py")

def parse_python_list(content, var_name):
    match = re.search(rf"^{var_name}\s*=\s*\[(.*?)\]", content, re.MULTILINE | re.DOTALL)
    if not match: return []
    items = re.findall(r"['\"]([^'\"]*)['\"]", match.group(1))
    return [i.strip() for i in items if i.strip()]

def update_python_list(content, var_name, new_list):
    formatted = ",\n    ".join([f"'{item}'" for item in new_list])
    new_block = f"{var_name} = [\n    {formatted}\n]" if new_list else f"{var_name} = []"
    return re.sub(rf"^{var_name}\s*=\s*\[.*?\]", new_block, content, flags=re.MULTILINE | re.DOTALL)

def extract_str(content, var):
    m = re.search(rf"^{var}\s*=\s*['\"]([^'\"]*)['\"]", content, re.MULTILINE)
    return m.group(1) if m else ""

def update_str(content, var, val):
    safe_val = str(val).replace("'", "\\'")
    if re.search(rf"^{var}\s*=\s*['\"].*?['\"]", content, re.MULTILINE):
        return re.sub(rf"^{var}\s*=\s*['\"].*?['\"]", f"{var} = '{safe_val}'", content, flags=re.MULTILINE)
    return content

def extract_int(content, var):
    m = re.search(rf"^{var}\s*=\s*(\d+)", content, re.MULTILINE)
    return int(m.group(1)) if m else 0

def update_int(content, var, val):
    if re.search(rf"^{var}\s*=\s*\d+", content, re.MULTILINE):
        return re.sub(rf"^{var}\s*=\s*\d+", f"{var} = {int(val)}", content, flags=re.MULTILINE)
    return content

def parse_dict_skill(content, var_name):
    match = re.search(rf"^{var_name}\s*=\s*\{{(.*?)\}}", content, re.MULTILINE | re.DOTALL)
    if not match: return {}
    d = {}
    block = match.group(1)
    block = re.sub(r'#[^\n]*', '', block)  # strip comment lines
    for line in block.split(','):
        if ':' in line:
            k, v = line.split(':', 1)
            k = k.strip().strip("'\"")
            v = int(float(re.sub(r'[^\d.]', '', v.strip() or '0')))
            if k: d[k] = v
    return d

def update_dict_skill(content, var_name, d):
    formatted = ",\n    ".join([f"\"{k}\": {v}" for k, v in d.items()])
    new_block = f"{var_name} = {{\n    {formatted}\n}}" if d else f"{var_name} = {{}}"
    if re.search(rf"^{var_name}\s*=\s*\{{.*?\}}", content, re.MULTILINE | re.DOTALL):
        return re.sub(rf"^{var_name}\s*=\s*\{{.*?\}}", new_block, content, flags=re.MULTILINE | re.DOTALL)
    return content

@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    if not os.path.exists(linkedin_config_path):
        return jsonify({"error": "Config files not found"}), 404

    with open(linkedin_config_path, "r", encoding="utf-8") as f: c_search = f.read()
    with open(personals_path, "r", encoding="utf-8") as f: c_personals = f.read()
    with open(questions_path, "r", encoding="utf-8") as f: c_questions = f.read()
    with open(secrets_path, "r", encoding="utf-8") as f: c_secrets = f.read()

    if request.method == "GET":
        data = {
            "search_terms": parse_python_list(c_search, "search_terms"),
            "search_location": extract_str(c_search, "search_location"),
            "experience_level": parse_python_list(c_search, "experience_level"),
            "job_type": parse_python_list(c_search, "job_type"),
            "on_site": parse_python_list(c_search, "on_site"),
            "companies": parse_python_list(c_search, "companies"),
            "sort_by": extract_str(c_search, "sort_by"),
            "date_posted": extract_str(c_search, "date_posted"),
            "easy_apply_only": False,
            
            "first_name": extract_str(c_personals, "first_name"),
            "last_name": extract_str(c_personals, "last_name"),
            "phone_number": extract_str(c_personals, "phone_number"),
            
            "desired_salary": extract_int(c_questions, "desired_salary"),
            "current_ctc": extract_int(c_questions, "current_ctc"),
            "notice_period": extract_int(c_questions, "notice_period"),
            "linkedin_url": extract_str(c_questions, "linkedIn"),
            "years_of_experience": extract_str(c_questions, "years_of_experience"),
            "skills": parse_dict_skill(c_questions, "skill_experience"),
        }

        easy_auto = re.search(r"^easy_apply_only\s*=\s*(True|False)", c_search, re.MULTILINE)
        if easy_auto: data["easy_apply_only"] = (easy_auto.group(1) == "True")

        return jsonify(data)

    elif request.method == "POST":
        payload = request.json
        
        c_search = update_python_list(c_search, "search_terms", payload.get("search_terms", []))
        c_search = update_python_list(c_search, "experience_level", payload.get("experience_level", []))
        c_search = update_python_list(c_search, "job_type", payload.get("job_type", []))
        c_search = update_python_list(c_search, "on_site", payload.get("on_site", []))
        c_search = update_python_list(c_search, "companies", payload.get("companies", []))
        c_search = update_str(c_search, "search_location", payload.get("search_location", ""))
        c_search = update_str(c_search, "sort_by", payload.get("sort_by", ""))
        c_search = update_str(c_search, "date_posted", payload.get("date_posted", ""))
        is_easy = "True" if payload.get("easy_apply_only") else "False"
        c_search = re.sub(r"^easy_apply_only\s*=\s*(True|False)", f"easy_apply_only = {is_easy}", c_search, flags=re.MULTILINE)
        
        c_personals = update_str(c_personals, "first_name", payload.get("first_name", ""))
        c_personals = update_str(c_personals, "last_name", payload.get("last_name", ""))
        c_personals = update_str(c_personals, "phone_number", payload.get("phone_number", ""))
        
        c_questions = update_int(c_questions, "desired_salary", payload.get("desired_salary", 0))
        c_questions = update_int(c_questions, "current_ctc", payload.get("current_ctc", 0))
        c_questions = update_int(c_questions, "notice_period", payload.get("notice_period", 0))
        c_questions = update_str(c_questions, "linkedIn", payload.get("linkedin_url", ""))
        c_questions = update_str(c_questions, "years_of_experience", payload.get("years_of_experience", "0"))
        c_questions = update_dict_skill(c_questions, "skill_experience", payload.get("skills", {}))

        with open(linkedin_config_path, "w", encoding="utf-8") as f: f.write(c_search)
        with open(personals_path, "w", encoding="utf-8") as f: f.write(c_personals)
        with open(questions_path, "w", encoding="utf-8") as f: f.write(c_questions)
        with open(secrets_path, "w", encoding="utf-8") as f: f.write(c_secrets)

        return jsonify({"status": "success"})


@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        resumes_dir = os.path.join(os.path.dirname(__file__), "all resumes")
        os.makedirs(resumes_dir, exist_ok=True)
        filepath = os.path.join(resumes_dir, "resume.pdf") 
        try:
            file.save(filepath)
            return jsonify({"status": "success", "message": "Resume uploaded successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# ━━━━━━━━━━━━━━━━━━━  API EXECUTION ━━━━━━━━━━━━━━━━━━━

@app.route("/api/start", methods=["POST"])
def start_bot():
    if bot_processes.get("linkedin") and bot_processes["linkedin"].poll() is None:
        return jsonify({"status": "already_running"})

    try:
        payload = request.get_json(silent=True) or {}
        max_jobs = payload.get("max_jobs", 0)
        
        # Write max_number_of_jobs_run to search.py
        if os.path.exists(linkedin_config_path):
            with open(linkedin_config_path, "r", encoding="utf-8") as f: c_search = f.read()
            if re.search(r"^max_number_of_jobs_run\s*=\s*\d+", c_search, re.MULTILINE):
                c_search = re.sub(r"^max_number_of_jobs_run\s*=\s*\d+", f"max_number_of_jobs_run = {int(max_jobs)}", c_search, flags=re.MULTILINE)
            else:
                c_search += f"\n# Added by UI\nmax_number_of_jobs_run = {int(max_jobs)}\n"
            with open(linkedin_config_path, "w", encoding="utf-8") as f: f.write(c_search)

        script_path = os.path.join(os.path.dirname(__file__), "runAiBot.py")
        venv_python = sys.executable 
        proc = subprocess.Popen(
            [venv_python, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(__file__),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        
        q = queue.Queue()
        t = threading.Thread(target=enqueue_output, args=(proc.stdout, q))
        t.daemon = True
        t.start()
        
        bot_processes["linkedin"] = proc
        bot_processes["queue"] = q
        
        return jsonify({"status": "started", "pid": proc.pid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stop", methods=["POST"])
def stop_bot():
    proc = bot_processes.get("linkedin")
    if proc and proc.poll() is None:
        try:
            os.kill(proc.pid, signal.CTRL_C_EVENT)
            proc.wait(timeout=5)
        except Exception:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except:
                pass
        
        if bot_processes.get("queue"):
            bot_processes["queue"].put("STREAM_DONE")
            
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not_running"})


@app.route("/api/logs")
def stream_logs():
    def generate():
        q = bot_processes.get("queue")
        if not q:
            return
        
        while True:
            try:
                msg = q.get(timeout=1.0)
                if msg == "STREAM_DONE":
                    yield "event: message\ndata: STREAM_DONE\n\n"
                    break
                yield f"data: {msg}\n\n"
            except queue.Empty:
                yield ": heartbeat\n\n"
                
                # if process died without sending STREAM_DONE
                proc = bot_processes.get("linkedin")
                if proc and proc.poll() is not None:
                    yield "event: message\ndata: STREAM_DONE\n\n"
                    break

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, port=5000)