from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.rembg_controller import router as image_router

def create_app() -> FastAPI:
    app = FastAPI(title="Background Removal API")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Router’ları ekle
    app.include_router(image_router, prefix="", tags=["images"])
    return app

app = create_app()
