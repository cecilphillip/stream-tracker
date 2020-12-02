# Established: 12/2/2020
from fastapi import FastAPI

api = FastAPI()

@api.get("/hello")
def hello():    
    """
    this is just the hello function
    """
    return {"hello" : "World"}