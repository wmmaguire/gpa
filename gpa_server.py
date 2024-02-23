from app import create_app, db, socketio
from app.models import User

app = create_app()
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

# main
if __name__ == '__main__':
    socketio.run(app)
