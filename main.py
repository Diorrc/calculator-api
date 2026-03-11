from fastapi import FastAPI, status, HTTPException, Depends
from google.cloud import bigquery

app = FastAPI()

# Dependency method to provide a BigQuery client
# This will be used by the other endpoints where a database connection is necessary
def get_bq_client():
    # client automatically uses Cloud Run's service account credentials
    client = bigquery.Client()
    try:
        yield client
    finally:
        client.close()

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


@app.get("/subtract/{a}/{b}", status_code=200)
def subtract(a: str, b: str):
    """
    Subtract two numbers together.
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

    return {"operation": "subtract", "a": a,"b": b, "result": a - b}

@app.get("/multiply/{a}/{b}", status_code=200)
def multiply(a: str, b: str):
    """
    multiply two numbers together.
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

    return {"operation": "multiply", "a'": a, "b": b, "result": a * b}

@app.get("/divide/{a}/{b}", status_code=200)
def divide(a: str, b: str):
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(status_code=422, detail="Both 'a' and 'b' must be valid numbers")

    if b == 0:
        raise HTTPException(status_code=422, detail="Division by zero is not allowed")

    return {"operation": "divide", "a": a, "b": b, "result": a / b}

@app.get("/power/{base}/{exponent}", status_code=200)
def power(base: str, exponent: str):
    """
    Raise a base number to a given exponent.

    Path Parameters:
    - base: the base number
    - exponent: the exponent value

    Returns:
    - JSON containing the operation, inputs, and the computed power result.
    """
    try:
        base = float(base)
        exponent = float(exponent)
    except ValueError:
        raise HTTPException(status_code=422, detail="Both 'a' and 'b' must be valid numbers")

    result = base ** exponent

    return {"operation": "power", "base": base, "exponent": exponent, "result": result}

@app.get("/km-to-miles/{km}", status_code=200)
def km_to_miles(km: str):
    """
    Convert kilometers to miles.

    Path Parameters:
    - km: distance in kilometers

    Returns:
    - JSON containing the converted distance in miles.
    """
    try:
        km = float(km)
    except ValueError:
        raise HTTPException(status_code=422, detail="All arguments must be valid numbers")

    miles = km * 0.621371

    return {"operation": "km_to_miles", "kilometers": km, "result": miles}

@app.get("/compoundinterest/{principal}/{rate}/{years}", status_code=200)
def compoundinterest(principal: str, rate: str, years: str):
    """
    Calculate compound interest.

    Path Parameters:
    - principal: initial principal balance
    - rate: annual interest rate
    - years: number of years

    Returns:
    - JSON containing the computed interest.
    """
    try:
        principal = float(principal)
        rate = float(rate)
        years = float(years)
    except ValueError:
        raise HTTPException(status_code=422, detail="All arguments must be valid numbers")
    r = rate / 100
    amount = principal * (1 + r) ** years
    interest = amount - principal

    return {"operation": "compoundinterest", "principal": principal, "rate": rate, "years": years, "result": interest}

@app.get("/dbwritetest", status_code=200)
def dbwritetest(bq: bigquery.Client = Depends(get_bq_client)):
    """
    Writes a simple test row to a BigQuery table.

    Uses the `get_bq_client` dependency method to establish a connection to BigQuery.
    """
    # Define a Python list of objects that will become rows in the database table
    # In this instance, there is only a single object in the list
    row_to_insert = [
        {
            "endpoint": "/dbwritetest",
            "result": "Success",
            "status_code": 200
        }
    ]
    
    # Use the BigQuery interface to write our data to the table
    # If there are errors, store them in a list called `errors`
    # YOU MUST UPDATE YOUR PROJECT AND DATASET NAME BELOW BEFORE THIS WILL WORK!!!
    errors = bq.insert_rows_json("project-fdc64e01-d38d-4013-b83.calculator.api_logs", row_to_insert)

    # If there were any errors, raise an HTTPException to inform the user
    if errors:
        # Log the full error to your Cloud Run logs for debugging
        print(f"BigQuery Insert Errors: {errors}")
        
        # Raise an exception to the API user
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to log data to BigQuery",
                "errors": errors  # Optional: return specific BQ error details
            }
        )

    # If there were NOT any errors, send a friendly response message to the API caller
    return {"message": "Log entry created successfully"}