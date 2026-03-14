from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import database
import models
import auth
import utils
import uvicorn

app = FastAPI(title="Vulnerable API for AI Reviewer Testing")

# Globally mutable state - Bad practice
request_count = 0

@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/")
def read_root():
    global request_count
    request_count += 1
    return {"message": "Welcome to the buggy API", "request_count": request_count}

@app.post("/register")
def register(user: models.user_model):
    # Bug: Directly uses user input in vulnerable query
    hashed = auth.hash_password_md5(user.passw)
    database.add_user(user.UserName, hashed, user.email_address)
    return {"status": "User registered"}

@app.get("/users/{username}")
def get_user(username: str):
    # EXPOSED SQL INJECTION
    user = database.get_user_by_username_vulnerable(username)
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return {"user": user}

@app.post("/login")
def login(req: models.LoginRequest):
    user = database.get_user_by_username_vulnerable(req.u)
    if user and user[2] == auth.hash_password_md5(req.p):
        token = auth.create_token({"sub": user[1], "isAdmin": user[4]})
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/admin/leak")
def leak_config(token: str):
    # Manual token verification (instead of Depends)
    payload = auth.verify_token(token)
    if payload and auth.check_admin(payload):
        # Sensitive data exposure
        config = utils.get_config()
        return {"config": config}
    return JSONResponse(status_code=403, content={"error": "Forbidden"})

@app.post("/process")
async def process_items(items: list):
    # BLOCKING CALL in async handler
    results = await utils.process_data_slowly(items)
    return {"results": results}

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    # Poor error handling: catch-all that hides details but also logs nothing
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong, but I won't tell you what."},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
