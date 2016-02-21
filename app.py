from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from baby_names import baby_names_utilities
from imdb_scraper import imdb_scraper

# Creat app and API
app = Flask(__name__)
api = Api(app)

# Arg parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', type=str, help="The 'name' parameter must be a string!")
parser.add_argument('gender', type=str, help="The 'gender' parameter must be a string!")
parser.add_argument('year', type=int, help="The 'year' parameter must be a integer!")

# Resource fields for output
record_fields = { 
    'year': fields.Float,
    'count': fields.Float
}

record_list_fields = {
    'records': fields.List(fields.Nested(record_fields))
}

# Load data
baby_names_df = baby_names_utilities.load_baby_names_data()

# Define APIs
class ActorPopularMovies(Resource):
    def get(self, actor_name):
        return imdb_scraper.get_actor_popular_movies(actor_name)

class BabyNamesSegment(Resource):
    #@marshal_with(record_list_fields)
    def get(self):
        args = parser.parse_args()
        segment = baby_names_utilities.segment_data({'name':args['name'], 
                                                      'gender':args['gender'], 
                                                     'year':args['year']},
                                                     ['year','count'])

        segment_json = segment.to_json(orient='records')
        
        return segment_json


# Add APIs 
api.add_resource(ActorPopularMovies, '/popular-movies/<string:actor_name>')
api.add_resource(BabyNamesSegment, '/segment-baby-names')

# App routing
@app.route('/')
def home():
    return render_template('index.html')


# Run the app
if __name__ == "__main__":
    app.run(debug=True)