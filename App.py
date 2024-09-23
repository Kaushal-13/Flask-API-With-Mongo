from flask import Flask
from config import DevelopmentConfig
from routes.user_routes import user_bp
from utils.rate_limiter import configure_limiter


app = Flask(__name__)
limiter = configure_limiter(app)

app.register_blueprint(user_bp)


@app.route('/')
def base():
    return "MONGO DB + FLASK API IS running"


if __name__ == '__main__':
    app.run(debug=True)
