from google.appengine.ext import ndb
from google.storage.speckle.proto.jdbc_type import NULL

class Utilisateur(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    adresse = ndb.StringProperty(required=True)
    