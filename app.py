import data.initializer
import routes
from flask import Flask
app = Flask(__name__)
app.secret_key = '1234'

data.initializer.initialize()


# Blueprint registration
app.register_blueprint(routes.main_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
