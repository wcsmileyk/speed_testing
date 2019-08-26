import datetime
import json
from dateutil import parser
from flask import Flask, render_template, jsonify, request
from models import Result, Server

app = Flask(__name__)
app.config['SECRET_KEY'] = 'averylongbigstupidsecretkeythingamajigblopideeedooo'


def get_results(days=5):
    now = datetime.datetime.now()
    days_back = now - datetime.timedelta(days)
    results = Result.select().filter(Result.timestamp >= days_back)
    return results


@app.route('/')
def hello_world():
    test_results = get_results()
    labels = []
    downloads = []
    uploads = []
    pings = []

    for test in test_results:
        labels.append(test.timestamp.strftime("%d %H:%M:%S"))
        downloads.append(test.download_spd / 1000000)
        uploads.append(test.upload_spd / 1000000)
        pings.append(test.latency)

    return render_template('index.html', labels=json.dumps(labels), downloads=json.dumps(downloads), uploads=json.dumps(uploads), pings=json.dumps(pings))


@app.route('/api/servers', methods=['GET'])
def server_api():
    result = {'success': True, 'data': [server.to_json() for server in Server.select()]}
    return jsonify(result)


@app.route('/api/results')
def results_api():
    from_date = check_date(request.args.get('from_date'), 30)
    to_date = check_date(request.args.get('to_date'), 0)

    results = Result.select().where((Result.timestamp >= from_date) & (Result.timestamp <= to_date))
    return jsonify({'success': True, 'data': [result.to_json() for result in results]})


def check_date(date_string, td):
    try:
        return parser.parse(date_string)
    except (ValueError, TypeError):
        return datetime.datetime.now() - datetime.timedelta(td)


if __name__ == '__main__':
    app.run()
