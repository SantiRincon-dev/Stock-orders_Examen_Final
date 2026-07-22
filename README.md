# Stock Orders — Motor de Negociación en Bolsa

Stock Orders es un motor de negociación bursátil desarrollado en Python bajo el paradigma de Programación Orientada a Objetos.

El sistema permite registrar órdenes de compra y venta de acciones, administrarlas mediante colas de prioridad y ejecutar transacciones respetando las reglas de prioridad por precio y tiempo de llegada, simulando el funcionamiento básico de un libro de órdenes utilizado en mercados financieros.

Además, incorpora manejo de excepciones propias, cancelación de órdenes pendientes y recorrido perezoso del historial de transacciones mediante generadores.

Proyecto desarrollado como examen final de Programación Orientada a Objetos.

---

# Contenido

- Arquitectura
- Diseño Orientado a Objetos
- Diagrama de clases (UML)
- Cómo ejecutar
- Excepciones propias
- Reglas de negociación
- Autores y aportes

---

# Arquitectura

El proyecto está organizado como un paquete de Python, donde cada módulo posee una responsabilidad específica dentro del sistema.

```text
stock_orders/
├── __init__.py
├── exceptions.py
├── models.py
├── engine.py
main.py
UML.md
```

## Componentes principales

| Archivo | Responsabilidad |
|----------|-----------------|
| `models.py` | Implementa las entidades principales del dominio: acciones (`Stock`), órdenes (`Order`, `BuyOrder`, `SellOrder`) y transacciones (`Transaction`). |
| `engine.py` | Contiene la clase `ExchangeEngine`, encargada de administrar el libro de órdenes mediante colas de prioridad (`heapq`), registrar órdenes, cancelarlas y ejecutar el proceso de emparejamiento. |
| `exceptions.py` | Define las excepciones personalizadas utilizadas durante la validación del sistema. |
| `main.py` | Punto de entrada del proyecto donde se realiza una demostración completa del funcionamiento del sistema. |
| `UML.md` | Contiene el diagrama de clases elaborado en Mermaid. |

---

# Diseño Orientado a Objetos

El proyecto implementa los principales conceptos de Programación Orientada a Objetos.

## Encapsulamiento

La clase `Stock` mantiene el precio como un atributo privado (`__price`), permitiendo acceder y modificar su valor únicamente mediante los métodos `get_price()` y `set_price()`. Esto garantiza la validación del precio antes de modificarlo.

## Abstracción

La clase `Order` está definida como una clase abstracta (`ABC`), proporcionando la estructura común para cualquier tipo de orden e impidiendo su instanciación directa.

## Herencia

Las clases `BuyOrder` y `SellOrder` heredan de `Order`, reutilizando los atributos y comportamiento común definidos por la clase base.

## Polimorfismo

Cada tipo de orden redefine el método `execute()`, proporcionando una implementación específica para órdenes de compra y órdenes de venta.

## Generadores

El motor implementa los métodos `match_orders()` y `transactions()` mediante `yield`, permitiendo recorrer las transacciones de forma perezosa sin almacenarlas previamente en una nueva estructura.

## Colas de prioridad

El libro de órdenes utiliza el módulo `heapq` para mantener automáticamente el orden de prioridad.

- Compras: mayor precio primero.
- Ventas: menor precio primero.
- En igualdad de precio se utiliza el número de secuencia (`_seq`) para conservar el orden de llegada.

---

# Diagrama de clases (UML)

El diseño completo del sistema puede consultarse en el archivo:

**UML.md**

En este archivo se encuentran todas las clases del proyecto, junto con sus atributos, métodos, relaciones, multiplicidades y modificadores de acceso utilizando la sintaxis Mermaid.

---

# Cómo ejecutar

## Requisitos

- Python 3.13 o superior.

El proyecto utiliza únicamente módulos de la biblioteca estándar de Python. Aunque se utiliza el paquete stock_orders desarrollado para este proyecto.

## Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Stock-orders_Examen_Final
git checkout dev
```

## Ejecutar la demostración

```bash
python main.py
```

La demostración incluida en `main.py` muestra:

1. Un emparejamiento exitoso para las acciones de `AAPL`.
2. Órdenes pendientes para `TSLA`.
3. Cancelación de una orden antes de ejecutarse.
4. Registro de una orden duplicada (`DuplicateOrderError`).
5. Intento de asignar un precio inválido (`InvalidPriceError`).
6. Recorrido completo del historial mediante el generador `transactions()`.

---

# Excepciones propias

Las excepciones personalizadas se encuentran definidas en `stock_orders/exceptions.py`.

| Excepción | Descripción |
|-----------|-------------|
| `InvalidPriceError` | Se produce cuando se intenta asignar un precio menor o igual a cero a una acción. |
| `DuplicateOrderError` | Se lanza al intentar registrar una orden cuyo `order_id` ya existe dentro del sistema. |
| `OrderNotFoundError` | Se genera al intentar cancelar una orden inexistente. |

---

# Reglas de negociación

El motor implementa un libro de órdenes simplificado inspirado en el funcionamiento de un mercado bursátil.

Las reglas implementadas son:

- Cada símbolo mantiene un libro de órdenes independiente.
- Las órdenes de compra tienen prioridad por mayor precio.
- Las órdenes de venta tienen prioridad por menor precio.
- Si existen órdenes con el mismo precio, se prioriza aquella que llegó primero.
- Existe un emparejamiento cuando el mejor precio de compra es mayor o igual al mejor precio de venta.
- El precio acordado corresponde a la orden que ya se encontraba esperando dentro del libro.
- Las órdenes canceladas permanecen almacenadas en el heap y son descartadas únicamente cuando llegan al tope de la cola (*lazy deletion*).
- Para este proyecto se asume que las órdenes que hacen match siempre poseen la misma cantidad, por lo que no se implementan ejecuciones parciales.

---

# Autores y aportes

| Integrante | Aporte |
|------------|--------|
| **Maicol Fernando Castro Revelo** | Integración del proyecto, desarrollo de `main.py`, documentación (`README.md`) y diagrama UML. |
| **Nicolás Garzón Peña** | Desarrollo del motor de negociación (`ExchangeEngine`). |
| **Juan Esteban León Martínez** | Implementación de la jerarquía de órdenes (`Order`, `BuyOrder` y `SellOrder`). |
| **Brayan Santiago Rincón Rodríguez** | Desarrollo de modelos (`Stock`, `Transaction`) y excepciones personalizadas. |