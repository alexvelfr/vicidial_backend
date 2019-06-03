import dotenv
from flask import Flask
from api.api_v1 import api
dotenv.load_dotenv()


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(port=2005)
