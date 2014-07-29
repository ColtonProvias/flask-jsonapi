from flask import Blueprint, jsonify, request, abort
from sqlalchemy_jsonapi import JSONAPI


class JSONAPIEndpoint:
    def __init__(self, name):
        self.name = name

    def parse_request(self):
        args = {}

        for arg, value in request.args.items():
            if arg.endswith(']'):
                arg, key = arg.rstrip(']').split('[')
                if arg not in args.keys():
                    args[arg] = {}
                args[arg][key] = value
            else:
                args[arg] = value

        include = args.pop('include', None)
        include = include.split(',') if include is not None else None

        fields = args.pop('fields', None)
        if isinstance(fields, dict):
            for key, value in fields.items():
                fields[key] = value.split(',')
        elif fields is not None:
            fields = fields.split(',')

        sort = args.pop('sort', None)
        if isinstance(sort, dict):
            for key, value in sort.items():
                sort[key] = value.split(',')
        elif sort is not None:
            sort = sort.split(',')

        return include, sort, fields, args

    def dispatch_collection(self):
        if request.method == 'GET':
            return self.collection_get()
        elif request.method == 'POST':
            return self.collection_post()

    def dispatch_object(self, object_id):
        if request.method == 'GET':
            return self.object_get(object_id)
        elif request.method == 'PUT':
            return self.object_put(object_id)
        elif request.method == 'PATCH':
            return self.object_patch(object_id)
        elif request.method == 'DELETE':
            return self.object_delete(object_id)

    def create_blueprint(self, url_prefix=''):
        blueprint = Blueprint(self.name, __name__)
        url = url_prefix + '/' + self.name
        blueprint.add_url_rule(url, view_func=self.dispatch_collection,
                               methods=['GET', 'POST'])
        blueprint.add_url_rule(url + '/<object_id>',
                               view_func=self.dispatch_object,
                               methods=['GET', 'PUT', 'PATCH', 'DELETE'])
        return blueprint

    def render_response(self, data, status_code=200):
        return jsonify(data), status_code


class SQLAlchemyEndpoint(JSONAPIEndpoint):
    def __init__(self, model_class, session):
        self.model_class = model_class
        self.session = session
        name = getattr(model_class, 'jsonapi_key', model_class.__tablename__)
        super().__init__(name)

    @property
    def query(self):
        return self.session.query(self.model_class)

    def get_obj(self, object_id):
        if ',' in object_id:
            object_ids = object_id.split(',')
            return [self.query.get(obj_id) for obj_id in object_ids]
        else:
            return self.query.get(object_id)

    @property
    def serializer(self):
        return JSONAPI(self.model_class).serialize

    def collection_get(self):
        include, sort, fields, args = self.parse_request()
        collection = self.query.all()
        return self.render_response(self.serializer(collection, fields=fields,
                                                    sort=sort))

    def object_get(self, object_id):
        include, sort, fields, args = self.parse_request()
        obj = self.get_obj(object_id)
        if obj is None:
            abort(404)
        return self.render_response(self.serializer(obj, fields=fields,
                                                    sort=sort))

    def object_delete(self, object_id):
        obj = self.obj_getter(object_id)
        if obj is None:
            abort(404)
        self.session.delete(obj)
        self.session.commit()
        return self.render_response({}, 204)


class FlaskJSONAPI(object):
    blueprints = []

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app

    def init_app(self, app):
        self.app = app

        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint)

    def add_endpoint(self, view, url_prefix=''):
        blueprint = view.create_blueprint(url_prefix)
        if self.app:
            self.app.register_blueprint(blueprint)
