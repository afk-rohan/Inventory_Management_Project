class Order:
    def __init__(self, order_id, date, status, fulfilment, sales_channel,
                 ship_service_level, style, sku, category, size, asin,
                 courier_status, qty, amount, ship_city, ship_state,
                 promotion_ids, b2b, fulfilled_by):

        self.order_id = order_id
        self.date = date
        self.status = status
        self.fulfilment = fulfilment
        self.sales_channel = sales_channel
        self.ship_service_level = ship_service_level
        self.style = style
        self.sku = sku
        self.category = category
        self.size = size
        self.asin = asin
        self.courier_status = courier_status
        self.qty = int(qty) if qty else 0
        self.amount = float(amount) if amount else 0.0
        self.ship_city = ship_city
        self.ship_state = ship_state
        self.promotion_ids = promotion_ids
        self.b2b = b2b
        self.fulfilled_by = fulfilled_by

    def __str__(self):
        return f"{self.order_id} | {self.category} | {self.qty} | {self.amount} | {self.status}"
