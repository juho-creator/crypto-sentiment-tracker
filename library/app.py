from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    limit = request.form.get('number', 10)
    url = f"https://api.alternative.me/fng/?limit={limit}"
    response = requests.get(url)
    data = response.json()['data']

    for entry in data:
        timestamp = int(entry['timestamp'])
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        entry['date'] = date

    average = calculate_average(data)

    return render_template('index.html', data=data, average=average)

def calculate_average(data):
    total_value = 0
    for entry in data:
        total_value += int(entry['value'])
    return round(total_value / len(data), 2) if data else 0

if __name__ == '__main__':
    app.run(debug=True)
