from flask import Blueprint, render_template

weather_bp = Blueprint(
    'weather_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@weather_bp.route('/')
def hello():
    return render_template('weather.html')