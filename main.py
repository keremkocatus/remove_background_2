from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.rembg_controller import rembg_router
from controllers.enhance_controller import enhance_router
from controllers.caption_controller import caption_router
from controllers.upload_controller import upload_router
from controllers.chain_controller import chain_router
from controllers.late_enhance_controller import late_enhance_router

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
    app.include_router(upload_router, prefix="/upload")
    app.include_router(chain_router)
    app.include_router(late_enhance_router)

    return app

app = create_app()
