from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import user, order, auth, product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=["*"]
)

app.include_router(user.router)
app.include_router(order.router)
app.include_router(auth.router)
app.include_router(product.router)


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error"
        }
    )
