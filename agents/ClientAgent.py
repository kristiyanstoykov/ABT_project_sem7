import logging
from mesa import Agent
from models.Product import Product
from models.Opinion import Opinion

logger = logging.getLogger(__name__)

class ClientAgent(Agent):
    def __init__(self, unique_id, model, money, product_to_sell, product_needs):
        super().__init__(unique_id, model)
        self.money = money
        self.product_to_sell = product_to_sell
        self.product_needs = product_needs  # List of Product instances with id, name, and quantity
        self.inventory = []  # List of Product instances the client owns
        self.opinions = {}  # Dict of shop_id -> Opinion instances
        self.opinion_exchange_count = {}

    def replenish_needs(self):
        for need in self.product_needs:
            # Reset quantities to original daily requirements
            if need.product_id == 1:  # Milk
                need.quantity = 5
            elif need.product_id == 2:  # Eggs
                need.quantity = 3
            elif need.product_id == 3:  # Bread
                need.quantity = 4
            elif need.product_id == 4:  # Butter
                need.quantity = 2

    def buy_products(self):
        for need in self.product_needs:
            # Check if the inventory has less than the required quantity
            inventory_item = next((item for item in self.inventory if item.product_id == need.product_id), None)
            if inventory_item and inventory_item.quantity >= need.quantity * 5:
                continue  # Skip buying if we have enough in inventory

            # Determine the quantity to buy (5 to 8 times the needed quantity)
            buy_quantity = self.random.randint(5, 8) * need.quantity

            # Try to buy the product from each shop until successful
            for shop in self.model.shops:
                if shop.sell_product(self, need.product_id, buy_quantity):
                    # Update the client's inventory
                    if inventory_item:
                        inventory_item.quantity += buy_quantity
                    else:
                        self.inventory.append(Product(
                            product_id=need.product_id,
                            name=need.name,
                            quality=0,  # Assuming quality is not tracked for client inventory
                            price=need.price,
                            quantity=buy_quantity
                        ))
                    break  # Stop searching after a successful purchase


    def produce_product(self):
        # Check if all required ingredients are available in the inventory
        for need in self.product_needs:
            inventory_item = next((item for item in self.inventory if item.product_id == need.product_id), None)
            if not inventory_item or inventory_item.quantity < need.quantity:
                logger.info(f"Client {self.unique_id}: Not enough {need.name} to produce product")
                return

        total_cost = 0
        # Deduct ingredients from inventory and calculate total cost
        for need in self.product_needs:
            inventory_item = next((item for item in self.inventory if item.product_id == need.product_id), None)
            inventory_item.adjust_quantity(-need.quantity)
            total_cost += inventory_item.price * need.quantity
            logger.info(f"Client {self.unique_id}: Deducted {need.quantity} of {need.name} from inventory, total cost so far: {total_cost:.2f}")

        # Calculate profit (80-90% of the total cost) and add a surcharge (10-30%)
        profit_margin = self.random.uniform(0.8, 0.9)
        surcharge = self.random.uniform(0.1, 0.3)
        profit = total_cost * profit_margin * (1 + surcharge)
        self.money += profit
        logger.info(f"Client {self.unique_id}: Profit margin: {profit_margin:.2f}, Surcharge: {surcharge:.2f}, Total cost: {total_cost:.2f}")
        logger.info(f"Client {self.unique_id}: Produced product and earned {profit:.2f}")

    def choose_best_shop(self):
        if not self.opinions:
            logger.info(f"Client {self.unique_id}: No opinions yet.")
            return None

        # Find the best shop
        best_shop = max(self.opinions.values(), key=lambda opinion: opinion.get_score())
        if best_shop.get_score() == 0:
            logger.info(f"Client {self.unique_id}: All opinions are neutral, choosing a random shop.")
            return self.random.choice(list(self.opinions.keys()))
        logger.info(f"Client {self.unique_id}: Best shop is {best_shop.shop_id} with score {best_shop.get_score()}")
        return best_shop.shop_id

    def update_opinion(self, shop_id, experience, reason):
        if shop_id not in self.opinions:
            self.opinions[shop_id] = Opinion(shop_id=shop_id, initial_score=0.0)
        self.opinions[shop_id].adjust_score(change=experience, reason=reason)

    def share_opinion(self, other_client):
        for shop_id, opinion in self.opinions.items():
            if shop_id not in other_client.opinions:
                other_client.opinions[shop_id] = Opinion(shop_id=shop_id, initial_score=0.0)
            if other_client.opinions[shop_id].get_score() < opinion.get_score():
                logger.info(f"Client {self.unique_id}: sharing opinion about Shop {shop_id} with Client {other_client.unique_id}")
                other_client.opinions[shop_id].adjust_score(
                    change=0.5, reason="Opinion shared by another client."
                )
                # Track opinion exchange
                if shop_id not in self.opinion_exchange_count:
                    self.opinion_exchange_count[shop_id] = 0
                self.opinion_exchange_count[shop_id] += 1

    def step(self):
        logger.info(f"Client {self.unique_id}: Starting daily step.")

        # Choose a shop and attempt to buy products if needed
        self.buy_products()

        self.produce_product()

        # Share opinions with nearby clients
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        for neighbor in neighbors:
            if isinstance(neighbor, ClientAgent):
                logger.info(f"Client {self.unique_id}: sharing opinions with Client {neighbor.unique_id}")
                self.share_opinion(neighbor)

        # Log the client's money at the end of the day
        logger.info(f"Client {self.unique_id}: Money = {self.money:.2f}")

        logger.info(f"Client {self.unique_id}: Ending daily step.")