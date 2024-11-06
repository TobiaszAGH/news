from flask import Blueprint

sport_bp = Blueprint(
    'sport_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@sport_bp.route('/')
def hello():
    return 'sport'