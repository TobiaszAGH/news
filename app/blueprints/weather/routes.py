from flask import Blueprint

weather_bp = Blueprint(
    'weather_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@weather_bp.route('/')
def hello():
    return 'weather'