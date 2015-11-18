# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from google.storage.speckle.proto.jdbc_type import NULL


class Utilisateur(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    adresse = ndb.StringProperty(required=True)
    nom = ndb.StringProperty(required=True)
    prenom = ndb.StringProperty(required=True)

class Offre(ndb.Model):
    titre = ndb.StringProperty(required=True)
    point_depart = ndb.StringProperty(required=True)
    point_arrive = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    heure = ndb.StringProperty(required=True)
    nb_place = ndb.StringProperty(required=True)
    id_utilisateur = ndb.StringProperty(required=True)

class Demande(ndb.Model):
    point_depart = ndb.StringProperty(required=True)
    point_arrive = ndb.StringProperty(required=True)
    date = ndb.StringProperty(required=True)
    heure = ndb.StringProperty(required=True)
    id_utilisateur = ndb.StringProperty(required=True)