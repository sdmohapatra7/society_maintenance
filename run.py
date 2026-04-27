from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file BEFORE creating app

from dev3 import create_app
from dev3.common import Config

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
