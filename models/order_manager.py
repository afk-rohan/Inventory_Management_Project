import csv
from models.order import Order

class OrderManager:
    def __init__(self):
        self.orders = []

    def load_data(self, file_path):
        with open(file_path, newline='', encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader)
            headers = next(reader)
            headers = [h.strip() for h in headers]

            for row in reader:
                try:
                    data = dict(zip(headers, row))
                    order = Order(
                        data.get("Order ID", ""),
                        data.get("Date", ""),
                        data.get("Status", ""),
                        data.get("Fulfilment", ""),
                        data.get("Sales Channel", ""),
                        data.get("ship-service-level", ""),
                        data.get("Style", ""),
                        data.get("SKU", ""),
                        data.get("Category", ""),
                        data.get("Size", ""),
                        data.get("ASIN", ""),
                        data.get("Courier Status", ""),
                        data.get("Qty", "0"),
                        data.get("Amount", "0"),
                        data.get("ship-city", ""),
                        data.get("ship-state", ""),
                        data.get("promotion-ids", ""),
                        data.get("B2B", ""),
                        data.get("fulfilled-by", "")
                    )
                    self.orders.append(order)
                except:
                    continue

    def search_by_status(self, keyword):
        return [o for o in self.orders if keyword.lower() in o.status.lower()]

    def top_n_by_amount(self, n):
        totals = {}
        for o in self.orders:
            if o.sku:
                totals[o.sku] = totals.get(o.sku, 0) + o.amount
        items = list(totals.items())
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:n]

    def sales_by_city(self, city):
        return sum(o.amount for o in self.orders if o.ship_city.lower() == city.lower())

    def category_performance(self):
        result = {}
        for o in self.orders:
            if o.category not in result:
                result[o.category] = {"amount": 0, "qty": 0}
            result[o.category]["amount"] += o.amount
            result[o.category]["qty"] += o.qty
        return result

    def clv(self):
        clv_data = {}
        for o in self.orders:
            clv_data[o.order_id] = clv_data.get(o.order_id, 0) + o.amount
        return clv_data
