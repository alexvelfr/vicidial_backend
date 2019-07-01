import dotenv
import logging
from flask import Flask
from flask_cors import CORS
from api.api_v1 import api
dotenv.load_dotenv()

fh = logging.FileHandler("vicidial.log")
fh.setFormatter(logging.Formatter('[%(asctime)s: %(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S'))
logger = logging.getLogger('vicidial')
logger.setLevel(logging.INFO)
logger.addHandler(fh)

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')

CORS(app, resources={'/api/': {'origins': '*'}})

if __name__ == '__main__':
    app.run(port=2005)
