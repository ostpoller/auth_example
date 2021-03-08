from auth import create_app
from auth.models import db, User


app = create_app()


@app.shell_context_processor
def make_shell_context():
    context = {
        'db': db,
        'User': User
    }
    return context
