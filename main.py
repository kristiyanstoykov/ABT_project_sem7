import logging
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from models.MarketSimulationModel import MarketSimulationModel

# Configure logging
logging.basicConfig(filename='simulation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parameters for the simulation
    GRID_WIDTH = 6
    GRID_HEIGHT = 6
    NUM_CLIENTS = 30
    NUM_SHOPS = 5

    # Clear the simulation.log file
    with open('simulation.log', 'w'):
        pass

    # Initialize the model
    model = MarketSimulationModel(
        width=GRID_WIDTH,
        height=GRID_HEIGHT,
        num_clients=NUM_CLIENTS,
        num_shops=NUM_SHOPS
    )

    # Run the simulation for 365 days
    NUM_DAYS = 100
    for day in range(NUM_DAYS):
        logger.info(f"\n--- Simulating Day {day + 1} ---")
        model.step()
        logger.info(f"--- End of Day {day + 1} ---\n")

    # Generate the heatmap of agent counts
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell_content, (x, y) in model.grid.coord_iter():
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count

    # Plot the grid heatmap in a separate window
    plt.figure()
    g = sns.heatmap(agent_counts, cmap="viridis", annot=True, cbar=False, square=True)
    g.figure.set_size_inches(5, 5)
    g.set(title="Number of agents on each cell of the grid")
    plt.show(block=False)

    # Read the log file and extract data for plotting
    log_file = 'simulation.log'
    shop_profits = {}
    client_money = {}

    with open(log_file, 'r') as file:
        for line in file:
            # Extract shop profits
            shop_match = re.search(r'Shop (\d+): Money = (\d+\.\d+)', line)
            if shop_match:
                shop_id = int(shop_match.group(1))
                money = float(shop_match.group(2))
                if shop_id not in shop_profits:
                    shop_profits[shop_id] = []
                shop_profits[shop_id].append(money)

            # Extract client money
            client_match = re.search(r'Client (\d+): Money = (\d+\.\d+)$', line)
            if client_match:
                client_id = int(client_match.group(1))
                money = float(client_match.group(2))
                if client_id not in client_money:
                    client_money[client_id] = []
                client_money[client_id].append(money)

    # Prepare data for plotting
    plot_data = {
        'shop_profits': shop_profits,
        'client_money': client_money
    }
    plot_titles = {
        'shop_profits': 'Shop Profits Over Time',
        'client_money': 'Client Money Over Time'
    }
    plot_labels = {
        'shop_profits': 'Shop',
        'client_money': 'Client'
    }

    # Create subplots for all data in a separate window
    fig, axs = plt.subplots(len(plot_data), 1, figsize=(10, 5 * len(plot_data)))
    fig.tight_layout(pad=5.0)

    # Plot each dataset in a separate subplot
    for i, (key, data) in enumerate(plot_data.items()):
        ax = axs[i] if len(plot_data) > 1 else axs  # Handle single subplot case
        for entity_id, values in data.items():
            ax.plot(values, label=f'{plot_labels[key]} {entity_id}')
        ax.set_xlabel('Day')
        ax.set_ylabel('Money')
        ax.set_title(plot_titles[key])
        ax.legend()

    # Show all plots
    plt.show(block=False)

    # Keep the plots open
    input("Press Enter to exit and close all plots...")
