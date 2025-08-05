from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.webhook_controller import webhook_router
from controllers.chain_controller import chain_router
from controllers.late_enhance_controller import late_enhance_router
from controllers.image_edit_controller import image_edit_router
from controllers.review_controller import review_router

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
    app.include_router(webhook_router)
    app.include_router(chain_router)
    app.include_router(late_enhance_router)
    app.include_router(image_edit_router)
    app.include_router(review_router)

    return app

app = create_app()
