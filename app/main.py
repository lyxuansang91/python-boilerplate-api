import uvicorn
from core.server import create_app

app = create_app()


def main():
    uvicorn.run(
        app="main:app",
        reload=True,
        workers=1,
    )

if __name__ == "__main__":
    main()