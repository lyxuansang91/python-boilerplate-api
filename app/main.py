import os
import sys

import uvicorn

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.server import create_app

app = create_app()


def main():
    uvicorn.run(
        app="app.main:app", host="0.0.0.0", reload=True, workers=1, port=settings.PORT
    )


if __name__ == "__main__":
    main()
