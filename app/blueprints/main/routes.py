from flask import Blueprint, render_template


main_bp = Blueprint(
    'main_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@main_bp.route('/', methods=['GET'])
def main():
    return render_template('main.html')