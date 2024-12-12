class Product:
    def __init__(self, product_id, name, quality, price, quantity=0):
        self.product_id = product_id
        self.name = name
        self.quality = quality
        self.price = price
        self.quantity = quantity

    def adjust_quantity(self, amount):
        if self.quantity + amount < 0:
            raise ValueError(f"Cannot reduce quantity below 0 for product {self.name}.")
        self.quantity += amount

    def calculate_quality_to_price(self):
        if self.price == 0:
            raise ZeroDivisionError(f"Price for product {self.name} is zero.")
        return self.quality / self.price

    def __str__(self):
        return (f"Product {self.name} (ID: {self.product_id}) - "
                f"Quality: {self.quality}, Price: {self.price}, Quantity: {self.quantity}")
