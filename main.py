from fastapi import FastAPI, status, HTTPException

app = FastAPI()


@app.get("/", status_code=200)
def read_root():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/add/{a}/{b}", status_code=200)
def add(a: str, b: str):
    """
    Add two numbers together.
    try: 

    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result
    """
    try: 
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=422, detail="Both 'a' and 'b' must be valid numbers" )

    return {"result": a + b}
