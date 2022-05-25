import uvicorn


def start_server(host="0.0.0.0",
                 port=8000):
    uvicorn.run("main:app",
                host=host,
                port=port,
                reload=False)


if __name__ == "__main__":
    start_server()
