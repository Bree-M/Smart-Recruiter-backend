from dotenv import load_dotenv
load_dotenv()
from flask_cors import CORS


app = create_app()

CORS(app)
