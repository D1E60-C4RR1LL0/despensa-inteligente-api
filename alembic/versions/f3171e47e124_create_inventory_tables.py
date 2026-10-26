"""create inventory tables

Revision ID: f3171e47e124
Revises: 0c11a0e481fc
Create Date: 2026-10-26 17:24:12.981823

"""
from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3171e47e124'
down_revision: Union[str, None] = '0c11a0e481fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Detectar esquemas heredados antes de ejecutar DDL no transaccional en MySQL.
    if not context.is_offline_mode():
        inventory_tables = {
            'categorias', 'proveedores', 'tipos_movimiento', 'ubicaciones',
            'productos', 'movimientos_inventario', 'stocks',
        }
        existing = inventory_tables.intersection(
            sa.inspect(op.get_bind()).get_table_names()
        )
        if existing:
            raise RuntimeError(
                'Existen tablas de inventario anteriores a esta migracion: '
                + ', '.join(sorted(existing))
                + '. Revisar docs/devops/AUDITORIA_ARRANQUE.md antes de continuar.'
            )
    op.create_table('categorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorias_id'), 'categorias', ['id'], unique=False)
    op.create_index(op.f('ix_categorias_nombre'), 'categorias', ['nombre'], unique=True)
    op.create_table('proveedores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('contacto', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('direccion', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proveedores_id'), 'proveedores', ['id'], unique=False)
    op.create_index(op.f('ix_proveedores_nombre'), 'proveedores', ['nombre'], unique=False)
    op.create_table('tipos_movimiento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=20), nullable=True),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('afecta_stock', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_index(op.f('ix_tipos_movimiento_codigo'), 'tipos_movimiento', ['codigo'], unique=True)
    op.create_index(op.f('ix_tipos_movimiento_id'), 'tipos_movimiento', ['id'], unique=False)
    op.create_table('ubicaciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('direccion', sa.String(length=255), nullable=True),
    sa.Column('tipo', sa.String(length=50), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ubicaciones_id'), 'ubicaciones', ['id'], unique=False)
    op.create_index(op.f('ix_ubicaciones_nombre'), 'ubicaciones', ['nombre'], unique=True)
    op.create_table('productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=50), nullable=True),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('precio_compra', sa.Float(precision=2), nullable=True),
    sa.Column('precio_venta', sa.Float(precision=2), nullable=True),
    sa.Column('unidad_medida', sa.String(length=20), nullable=True),
    sa.Column('stock_minimo', sa.Integer(), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.Column('categoria_id', sa.Integer(), nullable=True),
    sa.Column('proveedor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ),
    sa.ForeignKeyConstraint(['proveedor_id'], ['proveedores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_productos_codigo'), 'productos', ['codigo'], unique=True)
    op.create_index(op.f('ix_productos_id'), 'productos', ['id'], unique=False)
    op.create_index(op.f('ix_productos_nombre'), 'productos', ['nombre'], unique=False)
    op.create_table('movimientos_inventario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('cantidad', sa.Float(precision=2), nullable=False),
    sa.Column('referencia', sa.String(length=50), nullable=True),
    sa.Column('observaciones', sa.Text(), nullable=True),
    sa.Column('tipo_movimiento_id', sa.Integer(), nullable=False),
    sa.Column('producto_id', sa.Integer(), nullable=False),
    sa.Column('ubicacion_origen_id', sa.Integer(), nullable=True),
    sa.Column('ubicacion_destino_id', sa.Integer(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
    sa.ForeignKeyConstraint(['tipo_movimiento_id'], ['tipos_movimiento.id'], ),
    sa.ForeignKeyConstraint(['ubicacion_destino_id'], ['ubicaciones.id'], ),
    sa.ForeignKeyConstraint(['ubicacion_origen_id'], ['ubicaciones.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movimientos_inventario_id'), 'movimientos_inventario', ['id'], unique=False)
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Float(precision=2), nullable=True),
    sa.Column('producto_id', sa.Integer(), nullable=True),
    sa.Column('ubicacion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
    sa.ForeignKeyConstraint(['ubicacion_id'], ['ubicaciones.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('producto_id', 'ubicacion_id', name='uix_producto_ubicacion')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')
    op.drop_index(op.f('ix_movimientos_inventario_id'), table_name='movimientos_inventario')
    op.drop_table('movimientos_inventario')
    op.drop_index(op.f('ix_productos_nombre'), table_name='productos')
    op.drop_index(op.f('ix_productos_id'), table_name='productos')
    op.drop_index(op.f('ix_productos_codigo'), table_name='productos')
    op.drop_table('productos')
    op.drop_index(op.f('ix_ubicaciones_nombre'), table_name='ubicaciones')
    op.drop_index(op.f('ix_ubicaciones_id'), table_name='ubicaciones')
    op.drop_table('ubicaciones')
    op.drop_index(op.f('ix_tipos_movimiento_id'), table_name='tipos_movimiento')
    op.drop_index(op.f('ix_tipos_movimiento_codigo'), table_name='tipos_movimiento')
    op.drop_table('tipos_movimiento')
    op.drop_index(op.f('ix_proveedores_nombre'), table_name='proveedores')
    op.drop_index(op.f('ix_proveedores_id'), table_name='proveedores')
    op.drop_table('proveedores')
    op.drop_index(op.f('ix_categorias_nombre'), table_name='categorias')
    op.drop_index(op.f('ix_categorias_id'), table_name='categorias')
    op.drop_table('categorias')
