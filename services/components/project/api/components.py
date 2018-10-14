# services/components/project/api/components.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request, render_template

from project.api.models import Component
from project import db


components_blueprint = Blueprint('components', __name__, template_folder='./templates')


@components_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.session.add(Component(name=name, description=description))
        db.session.commit()
    components = Component.query.all()
    return render_template('index.html', components=components)


@components_blueprint.route('/components/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@components_blueprint.route('/components', methods=['POST'])
def add_component():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    name = post_data.get('name')
    description = post_data.get('description')
    try:
        component = Component.query.filter_by(name=name).first()
        if not component:
            db.session.add(Component(name=name, description=description))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{component} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That component already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@components_blueprint.route('/components/<component_id>', methods=['GET'])
def get_single_component(component_id):
    """Get single component details"""
    response_object = {
        'status': 'fail',
        'message': 'Component does not exist'
    }
    try:
        component = Component.query.filter_by(id=int(component_id)).first()
        if not component:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': component.id,
                    'name': component.name,
                    'description': component.description
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@components_blueprint.route('/components', methods=['GET'])
def get_all_components():
    """Get all components"""
    response_object = {
        'status': 'success',
        'data': {
            'components': [component.to_json() for component in Component.query.all()]
        }
    }
    return jsonify(response_object), 200
