# -*- coding: utf-8 -*-

import webapp2
import logging
import traceback
import datetime
import json

from google.appengine.ext import ndb
from google.appengine.ext import db

# Importation des modèles de données personnalisés.
from models import Actor, Address, Category, Customer, City, Country, Film, Language, FilmActor
from google.storage.speckle.proto.jdbc_type import NULL


def serialiser_pour_json(objet):
    """ Permet de sérialiser les dates et heures pour transformer
        un objet en JSON.

        Args:
            objet (obj): L'objet à sérialiser.

        Returns:
            obj : Si c'est une date et heure, retourne une version sérialisée
                  selon le format ISO (str); autrement, retourne l'objet
                  original non modifié.
        """
    if isinstance(objet, datetime.datetime):
        # Pour une date et heure, on retourne une chaîne
        # au format ISO (sans les millisecondes).
        return objet.replace(microsecond=0).isoformat()
    elif isinstance(objet, datetime.date):
        # Pour une date, on retourne une chaîne au format ISO.
        return objet.isoformat()
    else:
        # Pour les autres types, on retourne l'objet tel quel.
        return objet


class MainPageHandler(webapp2.RequestHandler):

    def get(self):
        # Permet de vérifier si le service Web est en fonction.
        # On pourrait utiliser cette page pour afficher de l'information
        # (au format HTML) sur le service Web REST.
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.response.out.write('TP2 "Service Web avec' +
                                'Google App Engine, Steve Bérubé et Rémy Huot')


