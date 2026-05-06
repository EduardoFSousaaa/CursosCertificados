import os

from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402
from seeds import register_seed_command  # noqa: E402

app = create_app(os.environ.get("FLASK_ENV", "development"))

with app.app_context():
    from flask_migrate import upgrade
    upgrade()

register_seed_command(app)

if __name__ == "__main__":
    app.run()
