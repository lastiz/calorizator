from app.app import create_app
from app.config import settings

import uvicorn


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app, host="127.0.0.1", port=settings.APP_PORT)
