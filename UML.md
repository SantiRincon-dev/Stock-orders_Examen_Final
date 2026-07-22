# Diagrama UML

```mermaid
classDiagram
    direction LR

    class Stock {
        -float __price
        +str symbol
        +str company
        +get_price() float
        +set_price(value: float) void
    }

    class Order {
        <<abstract>>
        +str order_id
        +str trader
        +str symbol
        +int quantity
        +float price
        +bool is_cancelled
        #int _seq
        +execute()* str
        +get_summary() str
    }

    class BuyOrder {
        +execute() str
    }

    class SellOrder {
        +execute() str
    }

    class Transaction {
        +BuyOrder buy_order
        +SellOrder sell_order
        +int quantity
        +float price
        +get_summary() str
    }

    class ExchangeEngine {
        -dict _buy_heaps
        -dict _sell_heaps
        -dict _orders_by_id
        -list _transactions
        +place_order(order: Order) void
        +cancel_order(order_id: str) void
        +match_orders() Generator~Transaction~
        +transactions() Generator~Transaction~
    }

    class InvalidPriceError {
        <<Exception>>
    }

    class DuplicateOrderError {
        <<Exception>>
    }

    class OrderNotFoundError {
        <<Exception>>
    }

    Order <|-- BuyOrder
    Order <|-- SellOrder

    Transaction "1" --> "1" BuyOrder
    Transaction "1" --> "1" SellOrder

    ExchangeEngine "1" --> "*" Order
    ExchangeEngine "1" --> "*" Transaction

    Stock ..> InvalidPriceError
    ExchangeEngine ..> DuplicateOrderError
    ExchangeEngine ..> OrderNotFoundError