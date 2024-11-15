from flask import Blueprint

news_bp = Blueprint(
    'news_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@news_bp.route('/')
def hello():
    return 'news'