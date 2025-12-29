from flask import Blueprint
from flask import render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def root():
    return render_template('root.html')

@main_bp.route('/readme')
def readme():
    return render_template('readme.html')
