from fastapi import APIRouter, Depends
from db.models.user import User
from routers.jwt_auth_user import currentUser
from db.data.product import product_list

router=APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        404: {"message":"No encontrado."}
    }
)

######################################################################################################

@router.get("/")
async def product(user: User=Depends(currentUser)):
    return product_list


@router.get("/{id}")
async def productById(id: int, user: User=Depends(currentUser)):
    try:
        return product_list[id-1]
    except:
        return "Producto no encontrado"