import uvicorn
from utility import settings

def start_server(host="0.0.0.0",
                 port=settings.PORT):
    uvicorn.run("main:app",
                host=host,
                port=port,
                reload=False)


if __name__ == "__main__":
    start_server()
