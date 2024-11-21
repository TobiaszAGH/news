from flask import Blueprint, render_template

news_bp = Blueprint(
    'news_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@news_bp.route('/')
def hello():
    return render_template('news.html')