class ChargementHandler(webapp2.RequestHandler):

    def get(self):
        ndb.delete_multi(Actor.query().fetch(keys_only=True))
        ndb.delete_multi(FilmActor.query().fetch(keys_only=True))
        ndb.delete_multi(Film.query().fetch(keys_only=True))
        ndb.delete_multi(Language.query().fetch(keys_only=True))
        ndb.delete_multi(City.query().fetch(keys_only=True))
        ndb.delete_multi(Customer.query().fetch(keys_only=True))
        ndb.delete_multi(Address.query().fetch(keys_only=True))
        ndb.delete_multi(Country.query().fetch(keys_only=True))
        ndb.delete_multi(Category.query().fetch(keys_only=True))

        with open('Actor.json') as json_data:
            actor_dict_in = json.loads(json_data.read())

            for lActeur in actor_dict_in:
                cle = ndb.Key('Actor', int(lActeur['actor_id']))
                unActeur = Actor(key=cle)
                unActeur.first_name = lActeur['first_name']
                unActeur.last_name = lActeur['last_name']

                unActeur.put()
            json_data.close()

        with open('filmactor.json') as actorfilm_data:
            filmActor_dict_in = json.loads(actorfilm_data.read())

            for leFilmActor in filmActor_dict_in:
                unFilmActor = FilmActor()
                unFilmActor.actor_id = leFilmActor['actor_id']
                unFilmActor.film_id = leFilmActor['film_id']

                unFilmActor.put()
            actorfilm_data.close()

        with open('Film.json') as json_data:
            film_dict_in = json.loads(json_data.read())
            with open('filmactor.json') as filmactor_data:
                film_actor_dict_in = json.loads(filmactor_data.read())
            with open('FilmCategory.json') as filmCategory_data:
                film_category_dict_in = json.loads(filmCategory_data.read())
                for leFilm in film_dict_in:
                    unFilm = Film()
                    unFilm.title = leFilm['title']
                    unFilm.description = leFilm['description']
                    unFilm.release_year = int(leFilm['release_year'])
                    unFilm.language_id = int(leFilm['language_id'])
                    if leFilm['original_language_id'] is not None:
                        unFilm.original_language_id = int(leFilm['original_language_id'])
                    for unActor in film_actor_dict_in:
                        if unActor['film_id'] == int(leFilm['film_id']):
                            unFilm.list_actor.append(int(unActor['actor_id']))
                    for uneCategory in film_category_dict_in:
                        if int(uneCategory['film_id']) == int(leFilm['film_id']):
                            unFilm.category_id = int(uneCategory['category_id'])
                    unFilm.rental_duration = int(leFilm['rental_duration'])
                    unFilm.rental_rate = float(leFilm['rental_rate'])
                    unFilm.length = int(leFilm['length'])
                    unFilm.replacement_cost = float(leFilm['replacement_cost'])
                    unFilm.rating = leFilm['rating']
                    unFilm.special_features = leFilm['special_features']

                    unFilm.put()
            json_data.close()

        with open('Language.json') as json_data:
            language_dict_in = json.loads(json_data.read())

            for leLangage in language_dict_in:
                cle = ndb.Key('Language', int(leLangage['language_id']))
                unLanguage = Language(key=cle)
                unLanguage.name = leLangage['name']
                unLanguage.name_fr = leLangage['name_fr']

                unLanguage.put()
            json_data.close()

        with open('Customer.json') as json_data_client:
            customer_dict_in = json.loads(json_data_client.read())

            for leClient in customer_dict_in:
                cle = ndb.Key('Customer', int(leClient['customer_id']))
                unCustomer = Customer(key=cle)
                unCustomer.store_id = int(leClient['store_id'])
                unCustomer.first_name = leClient['first_name']
                unCustomer.last_name = leClient['last_name']
                unCustomer.email = leClient['email']
                unCustomer.address_id = int(leClient['address_id'])
                unCustomer.active = int(leClient['active'])
                unCustomer.password = leClient['password']

                unCustomer.put()
                with open('Address.json') as json_data_address:
                    address_dict_in = json.loads(json_data_address.read())
                for lAddresse in address_dict_in:
                    if unCustomer.address_id == int(lAddresse['address_id']):
                        uneAddresse = Address(parent=cle)
                        uneAddresse.address = lAddresse['address']
                        uneAddresse.address2 = lAddresse['address2']
                        uneAddresse.district = lAddresse['district']
                        uneAddresse.city_id = int(lAddresse['city_id'])
                        uneAddresse.postal_code = lAddresse['postal_code']
                        uneAddresse.phone = lAddresse['phone']

                        uneAddresse.put()
                json_data_address.close()
            json_data_client.close()

        with open('Country.json') as json_data:
            country_dict_in = json.loads(json_data.read())

            for leCountry in country_dict_in:
                cle_country = ndb.Key('Country', int(leCountry['country_id']))
                uneCountry = Country(key=cle_country)
                uneCountry.country = leCountry['country']

                uneCountry.put()
            json_data.close()

        with open('Category.json') as json_data:
            category_dict_in = json.loads(json_data.read())

            for laCategory in category_dict_in:
                cle_category = ndb.Key('Category', int(laCategory['category_id']))
                uneCategory = Category(key=cle_category)
                uneCategory.name = laCategory['name']
                uneCategory.name_fr = laCategory['name_fr']

                uneCategory.put()
            json_data.close()

        with open('City.json') as json_data:
            city_dict_in = json.loads(json_data.read())

            for leCity in city_dict_in:
                cle_city = ndb.Key('City', int(leCity['city_id']))
                unCity = City(key=cle_city)
                unCity.city = leCity['city']
                unCity.country_id = int(leCity['country_id'])

                unCity.put()
            json_data.close()
        self.response.set_status(201)
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.response.out.write('Le Chargement a été effectué avec succès!')


