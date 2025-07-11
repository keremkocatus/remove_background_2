from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.rembg_controller import rembg_router
from controllers.enhance_controller import enhance_router
from controllers.caption_controller import caption_router

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
    app.include_router(rembg_router, prefix="/rembg")
    app.include_router(enhance_router, prefix="/enhance")
    app.include_router(caption_router, prefix="/caption")

    return app

app = create_app()
