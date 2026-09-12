from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from config.database import get_db
from models.producto import Producto as ProductoModel
from models.stock import Stock as StockModel
from schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate, ProductoDetalleResponse, ListaCompraResponse
from utils.auth import get_current_active_user
from models.user import User as UserModel

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/", response_model=ProductoResponse)
async def create_producto(
    producto: ProductoCreate, 
    current_user: UserModel = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    # Verificar que no exista otro producto con el mismo código
    db_producto = db.query(ProductoModel).filter(ProductoModel.codigo == producto.codigo).first()
    if db_producto:
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")
    
    db_producto = ProductoModel(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/", response_model=List[ProductoResponse])
async def read_productos(
    skip: int = 0, 
    limit: int = 100, 
    current_user: UserModel = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    productos = db.query(ProductoModel).offset(skip).limit(limit).all()
    return productos

@router.get("/lista-compras", response_model=List[ListaCompraResponse])
async def read_lista_compras(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    productos = (
        db.query(
            ProductoModel.id.label("producto_id"),
            ProductoModel.codigo,
            ProductoModel.nombre,
            func.coalesce(func.sum(StockModel.cantidad), 0).label("stock_actual"),
            ProductoModel.stock_minimo
        )
        .outerjoin(
            StockModel,
            StockModel.producto_id == ProductoModel.id
        )
        .filter(
            ProductoModel.activo == True
        )
        .group_by(
            ProductoModel.id,
            ProductoModel.codigo,
            ProductoModel.nombre,
            ProductoModel.stock_minimo
        )
        .having(
            func.coalesce(func.sum(StockModel.cantidad), 0)
            < ProductoModel.stock_minimo
        )
        .all()
    )

    return [
        {
            "producto_id": producto.producto_id,
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo,
            "cantidad_sugerida": producto.stock_minimo - producto.stock_actual
        }
        for producto in productos
    ]

@router.get("/{producto_id}", response_model=ProductoDetalleResponse)
async def read_producto(
    producto_id: int, 
    current_user: UserModel = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    # Obtener el producto con su stock total
    db_producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Calcular stock total sumando todas las ubicaciones
    stock_total = db.query(func.sum(StockModel.cantidad)).filter(StockModel.producto_id == producto_id).scalar() or 0
    
    # Crear respuesta con el stock total
    response = ProductoDetalleResponse.model_validate(db_producto)
    response.stock_total = stock_total
    
    return response

@router.put("/{producto_id}", response_model=ProductoResponse)
async def update_producto(
    producto_id: int, 
    producto: ProductoUpdate, 
    current_user: UserModel = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    db_producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar que no exista otro producto con el mismo código
    if producto.codigo and producto.codigo != db_producto.codigo:
        codigo_exists = db.query(ProductoModel).filter(ProductoModel.codigo == producto.codigo).first()
        if codigo_exists:
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")
    
    # Actualizar solo los campos proporcionados
    producto_data = producto.model_dump(exclude_unset=True)
    for key, value in producto_data.items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(
    producto_id: int, 
    current_user: UserModel = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    db_producto = db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar si hay stocks o movimientos asociados antes de eliminar
    if db_producto.stocks:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar el producto porque tiene stock asociado"
        )
    
    if db_producto.movimientos:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar el producto porque tiene movimientos de inventario asociados"
        )
    
    db.delete(db_producto)
    db.commit()
    return None 