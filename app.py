from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, abort
import json
import os
from rembg import remove
from PIL import Image
import io
import requests
import qrcode

app = Flask(__name__)

# Helper functions for JSON data handling
def load_json(file_name):
    file_path = os.path.join("data", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return []

def save_json(file_name, data):
    file_path = os.path.join("data", file_name)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Routes for loading JSON data
def load_services():
    return load_json('services.json')

# Function to load projects from JSON
def load_projects():
    try:
        with open('data/projects.json', 'r') as file:
            projects = json.load(file)
            return projects
    except Exception as e:
        print(f"Error loading projects: {e}")
        return []

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Services route
@app.route('/services')
def services():
    services = load_services()
    return render_template('services.html', services=services)


@app.route('/projects')
def projects():
    selected_category = request.args.get('category', 'All')
    all_projects = load_projects()
    categories = {project.get('category', 'Uncategorized') for project in all_projects}

    if selected_category != 'All':
        filtered_projects = [project for project in all_projects if project.get('category') == selected_category]
    else:
        filtered_projects = all_projects

    return render_template('projects.html', projects=filtered_projects, categories=categories, selected_category=selected_category)


@app.route('/projects/<int:project_id>')
def project_detail(project_id):
    projects = load_projects()
    project = next((proj for proj in projects if proj['id'] == project_id), None)
    similar_projects = [p for p in projects if p['id'] != project_id][:3]  # Get a few similar projects

    if project is None:
        return "Project not found", 404

    return render_template('project_detail.html', project=project, similar_projects=similar_projects)


# Report a Bug route
@app.route('/report-bug', methods=["GET", "POST"])
def report_bug():
    if request.method == "POST":
        bug_report = request.form.to_dict()
        bug_reports = load_json("bug_reports.json")
        bug_reports.append(bug_report)
        save_json("bug_reports.json", bug_reports)
        return jsonify({"status": "Bug reported successfully"})
    return render_template('report_bug.html')

@app.route('/services/background-remover', methods=['GET', 'POST'])
def background_remover():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        img = Image.open(file.stream)
        output = remove(img)  # Perform background removal

        # Save output to a buffer to send as a file
        output_io = io.BytesIO()
        output.save(output_io, format='PNG')
        output_io.seek(0)

        return send_file(output_io, mimetype='image/png', as_attachment=True, download_name='no_background.png')

    return render_template('background_remover.html')

# Weather Station route
@app.route('/services/weather-station', methods=['GET', 'POST'])
def weather_station():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        api_key = 'YOUR_API_KEY'  # Replace with your actual API key
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
        else:
            flash("City not found. Please try again.")
    return render_template('weather_station.html', weather_data=weather_data)

@app.route('/services/grammar-analyzer', methods=['GET', 'POST'])
def grammar_analyzer():
    corrected_text = None
    if request.method == 'POST':
        text = request.form.get('text')
        api_url = 'https://api.languagetoolplus.com/v2/check'
        payload = {
            'text': text,
            'language': 'en-US'
        }
        response = requests.post(api_url, data=payload)
        result = response.json()

        # Apply corrections
        for match in result['matches']:
            offset = match['offset']
            length = match['length']
            replacement = match['replacements'][0]['value'] if match['replacements'] else ""
            text = text[:offset] + replacement + text[offset + length:]

        corrected_text = text

    return render_template('grammar_analyzer.html', corrected_text=corrected_text)

# QR Code Generator route
@app.route('/services/qr-code-generator', methods=['GET', 'POST'])
def qr_code_generator():
    if request.method == 'POST':
        data = request.form.get('data')
        qr = qrcode.make(data)
        qr_io = io.BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)
        return send_file(qr_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    return render_template('qr_code_generator.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host=0,0,0,0, port=5000)
