# services/roles/project/api/roles.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request, render_template

from project.api.models import Role
from project import db


roles_blueprint = Blueprint('roles', __name__, template_folder='./templates')


@roles_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.session.add(Role(name=name, description=description))
        db.session.commit()
    roles = Role.query.all()
    return render_template('index.html', roles=roles)


@roles_blueprint.route('/roles/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@roles_blueprint.route('/roles', methods=['POST'])
def add_role():
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
        role = Role.query.filter_by(name=name).first()
        if not role:
            db.session.add(Role(name=name, description=description))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{name} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That role already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@roles_blueprint.route('/roles/<role_id>', methods=['GET'])
def get_single_role(role_id):
    """Get single role details"""
    response_object = {
        'status': 'fail',
        'message': 'Role does not exist'
    }
    try:
        role = Role.query.filter_by(id=int(role_id)).first()
        if not role:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': role.id,
                    'name': role.name,
                    'description': role.description
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@roles_blueprint.route('/roles', methods=['GET'])
def get_all_roles():
    """Get all roles"""
    response_object = {
        'status': 'success',
        'data': {
            'roles': [role.to_json() for role in Role.query.all()]
        }
    }
    return jsonify(response_object), 200
