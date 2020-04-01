import csv
import requests
from contextlib import closing
from . import db


class Covid19:

    @staticmethod
    def map_url(category):
        """
        returns a url for virus data based on data_set requested
        :param category: name of dataset as str
        :return: url for dataset as str
        """
        source = {
            "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
                      "master/csse_covid_19_data/csse_covid_19_time_series/"
                      "time_series_covid19_deaths_global.csv",
            "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
                         "master/csse_covid_19_data/csse_covid_19_time_series/"
                         "time_series_covid19_confirmed_global.csv",
            "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/" \
                         "master/csse_covid_19_data/csse_covid_19_time_series/t" \
                         "ime_series_covid19_recovered_global.csv",
        }
        return source.get(category)

    def import_data(self, url):
        """
        takes a category and returns a dataset in a dict list
        using a url which is set in map_url method
        :param url: url of dataset as str
        :return: data-frame of virus data
        """
        url_request = requests.get(url, stream=True)
        with closing(url_request) as csv_file:
            csv_file = (line.decode('utf-8') for line in csv_file.iter_lines())
            csv_reader = csv.reader(csv_file, delimiter=',')
            virus_by_country = self.parse_csv(csv_reader)

            return virus_by_country

    @staticmethod
    def parse_csv(csv_reader: iter):
        """
        takes a csv iterator and returns a list of dicts
        containing the data
        :param csv_reader: iterator
        :return: list of dicts
        """
        headers = next(csv_reader)
        virus_by_country = []
        for row in csv_reader:
            country = {headers[0]: row[0].lower(),
                       headers[1]: row[1].lower(),
                       headers[2]: float(row[2]),
                       headers[3]: float(row[3]),
                       'data': dict(zip(headers[4:],
                                        list(map(int, row[4:]))))
                       }
            virus_by_country.append(country)

        return virus_by_country

    @staticmethod
    def save_data_to_db(virus_set, category):
        """
        takes a list of dicts containing virus data
        and saves all to db of given category
        :param virus_set: list of country dicts
        :param category: str for db to save virus set to
        """
        database = db.map_db(category)
        database.delete_many({})
        database.insert_many(virus_set)
        # todo: need a method of updating (not deleting & re-adding)

    @staticmethod
    def compile_region_data(virus_data):
        """
        takes a list of dicts of regions and combines the
        total for dataset given on each date
        :param virus_data: list of country dicts
        :return: dist of combined country data
        """
        country = virus_data[0]['Country/Region']
        state = []
        data = {}
        for region in virus_data:
            state.append(region['Province/State'])
            for key in region['data'].keys():
                date = region['data'][key]
                if key in data.keys():
                    data[key] += date
                else:
                    data[key] = date

        country_data = {'Country/Region': country,
                        'Province/State': state,
                        'data': data},

        return country_data

    def import_multiple_data(self, *categories):
        """
        takes a category and updates associated db
        :param categories: category as str to update
                (eg deaths)
        """
        for category in categories:
            url = db.map_url(category)
            virus_by_country_data = self.import_data(url)
            self.save_data_to_db(virus_by_country_data, category)
