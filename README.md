# Stock Orders — Motor de Negociación en Bolsa

Motor de negociación bursátil en Python que permite crear órdenes de compra y
venta, emparejarlas respetando prioridad de precio y luego de tiempo de
llegada (como en una bolsa real), prevenir órdenes duplicadas o precios
inválidos mediante excepciones propias, cancelar órdenes pendientes y exponer
el historial de transacciones de forma perezosa mediante generadores.
Proyecto desarrollado como examen final, en equipo de 4 integrantes.

---
# Contenido
- Arquitectura
- Diagrama de clases (UML)
- Cómo ejecutar
- Excepciones propias
- Reglas de negociación
- Autores y aportes
---
# Arquitectura
El proyecto está organizado como un paquete de Python:
```text
stock_orders/
├── __init__.py
├── exceptions.py     # InvalidPriceError, DuplicateOrderError, OrderNotFoundError
├── models.py          # Stock, Order (ABC), BuyOrder, SellOrder, Transaction
└── engine.py           # ExchangeEngine (colas de prioridad con heapq)
main.py                  # Demostración funcional del flujo completo
UML.md                    # Diagrama de clases (Mermaid)
```
## Componentes principales
| Módulo          | Responsabilidad                                                                                                                                                     |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `exceptions.py` | Excepciones propias del dominio (precio inválido, orden duplicada, orden no encontrada).                                                                            |
| `models.py`     | Modelos de dominio: acciones (`Stock`), órdenes (`Order`, `BuyOrder`, `SellOrder`) y transacciones (`Transaction`).                                                 |
| `engine.py`     | `ExchangeEngine`: administra, por símbolo, dos colas de prioridad (`heapq`) — un max-heap de compras y un min-heap de ventas — y ejecuta el matching entre órdenes. |
| `main.py`       | Punto de entrada (`if __name__ == "__main__":`) con una demo completa del sistema.                                                                                  |
## Diseño orientado a objetos
- __Encapsulamiento:__ el precio de `Stock` es privado (`__price`) y solo se
accede mediante `get_price()` / `set_price(value)`, este último con
validación.
- __Abstracción:__ `Order` es una clase abstracta (`abc.ABC`) — no puede
instanciarse directamente.
- Herencia y polimorfismo: `BuyOrder` y `SellOrder` heredan de `Order` y
redefinen `execute()` con su propio comportamiento.
- __Generadores:__ `match_orders()` y `transactions()` en `ExchangeEngine` son
generadores (`yield`), por lo que no acumulan resultados en memoria antes de
devolverlos.
- __Eliminación perezosa (lazy deletion):__ cancelar una orden solo marca
`is_cancelled = True`; se descarta del heap cuando aparece en el tope
durante el matching, sin reordenar ni buscar activamente.

---
# Diagrama de clases (UML)

---
# Cómo ejecutar
Requiere Python 3.x (no usa dependencias externas, solo librería estándar:
`abc`, `heapq`, `itertools` según aplique).
```bash
git clone <URL-del-repositorio>
cd stock-orders
git checkout dev
python main.py
```
La demo en `main.py` muestra:
1. Una transacción ejecutada por match en `AAPL`.
2. Órdenes de `TSLA` que quedan pendientes por no coincidir en precio.
3. La cancelación de una orden antes de ejecutarse (y su ausencia en las
transacciones finales).
4. El intento de registrar una orden con `order_id` duplicado
(`DuplicateOrderError`).
5. El intento de fijar un precio inválido en un `Stock`
(`InvalidPriceError`).
6. El recorrido perezoso del historial de transacciones con
`transactions()`.

---
# Excepciones propias

Definidas en `stock_orders/exceptions.py`:
Excepción	Se lanza cuando...
`InvalidPriceError`	Se intenta fijar un precio ≤ 0 en `Stock.set_price(value)`.
`DuplicateOrderError`	`ExchangeEngine.place_order(order)` recibe un `order_id` que ya existe.
`OrderNotFoundError`	`ExchangeEngine.cancel_order(order_id)` recibe un `order_id` que no existe.

---
# Reglas de negociación
- Por cada símbolo, `ExchangeEngine` mantiene un max-heap de compras
(mayor precio primero, empatando por orden de llegada) y un min-heap de
ventas (menor precio primero, empatando por orden de llegada), usando
`heapq` con tuplas `(-price, seq, order)` y `(price, seq, order)`
respectivamente.
- Un match ocurre cuando el precio tope de compra ≥ precio tope de venta.
- El precio acordado de la `Transaction` es el de la orden que ya estaba en
el libro (menor `_seq`, es decir, la más antigua de las dos).
- Las órdenes canceladas se descartan silenciosamente si aparecen en el tope
del heap durante el matching.
- Para este examen se asume que las órdenes que hacen match siempre tienen la
misma cantidad (no hay llenado parcial).

---
# Autores y aportes
- Maicol Fernando Castro Revelo
- Nicolás Garzón Peña
- Juan Esteban León Martínez
- Brayan Santiago Rincón Rodríguez