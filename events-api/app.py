import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/events/latest")
def get_latest_events():
    events = [
        {"date": "2025-06-04", "user": "user1", "event": "login"},
        {"date": "2025-06-04", "user": "user2", "event": "logout"},
    ]
    return events


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
