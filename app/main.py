# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.sequence_buffer import FeatureSequenceBuffer
from app.ensemble import ensemble_predict
from app.analytics import record_state, snapshot
from app.signal_engine import signal
from app.hooks import start_hooks, stop_hooks, event_buffer
from app.feature_extractor import extract_features
from app.rules import is_idle
from app.trainers.training_manager import TrainingManager


from collections import deque


LAST_FEATURES = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    trainer.bootstrap()
    start_hooks()
    print("[APP] Started")
    yield
    stop_hooks()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

trainer = TrainingManager()
model = trainer.rf.model
gru = trainer.gru.gru

seq_buffer = FeatureSequenceBuffer(max_len=10)
SEQUENCE_WINDOW = 20
LAST_SEQUENCE = deque(maxlen=SEQUENCE_WINDOW)

# Static dashboard
app.mount("/dashboard", StaticFiles(directory="app/dashboard", html=True), name="dashboard")


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/monitor")
def monitor():
    global LAST_FEATURES

    features = extract_features(event_buffer)

    if not features or is_idle(features):
        return {"state": "idle", "features": features}

    LAST_FEATURES = list(features.values())
    prediction = model.predict(LAST_FEATURES)

    return {
        "state": prediction,
        "features": features,
        "buffer_size": len(event_buffer)
    }


@app.get("/state")
def get_state():
    global LAST_FEATURES, LAST_SEQUENCE

    features = extract_features(event_buffer)
    if not features:
        return {"state": "idle"}

    if is_idle(features):
        seq_buffer.clear()
        return {"state": "idle"}

    seq_buffer.add(features)

    rf_pred = model.predict(list(features.values()))
    gru_pred = None

    if seq_buffer.is_ready():
        seq = seq_buffer.get_sequence()
        gru_pred = gru.predict(seq)
        LAST_SEQUENCE = seq

    final_state = ensemble_predict(rf_pred, gru_pred)
    LAST_FEATURES = list(features.values())
    
    LAST_SEQUENCE.append(features)
    record_state(final_state)
    signal(final_state)


    return {
        "state": final_state,
        "rf": rf_pred,
        "gru": gru_pred
    }



@app.get("/stats")
def stats():
    return trainer.stats()



@app.post("/feedback")
def feedback(label: str):
    if LAST_FEATURES is None:
        return {"status": "no recent activity"}

    retrained = trainer.add_feedback(
        LAST_FEATURES,
        label,
        sequence=LAST_SEQUENCE
    )

    return {
        "status": "feedback received",
        "rf_retrained": retrained,
        "gru_trained": gru.trained
    }

@app.get("/analytics")
def analytics():
    return snapshot()
