import redis
import uvicorn
from fastapi import FastAPI

# What does this do?
# This is a server definition for churning up and 
# leveraging the various agents defined for the tasks.
# It tracks and maintains the user contexts and agents.

# Strategy this will utilize is one of minimizing collisions.
# If there are no free agents to process the request when it's received
# it churns up another agent of the task type to service it.
# It's made in a way to ensure scalability.


app = FastAPI()
redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/forward")
async def forwarded_task():
    pass

@app.post("/chat")
async def chat():
    pass

@app.post("/asr")
async def asr():
    pass

@app.post("/tts")
async def tts():
    pass

def serve_rest(**kwargs):
    '''Enable conversations over a REST API'''
    uvicorn.run("genial:chat:app", 
                host="0.0.0.0",
                port=9263,
                reload=False,
                log_level="error",
                debug=True,
                workers=4,
                limit_concurrency=4,
                limit_max_requests=200)
