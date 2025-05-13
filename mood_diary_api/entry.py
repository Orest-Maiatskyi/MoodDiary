import uvicorn

from api import api


if __name__ == '__main__':
    uvicorn.run("entry:api", host="localhost", port=8000, reload=True)