class FilmHandler(webapp2.RequestHandler):

    # ajout d'un film

    def post(self):
        try:
            film = Film()

            film_dict_in = json.loads(self.request.body)

            film.title = film_dict_in['title']
            film.description = film_dict_in['description']
            film.release_year = film_dict_in['release_year']
            film.language_id = film_dict_in['language_id']
            film.original_language_id = film_dict_in['original_language_id']
            film.rental_duration = film_dict_in['rental_duration']
            film.rental_rate = film_dict_in['rental_rate']
            film.length = film_dict_in['length']
            film.replacement_cost = film_dict_in['replacement_cost']
            film.rating = film_dict_in['rating']
            film.special_features = film_dict_in['special_features']

            film.put()

            self.response.set_status(201)

            film_dict = film.to_dict()
            film_dict['idFilm'] = film.key.id()
            film_json = json.dumps(film_dict, default=serialiser_pour_json)
            self.response.headers['Content-Type'] = ('application/json;' +
                                                     ' charset=utf-8')
            self.response.out.write(film_json)

        except (db.BadValueError, ValueError, KeyError):
            logging.error('%s', traceback.format_exc())
            self.error(400)

        except Exception:
            logging.error('%s', traceback.format_exc())
            self.error(500)

    # recherche d'un film

    def get(self, idFilm=None):
        try:
            if idFilm is not None:
                cle = ndb.Key('Film', long(idFilm))
                film = cle.get()
                if (film is None):
                    self.error(404)
                    return
                film_dict = film.to_dict()
                film_dict['idFilm'] = film.key.id()
                if (film_dict['language_id'] is not None):
                    cle_language = ndb.Key('Language', int(film_dict['language_id']))
                    language = cle_language.get()
                    film_dict['language'] = language.name
                if (film_dict['original_language_id'] is not None):
                    cle_or_language = ndb.Key('Language', int(film_dict['original_language_id']))
                    or_language = cle_or_language.get()
                    film_dict['original_language'] = or_language.name

                film_final_dict = dict()

                film_final_dict['ID'] = film_dict['idFilm']
                film_final_dict['Title'] = film_dict['title']
                film_final_dict['Description'] = film_dict['description']
                film_final_dict['Language'] = film_dict['language']
                if (film_dict['original_language_id'] is not None):
                    film_final_dict['Original Language'] = film_dict['original_language']
                # if (film_dict['category_id'] is not None):
                    # film_final_dict['Category'] = film_dict['category']
                film_final_dict['Length'] = film_dict['length']
                film_final_dict['Rating'] = film_dict['rating']
                film_final_dict['Release Year'] = film_dict['release_year']
                film_final_dict['Rental Duration'] = film_dict['rental_duration']
                film_final_dict['Rental Rate'] = film_dict['rental_rate']
                film_final_dict['Special Features'] = film_dict['special_features']
                film_final_dict['List Actors'] = film_dict['list_actor']

                json_data = json.dumps(film_final_dict, default=serialiser_pour_json)
            else:
                list_film = []

                #requete = Film.query().order(Film.title)
                requete = Film.query()

                classification = self.request.get('classification')
                if (classification != ''):
                    requete = requete.filter(Film.rating ==
                                             str(classification))
                duree_min = self.request.get('duree-min')
                if (duree_min != ''):
                    requete = requete.filter(Film.length >= int(duree_min))
                duree_max = self.request.get('duree-max')
                if (duree_max != ''):
                    requete = requete.filter(Film.length <= int(duree_max))

                mots_cle = self.request.get('mots-cle')
                if (mots_cle != ''):
                    for unFilm in requete:
                        # join du mot cle
                        strVide = ''
                        motcle = strVide.join(mots_cle.split(' ')).lower()
                        titre = strVide.join(unFilm.title.split(' ')).lower()
                        if motcle in titre:
                            list_film.append(unFilm)
                else:
                    list_film = requete

                list_films_final = []

                cpt = 1
                for film in list_film:
                    if (cpt <= 20):
                        film_dict = film.to_dict()
                        film_dict['idFilm'] = long(film.key.id())

                        if (film_dict['language_id'] is not None):
                            cle_language = ndb.Key('Language', int(film_dict['language_id']))
                            language = cle_language.get()
                            film_dict['language'] = language.name

                        if (film_dict['original_language_id'] is not None):
                            cle_original_language = ndb.Key('Language', int(film_dict['original_language_id']))
                            original_language = cle_original_language.get()
                            film_dict['original_language'] = original_language.name

                            # ce code marche pas...
                        ''' if (film_dict['category_id'] is not None):
                            cle_category = ndb.Key('Category', int(film_dict['category_id']))
                            category = cle_category.get()
                            film_dict['category'] = category.category_name''' 

                        film_final_dict = dict()
                        film_final_dict['ID'] = film_dict['idFilm']
                        film_final_dict['Title'] = film_dict['title']
                        film_final_dict['Description'] = film_dict['description']
                        film_final_dict['Language'] = film_dict['language']
                        if (film_dict['original_language_id'] is not None):
                            film_final_dict['Original Language'] = film_dict['original_language']
                        # if (film_dict['category_id'] is not None):
                            # film_final_dict['Category'] = film_dict['category']
                        film_final_dict['Length'] = film_dict['length']
                        film_final_dict['Rating'] = film_dict['rating']
                        film_final_dict['Release Year'] = film_dict['release_year']
                        film_final_dict['Rental Duration'] = film_dict['rental_duration']
                        film_final_dict['Rental Rate'] = film_dict['rental_rate']
                        film_final_dict['Special Features'] = film_dict['special_features']
                        film_final_dict['List Actors'] = film_dict['list_actor']

                        list_films_final.append(film_final_dict)

                        cpt = cpt+1
                json_data = json.dumps(list_films_final,
                                       default=serialiser_pour_json)

            self.response.set_status(200)
            self.response.headers['Content-Type'] = ('application/json;' +
                                                     ' charset=utf-8')
            self.response.out.write(json_data)
        except (db.BadValueError, ValueError, KeyError):
            logging.error('%s', traceback.format_exc())
            self.error(400)
        except Exception:
            logging.error('%s', traceback.format_exc())
            self.error(500)

    def put(self, idFilm):
        try:

            cle = ndb.Key('Film', long(idFilm))

            film = cle.get()

            if film is None:
                status = 201
                film = Film(key=cle)

            else:
                status = 200

            film_dict_in = json.loads(self.request.body)

            film.title = film_dict_in['title']
            if (film_dict_in['description'] is not None):
                film.description = film_dict_in['description']
            if (film_dict_in['release_year'] is not None):
                film.release_year = film_dict_in['release_year']
            film.language_id = film_dict_in['language_id']
            if (film_dict_in['original_language_id'] is not None):
                film.original_language_id = film_dict_in['original_language_id']
            film.rental_duration = film_dict_in['rental_duration']
            film.rental_rate = film_dict_in['rental_rate']
            if (film_dict_in['length'] is not None):
                film.length = film_dict_in['length']
            film.replacement_cost = film_dict_in['replacement_cost']
            film.rating = film_dict_in['rating']
            if (film_dict_in['special_features'] is not None):
                film.special_features = film_dict_in['special_features']

            film.put()

            self.response.set_status(status)
            film_dict = film.to_dict()
            film_dict['idFilm'] = film.key.id()
            film_json = json.dumps(film_dict, default=serialiser_pour_json)
            self.response.headers['Content-Type'] = ('application/json;' +
                                                     ' charset=utf-8')
            self.response.out.write(film_json)

        # Exceptions en lien avec les données fournies (liées à la requête).
        except (db.BadValueError, ValueError, KeyError):
            logging.error('%s', traceback.format_exc())
            # Bad Request.
            self.error(400)

        # Exceptions graves lors de l'exécution du code
        # (non liées à la requête).
        except Exception:
            logging.error('%s', traceback.format_exc())
            # Internal Server Error.
            self.error(500)

    def delete(self, idFilm):
        try:
            if idFilm is not None:
                cle = ndb.Key('Film', long(idFilm))
                ndb.delete_multi(Film.query(ancestor=cle).
                                 fetch(keys_only=True))
                cle.delete()
            else:
                ndb.delete_multi(Film.query().fetch(keys_only=True))

            self.response.set_status(204)

        except (db.BadValueError, ValueError, KeyError):
            logging.error('%s', traceback.format_exc())
            self.error(400)

        except Exception:
            logging.error('%s', traceback.format_exc())
            self.error(500)


