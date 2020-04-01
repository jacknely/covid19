import pathlib
import pytest
from app.virus import Covid19
from flask_pymongo import PyMongo


class TestCovid19:

    def setup_method(self):
        self.test_virus = Covid19()
        self.current_dir = pathlib.Path(__file__).parent

    def test_map_url(self):
        test_url = self.test_virus.map_url('deaths')

        assert test_url == "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
                            "csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

    def test_map_db(self):
        test_db = self.test_virus.map_db("deaths")

        assert test_db == "db.mongo.deaths"


if __name__ == '__main__':
    pytest.main()
