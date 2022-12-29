from fastapi import Header, HTTPException

async def get_token_header(interntal_token: str= Header(...)):
    if interntal_token != "key":
        raise HTTPException(status_code=400, detail="invalid internal token ")