class ActorHandler(webapp2.RequestHandler):
    def get(self, idFilm):
        try:
            if idFilm is not None:
                cle = ndb.Key('Film', long(idFilm))
                film = cle.get()
                if (film is None):
                    self.error(404)
                    return
                list_actor = []
                list_index = film.list_actor
#if liste index is not none:
                for indexActeur in list_index:
                    requete = Actor.query()
                    for acteur_a_trouver in requete:
                        if indexActeur == int(acteur_a_trouver.key.id()):
                            acteur_dict_in = acteur_a_trouver.to_dict()
                            list_actor.append(acteur_dict_in)
                data_acteur = json.dumps(list_actor, default=serialiser_pour_json)

            self.response.set_status(200)
            self.response.headers['Content-Type'] = ('application/json;' +
                                                     ' charset=utf-8')
            self.response.out.write(data_acteur)
        except (db.BadValueError, ValueError, KeyError):
            logging.error('%s', traceback.format_exc())
            self.error(400)

        except Exception:
            logging.error('%s', traceback.format_exc())
            self.error(500)


class AddressHandler(webapp2.RequestHandler):
    def get(self, idCustomer):
        try:
            # Cle du propriétaire de l'addresse

            cle_customer = ndb.Key('Customer', long(idCustomer))
            customer = cle_customer.get()
            if (customer is None):
                self.error(404)
                return

            list_address = []
            for address in Address.query(ancestor=cle_customer).fetch():
                address_dict = address.to_dict()
                address_dict['id'] = address.key.id()
                cle_city = ndb.Key('City', int(address_dict['city_id']))
                city = cle_city.get()
                address_dict['city'] = city.city

                cle_country = ndb.Key('Country', int(city.country_id))
                country = cle_country.get()
                address_dict['country'] = country.country

                address_final_dict = dict()
                address_final_dict['Address'] = address_dict['address']
                address_final_dict['Address2'] = address_dict['address2']
                address_final_dict['District'] = address_dict['district']
                address_final_dict['City'] = address_dict['city']
                address_final_dict['Country'] = address_dict['country']
                address_final_dict['Postal Code'] = address_dict['postal_code']
                address_final_dict['Phone'] = address_dict['phone']
                address_final_dict['Last_Update'] = address_dict['last_update']
                list_address.append(address_final_dict)

            json_data = json.dumps(list_address, default=serialiser_pour_json)

            self.response.set_status(200)
            self.response.headers['Content-Type'] = ('application/json;' +
                                                     ' charset=utf-8')
            self.response.out.write(json_data)

        except (db.BadValueError, ValueError, KeyError):
            logging.error('%s', traceback.format_exc())
            self.error(400)

        except Exception:
            logging.error('%s', traceback.format_exc())
            self.error(500)

app = webapp2.WSGIApplication(
    [
        webapp2.Route(r'/',
                      handler=MainPageHandler,
                      methods=['GET']),
        webapp2.Route(r'/chargement', handler=ChargementHandler,
                      methods=['GET']),
        webapp2.Route(r'/films',
                      handler=FilmHandler,
                      methods=['GET', 'POST', 'DELETE']),
        webapp2.Route(r'/films/<idFilm>',
                      handler=FilmHandler,
                      methods=['GET', 'PUT',  'DELETE']),
        webapp2.Route(r'/films/<idFilm>/actors',
                      handler=ActorHandler,
                      methods=['GET']),
        webapp2.Route(r'/customers/<idCustomer>/address',
                      handler=AddressHandler,
                      methods=['GET']),
    ],
    debug=True)