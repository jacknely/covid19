from flask import jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger
from app import api, create_app, db
from app.virus import Covid19


virus = Covid19()


class Country(Resource):

    @swagger.operation(notes='these are notes')
    def get(self, category: str, country: str):
        data_set = db.get_by_country(country, category)

        results = []
        for query in data_set:
            results.append({'Country/Region': query['Country/Region'],
                            'Province/State': query['Province/State'],
                            'Lat': query['Lat'],
                            'Long': query['Long'],
                            'data': query['data']})
        if len(results) > 1:
            results = virus.compile_region_data(results)

        return jsonify(results)


class Countries(Resource):

    @swagger.operation(notes='these are notes')
    def get(self):
        data_set = db.get_all_country()

        results = []
        for query in data_set:
            results.append(query['Country/Region'])
        results_no_duplicates = list(set(results))

        return results_no_duplicates


class Update(Resource):

    @swagger.operation(notes='these are notes')
    def get(self):
        virus.import_multiple_data("deaths", "recovered", "confirmed")
        return {"message": "update successful"}, 200


api.add_resource(Country, '/<string:category>/<string:country>')
api.add_resource(Countries, '/countries')
api.add_resource(Update, '/update')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


