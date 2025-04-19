from app import create_app
import os
from dotenv import load_dotenv
import logging

load_dotenv()
app = create_app()
env = os.getenv("env", "development")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"This app is running in {env} environment")

if __name__ == "__main__":
    print("ENV:", os.getenv("env"))
    print("PORT:", app.config["PORT"])
    debug_mode = env == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=app.config["PORT"])