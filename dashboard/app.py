from flask import Flask, render_template, jsonify
import os, json

app = Flask(__name__)

REPORTS_FOLDER = os.path.join(os.getcwd(), 'reports')
os.makedirs(REPORTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = [f for f in os.listdir(REPORTS_FOLDER) if f.lower().endswith('.json')]
    files.sort(reverse=True)
    return render_template('index.html', reports=files)

@app.route('/report/<name>')
def report_json(name):
    # name already includes ".json"
    path = os.path.join(REPORTS_FOLDER, name)
    if not os.path.exists(path):
        return jsonify({'error': 'Fichier non trouvé'}), 404
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
