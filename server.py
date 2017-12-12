_author_ = 'Chris Donahue, ceuhanod@live.unc.edu, Onyen = ceuhanod'

from flask import (Flask, Response, request, render_template, make_response,
                   redirect)
from flask_restful import Api, Resource, reqparse, abort


import json
import random
import string
from datetime import datetime
from functools import wraps

with open('data.jsonld') as data:
    data = json.load(data)


def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def error_if_package_not_found(package_id):
    if package_id not in data['packages']:
        message = "No package with ID: {}".format(package_id)
        abort(404, message=message)


def filter_and_sort_packages(query='', sort_by='time_received'):

    def matches_query(item):
        (package_id, package) = item
        text = package['title'] + package['recipient']
        return query.lower() in text

    def get_sort_value(item):
        (package_id, package) = item
        return package[sort_by]

    filtered_packages = filter(matches_query, data['packages'].items())

    return sorted(filtered_packages, key=get_sort_value, reverse=True)

def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s

new_package_parser = reqparse.RequestParser()
for arg in ['address', 'title', 'recipient']:
    new_package_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))


update_package_parser = reqparse.RequestParser()
update_package_parser.add_argument(
    'location', type=str, default='')
update_package_parser.add_argument(
    'access_code', type=int, default='')

query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'query', type=str, default='')
query_parser.add_argument(
    'sort_by', type=str, choices=('location', 'time'), default='time')


def render_package_as_html(package):
    return render_template(
        'package+microdata+rdfa.html',
        package=package)

def render_package_inventory_as_html(packages):
    return render_template(
        'packages+microdata+rdfa.html',
        packages=packages)


class Package(Resource):

    def get(self, package_id):
        error_if_package_not_found(package_id)
        return make_response(
            render_package_as_html(
                data['packages'][package_id]), 200)

    def patch(self, package_id):
        error_if_package_not_found(package_id)
        package = data['packages'][package_id]
        update = update_package_parser.parse_args()
        package['location'] = update['location']
        if len(update['access_code'].strip()) > 0:
            package.setdefault('access_code', []).append(update['access_code'])
        return make_response(
            render_package_as_html(package), 200)


class PackageAsJSON(Resource):

      def get(self, package_id):
        error_if_package_not_found(package_id)
        package = data['packages'][package_id]
        package['@context'] = data['@context']
        return package

class PackageInventory(Resource):

    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_package_inventory_as_html(
                filter_and_sort_packages(**query)), 200)

    def post(self):
        package = new_package_parser.parse_args()
        package_id = generate_id()
        package['@id'] = 'request/' + package_id
        package['@type'] = 'packagecenter_locker_system:Package'

        package['time_received'] = datetime.isoformat(datetime.now())
        data['packages'][package_id] = package
        return make_response(
            render_package_inventory_as_html(
                filter_and_sort_packages()), 201)


class PackageInventoryAsJSON(Resource):
    def get(self):
        return data




app = Flask(__name__)
api = Api(app)
api.add_resource(PackageInventory, '/packages')
api.add_resource(PackageInventoryAsJSON, '/packages.json')
api.add_resource(Package, '/package/<string:package_id>')
api.add_resource(PackageAsJSON, '/package/<string:package_id>.json')

@app.route('/')
def index():
    return redirect(api.url_for(PackageInventory), code=303)



@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5555,
        debug=True,
        use_debugger=False,
        use_reloader=False)
