from peewee import *

db = SqliteDatabase('speed_testing.db')


class BaseModel(Model):
    class Meta:
        database = db


class Server(BaseModel):
    st_id = PrimaryKeyField(null=False)
    name = CharField()
    sponsor = CharField()
    url = CharField()
    url1 = CharField(null=True)
    cc = CharField(max_length=2)
    host = CharField()
    lat = CharField()
    lon = CharField()


class Result(BaseModel):
    timestamp = DateTimeField(null=False)
    download_spd = FloatField()
    upload_spd = FloatField()
    bytes_sent = IntegerField()
    bytes_rec = IntegerField()
    latency = FloatField()
    client = CharField(max_length=16)
    server = ForeignKeyField(Server, related_name='server_results')




