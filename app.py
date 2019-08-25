#!/usr/bin/env python3

import datetime
import json
from flask import Flask, render_template
from models import Result

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

    print(labels)
    return render_template('index.html', labels=json.dumps(labels), downloads=json.dumps(downloads), uploads=json.dumps(uploads), pings=json.dumps(pings))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
