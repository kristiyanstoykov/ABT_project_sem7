import logging
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.ClientAgent import ClientAgent
from agents.ShopAgent import ShopAgent
from models.Product import Product
from models.Opinion import Opinion

logger = logging.getLogger(__name__)

class MarketSimulationModel(Model):
    def __init__(self, width, height, num_clients, num_shops):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.day_count = 0

        # Predefined list of products
        predefined_products = [
            Product(product_id=1, name="Milk", quality=8, price=2.5, quantity=0),
            Product(product_id=2, name="Eggs", quality=7, price=3.0, quantity=0),
            Product(product_id=3, name="Bread", quality=6, price=1.5, quantity=0),
            Product(product_id=4, name="Butter", quality=9, price=4.0, quantity=0),
            Product(product_id=5, name="Cheese", quality=7, price=5.0, quantity=0),
        ]

        # Create shops with randomly selected products
        self.shops = []
        for i in range(num_shops):
            shop = ShopAgent(unique_id=i, model=self)
            num_products = self.random.randint(2, 4)  # Each shop has 2 to 4 products
            for product in self.random.sample(predefined_products, num_products):
                shop.add_product(Product(
                    product_id=product.product_id,
                    name=product.name,
                    quality=product.quality,
                    price=product.price,
                    quantity=self.random.randint(10, 50)  # Random initial stock
                ))
            self.shops.append(shop)
            empty_cells = [(x, y) for (x, y) in self.grid.empties]
            if empty_cells:
                random_position = self.random.choice(empty_cells)
                self.grid.place_agent(shop, random_position)
            else:
                raise RuntimeError("No empty cells available for placing the agent.")

        # Create clients with randomly selected product needs
        self.clients = []
        for i in range(num_clients):
            num_needs = self.random.randint(2, 4)  # Each client has 2 to 4 needs
            product_needs = [
                Product(
                    product_id=product.product_id,
                    name=product.name,
                    quality=product.quality,
                    price=product.price,
                    quantity=self.random.randint(1, 5)  # Random daily need
                )
                for product in self.random.sample(predefined_products, num_needs)
            ]
            client = ClientAgent(
                unique_id=i + num_shops,
                model=self,
                money=500,
                product_to_sell="Cookies",
                product_needs=product_needs
            )
            self.clients.append(client)
            self.schedule.add(client)
            empty_cells = [(x, y) for (x, y) in self.grid.empties]
            if empty_cells:
                random_position = self.random.choice(empty_cells)
                self.grid.place_agent(client, random_position)
            else:
                raise RuntimeError("No empty cells available for placing the agent.")

        # Initialize client opinions about all shops
        for client in self.clients:
            for shop in self.shops:
                client.opinions[shop.unique_id] = Opinion(shop_id=shop.unique_id, initial_score=0.0)

    def step(self):
        logger.info(f"\n--- Day {self.day_count + 1} ---")

        # Replenish client needs at the start of each day
        for agent in self.schedule.agents:
            if isinstance(agent, ClientAgent):
                agent.replenish_needs()

        for shop in self.shops:
            shop.restock_products()
            shop.adjust_prices()

        self.schedule.step()
        self.day_count += 1

        # Log daily statistics
        self.log_daily_statistics()

    def log_daily_statistics(self):
        logger.info(f"\n--- Day {self.day_count} ---")
        logger.info("\nShop Statistics:")
        for shop in self.shops:
            total_stock = sum(p.quantity for p in shop.products)
            logger.info(f"Shop {shop.unique_id}: Money = {shop.money:.2f}, Total Stock = {total_stock}")
            for product in shop.products:
                logger.info(f"  {product}")

        logger.info("\nClient Statistics:")
        for agent in self.schedule.agents:
            if isinstance(agent, ClientAgent):
                inventory_summary = ", ".join(
                    f"{p.name}: {p.quantity}" for p in agent.inventory
                ) or "Empty"
                logger.info(f"Client {agent.unique_id}: Money = {agent.money:.2f}, Inventory = {inventory_summary}")

    def print_grid(self):
        grid_str = ""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell_contents = self.grid.get_cell_list_contents([(x, y)])
                if any(isinstance(agent, ShopAgent) for agent in cell_contents):
                    grid_str += "S "
                elif any(isinstance(agent, ClientAgent) for agent in cell_contents):
                    grid_str += "C "
                else:
                    grid_str += ". "
            grid_str += "\n"
        logger.info(f"\nGrid:\n{grid_str}")