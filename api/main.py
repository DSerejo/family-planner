
from app.main import app
from fastapi.responses import JSONResponse, Response

def handler(request):
    return JSONResponse(content={"message": "Hello, World!"}).render()
    # Ensure the request method is supported
    if request.method == 'GET':
        # You can handle FastAPI routing and responses here
        # For example, you can use app.__call__ to process the request
        scope = {
            'type': 'http',
            'path': request.path,
            'httpMethod': request.method,
            'headers': dict(request.headers),
            'queryParameters': request.query_params,
            'body': request.body,
        }
        receive = None  # As FastAPI doesn't use it
        send = lambda data: JSONResponse(content=data)
        response = app(scope, receive, send)
        return response
    else:
        return JSONResponse(status_code=405, content={"message": "Method Not Allowed"})