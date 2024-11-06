from flask import Blueprint

economy_bp = Blueprint(
    'economy_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@economy_bp.route('/')
def hello():
    return 'economy'