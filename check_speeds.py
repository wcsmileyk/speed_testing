import datetime
import speedtest
from peewee import IntegrityError

from models import Result, Server

st = speedtest.Speedtest()

results = []

for i in range(5):
    st.get_best_server()
    threads = 1
    st.download(threads=threads)
    st.upload(threads=threads)

    result = st.results.dict()
    result['timestamp'] = datetime.datetime.now()
    results.append(result)

for result in results:
    server_details = result['server']
    server_id = server_details['id']

    server_query = Server.select().where(Server.st_id == server_id)
    if len(server_query) == 0:
        server_params = {'st_id': server_id,
                         'name': server_details['name'],
                         'sponsor': server_details.get('sponsor'),
                         'url': server_details.get('url'),
                         'url1': server_details.get('url2'),
                         'cc': server_details.get('cc'),
                         'host': server_details.get('host'),
                         'lat': server_details.get('lat'),
                         'lon': server_details.get('lon')}

        server = Server.create(**server_params)
        server.save()
    else:
        server = server_query[0]

    r_params = {'server': server,
                'timestamp': result['timestamp'],
                'download_spd': result.get('download'),
                'upload_spd': result.get('upload'),
                'bytes_sent': result.get('bytes_sent'),
                'bytes_rec': result.get('bytes_received'),
                'latency': result['ping'],
                'client': result['client'].get('ip')}

    r = Result(**r_params)
    r.save()
