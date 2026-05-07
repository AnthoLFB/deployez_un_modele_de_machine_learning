import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api import routes
from .db.database import engine, Base

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ML Prediction API",
    description="API pédagogique pour prédire une target à partir de l'âge et du salaire.",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Une erreur interne est survenue. Veuillez contacter le support.", "error": str(exc)},
    )

# Inclusion des routes
app.include_router(routes.router)

@app.get("/")
async def root():
    return {
        "app_name": os.getenv("APP_NAME", "ML Prediction API"),
        "version": os.getenv("VERSION", "1.0.0")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
