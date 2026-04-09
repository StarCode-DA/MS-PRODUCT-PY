# 📦 Eclipse Bar — Microservicio de Productos (MS-PRODUCT-PY)

Microservicio encargado de la gestión del **catálogo maestro de productos** del sistema **Eclipse Bar**. Permite administrar los productos disponibles con su información completa: nombre, unidad, categoría, costo y precio.

---

## 📋 Tabla de contenido

- [Tecnologías](#tecnologías)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
- [Validaciones](#validaciones)
- [Permisos por rol](#permisos-por-rol)
- [Modelos de base de datos](#modelos-de-base-de-datos)
- [Relación con otros microservicios](#relación-con-otros-microservicios)
- [Correr con Docker](#correr-con-docker)

---

## 🛠 Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) — Framework web
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM para base de datos
- [PostgreSQL](https://www.postgresql.org/) — Base de datos
- [Pydantic V2](https://docs.pydantic.dev/) — Validación de datos
- [Uvicorn](https://www.uvicorn.org/) — Servidor ASGI

---

## ✅ Requisitos previos

- Python >= 3.11
- PostgreSQL corriendo (o usar Docker)
- Base de datos `eclipsebar_db` inicializada con `init.sql`
- Tabla `products` creada (ver script en [Modelos de base de datos](#modelos-de-base-de-datos))
- Token JWT válido generado por `MS-AUTH-PY` para endpoints protegidos

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone 
cd MS-PRODUCT-PY

# Instalar dependencias
pip install -r requirements.txt

# Correr el servidor
uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload
```

---

## 🔧 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/eclipsebar_db
```

---

## 📁 Estructura del proyecto

```
src/
├── models/
│   └── product.py           # Modelo SQLAlchemy de la tabla products
├── routers/
│   └── products.py          # Endpoints REST del microservicio
├── schemas/
│   └── product.py           # Schemas Pydantic (validación de datos)
├── utils/
├── database.py              # Configuración de conexión a PostgreSQL
├── main.py                  # Punto de entrada de la aplicación
└── config.py                # Configuración del servicio
```

---

## 📡 Endpoints

Base URL: `http://localhost:8003`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos/product/` | Listar productos del catálogo |
| POST | `/productos/product/` | Crear un nuevo producto |
| PUT | `/productos/product/{id}` | Actualizar un producto existente |
| PATCH | `/productos/product/{id}/toggle-activo` | Activar o desactivar un producto |

---

### GET `/productos/product/`

Retorna el catálogo completo de productos. Soporta filtros opcionales por nombre y categoría.

**Query params:**

| Param | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `name` | string | ❌ | Filtrar por nombre (búsqueda parcial, insensible a mayúsculas) |
| `category` | string | ❌ | Filtrar por categoría exacta |

```json
// Response
[
  {
    "id": 1,
    "name": "Aguardiente Antioqueño",
    "unit": "botella",
    "category": "licores",
    "cost": 25000.0,
    "price": 45000.0,
    "activo": true
  }
]
```

---

### POST `/productos/product/`

Crea un nuevo producto en el catálogo maestro.

```json
// Request
{
  "name": "Aguardiente Antioqueño",
  "unit": "botella",
  "category": "licores",
  "cost": 25000.0,
  "price": 45000.0
}

// Response
{
  "id": 1,
  "name": "Aguardiente Antioqueño",
  "unit": "botella",
  "category": "licores",
  "cost": 25000.0,
  "price": 45000.0,
  "activo": true
}
```

---

### PUT `/productos/product/{id}`

Reemplaza todos los campos de un producto existente.

```json
// Request
{
  "name": "Aguardiente Antioqueño",
  "unit": "botella",
  "category": "licores",
  "cost": 27000.0,
  "price": 48000.0
}

// Response
{
  "id": 1,
  "name": "Aguardiente Antioqueño",
  "unit": "botella",
  "category": "licores",
  "cost": 27000.0,
  "price": 48000.0,
  "activo": true
}
```

**Errores:**
- `404` — Producto no encontrado.

---

### PATCH `/productos/product/{id}/toggle-activo`

Activa o desactiva un producto del catálogo.

```json
// Response
{
  "id": 1,
  "name": "Aguardiente Antioqueño",
  "activo": false
}
```

**Errores:**
- `404` — Producto no encontrado.

---

## ✔️ Validaciones

- `cost` y `price` deben ser valores numéricos positivos.
- `name`, `unit` y `category` son campos requeridos al crear un producto.
- Al actualizar (`PUT`), todos los campos son reemplazados — se deben enviar completos.

---

## 👥 Permisos por rol

| Acción | Administrador | Cajero | Mesero |
|--------|---------------|--------|--------|
| Ver productos | ✅ | ✅ | ✅ |
| Crear producto | ✅ | ❌ | ❌ |
| Actualizar producto | ✅ | ❌ | ❌ |
| Activar / Desactivar | ✅ | ❌ | ❌ |

> ⚠️ El control de permisos por rol se gestiona en el frontend. El backend no valida el rol en este microservicio.

---

## 🗄️ Modelos de base de datos

| Tabla | Descripción |
|-------|-------------|
| `products` | Catálogo maestro de productos |

### Script de creación

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    unidad VARCHAR NOT NULL,
    categoria VARCHAR NOT NULL,
    costo NUMERIC NOT NULL,
    precio NUMERIC NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_products_categoria ON products(categoria);
```

---

## 🔗 Relación con otros microservicios

Este microservicio actúa como el **catálogo maestro de referencia** para el resto del sistema. Otros microservicios como **MS-INVENTORY-PY** almacenan únicamente el `product_id` como referencia a este catálogo.

```
MS-PRODUCT-PY    →  id, name, unit, category, cost, price
MS-INVENTORY-PY  →  product_id (referencia), sede_id, stock
```

> Cualquier cambio en nombre, precio o categoría de un producto se refleja automáticamente en todos los microservicios que lo referencian, sin necesidad de sincronización adicional.

---

## 🐳 Correr con Docker

```bash
# Construir imagen
docker build -t eb-products .

# Correr contenedor
docker run -p 8003:8003 --env-file .env eb-products
```

O usar el Docker Compose del repositorio `INFRA-EB-DK`:

```bash
cd INFRA-EB-DK/compose
docker compose up -d products
```

---

## 📖 Documentación automática

FastAPI genera documentación automática disponible en:

- Swagger UI: `http://localhost:8003/docs`
- ReDoc: `http://localhost:8003/redoc`
