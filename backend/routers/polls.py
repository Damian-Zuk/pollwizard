from fastapi import APIRouter, Depends
from auth.jwt_bearer import jwtBearer

router = APIRouter(
    prefix="/polls",
    tags=["Polls"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(jwtBearer())])
async def read_polls():
    return [{"name": "Co lepsze iPhone czy Android?"}, {"name": "Co według Ciebie było pierwsze jajko czy kura?"}]
