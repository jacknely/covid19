from flask_pymongo import PyMongo


class JyMongo(PyMongo):

    def map_db(self, category):
        """
        returns db for virus based on data_set requested
        :param category: name of dataset as str
        :return: db for dataset
        """
        source = {
            "deaths": self.db.deaths,
            "confirmed": self.db.confirmed,
            "recovered": self.db.recovered,
        }
        return source.get(category)

    def get_all_country(self):
        database = self.map_db('confirmed')
        return database.find()

    def get_by_country(self, country, category):
        database = self.map_db(category)
        return database.find({'Country/Region': country.lower()})