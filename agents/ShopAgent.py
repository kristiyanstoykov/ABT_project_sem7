import logging
from mesa import Agent
from models.Product import Product

logger = logging.getLogger(__name__)

class ShopAgent(Agent):
    def __init__(self, unique_id, model, scam_probability=0.1, initial_money=1000):
        super().__init__(unique_id, model)
        self.money = initial_money
        self.products = []  # List of Product instances available in the shop
        self.scam_probability = scam_probability
        self.sales_log = []  # List of transactions for logging purposes

    def add_product(self, product):
        self.products.append(product)

    def sell_product(self, client, product_id, quantity):
        product = next((p for p in self.products if p.product_id == product_id), None)
        if not product:
            logger.info(f"Shop {self.unique_id}: Product with ID {product_id} not found.")
            return False

        if product.quantity < quantity:
            logger.info(f"Shop {self.unique_id}: Not enough stock for {product.name}. Requested: {quantity}, Available: {product.quantity}")
            return False

        cost = product.price * quantity
        if client.money >= cost:
            logger.info(f"Shop {self.unique_id}: Selling {quantity} of {product.name} to Client {client.unique_id}")
            client.money -= cost
            self.money += cost
            product.adjust_quantity(-quantity)
            self.log_transaction(client, product, quantity, product.price, product.quality, scammed=False)
            return True
        else:
            logger.info(f"Shop {self.unique_id}: Client {client.unique_id} cannot afford {product.name}. Cost: {cost}, Client Money: {client.money}")
            return False

    def restock_products(self):
        for product in self.products:
            if product.quantity <= 25:  # Restock only if quantity is below 20
                restock_quantity = self.random.randint(30, 150)  # Random restock quantity
                restock_cost = restock_quantity * product.price * 0.2  # 20% of the price
                if self.money >= restock_cost:
                    product.adjust_quantity(restock_quantity)
                    self.money -= restock_cost
                    logger.info(f"Shop {self.unique_id}: Restocked {restock_quantity} of {product.name} for {restock_cost:.2f}")
                else:
                    logger.info(f"Shop {self.unique_id}: Not enough money to restock {product.name}")

    def adjust_prices(self):
        for product in self.products:
            # Simple price adjustment logic: higher demand leads to higher prices
            if product.quantity < 20:  # Low stock, increase price
                product.price *= 1.1
            elif product.quantity > 100:  # High stock, decrease price
                product.price *= 0.9
            product.price = round(product.price, 2)
            logger.info(f"Shop {self.unique_id}: Adjusted price of {product.name} to {product.price:.2f}")

    def log_transaction(self, client, product, quantity, price, quality, scammed):
        self.sales_log.append({
            "day": self.model.day_count,
            "client_id": client.unique_id,
            "product_id": product.product_id,
            "quantity": quantity,
            "price": price,
            "quality": quality,
            "scammed": scammed
        })

    def step(self):
        # Adjust prices dynamically based on stock levels
        self.adjust_prices()

        # Restock products
        self.restock_products()

        # Log the shop's money at the end of the day
        logger.info(f"Shop {self.unique_id}: Money = {self.money:.2f}")