from app import create_app
import os
from dotenv import load_dotenv
import logging

load_dotenv()
app = create_app()
env = os.getenv("env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"This app is running in {env} environment")

if __name__ == "__main__":
    app.run(debug=True)
