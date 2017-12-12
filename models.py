import datetime

import peewee
import playhouse.shortcuts

db = peewee.SqliteDatabase('journalapp.db')


class Base(peewee.Model):

    def to_dict(self):
        return playhouse.shortcuts.model_to_dict(self)

    class Meta:
        database = db


class Entry(Base):
    time = peewee.DateTimeField(default=datetime.datetime.now)
    text = peewee.BlobField()
    # Watson Tone Analyzer
    tone_analysis = peewee.BlobField()
    # Watson Natural Language Understanding
    nlu_analysis = peewee.BlobField()
    type = peewee.TextField()


db.create_tables([Entry], safe=True)
