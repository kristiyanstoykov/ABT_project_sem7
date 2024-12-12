# Market Simulation with Agents

A project for simulating a market environment to explore dynamic interactions between agents. Built with the Mesa framework.

## Table of Contents
- [Market Simulation with Agents](#market-simulation-with-agents)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [System Architecture](#system-architecture)
  - [Agents Description](#agents-description)
    - [ShopAgent](#shopagent)
    - [ClientAgent](#clientagent)
  - [Models](#models)
    - [MarketSimulationModel](#marketsimulationmodel)
    - [Product Model](#product-model)
    - [Opinion Model](#opinion-model)
  - [Simulation Workflow](#simulation-workflow)
  - [Results](#results)
  - [Future Improvements](#future-improvements)
  - [Technologies Used](#technologies-used)
  - [Author](#author)

## Introduction
This project simulates a market environment to analyze interactions between two types of agents:
- **ShopAgents**: Represent shops selling products.
- **ClientAgents**: Represent clients purchasing products.

## System Architecture
The system uses the Mesa framework, structured around the `MarketSimulationModel`. The environment is a grid where agents interact using `RandomActivation`. The simulation records and visualizes market dynamics for analysis.

## Agents Description
### ShopAgent
- **Role**: Represents a shop.
- **Attributes**: Inventory, balance, reputation score.
- **Behavior**: Dynamically restocks inventory, adjusts prices based on demand, and incorporates a "cheating probability" for variability.

### ClientAgent
- **Role**: Represents a customer.
- **Attributes**: Budget, inventory, opinions on shops.
- **Behavior**: Buys products based on quality-price ratio, interacts with neighbors to share opinions, and produces goods for profit.

## Models
### MarketSimulationModel
- Initializes the grid and agents.
- Manages daily cycles of simulation.
- Logs and visualizes market dynamics.

### Product Model
Defines attributes such as `ID`, `Name`, `Quality`, `Price`, and `Quantity`.

### Opinion Model
Tracks client opinions on shops, with attributes like `shop_id`, `score`, and `history`.

## Simulation Workflow
1. **Initialization**: Sets up the grid, places agents, and initializes product inventories and budgets.
2. **Daily Steps**:
   - Clients reset daily requirements and buy products.
   - Shops restock and adjust prices.
   - Clients produce goods and exchange opinions.
3. **Data Logging and Visualization**: Logs daily statistics like shop profits and client inventory.

## Results
- Shops dynamically adjust to demand but face challenges with product shortages.
- Most clients achieve profitability, but some struggle due to limited resources.
- The system demonstrates functional and dynamic agent interactions.

## Future Improvements
- Enhance inventory restocking strategies for shops.
- Adjust product supply levels to reduce shortages and improve market balance.

## Technologies Used
- **Mesa Framework**: [Mesa Documentation](https://mesa.readthedocs.io/stable/)
- **Matplotlib**: [Matplotlib Documentation](https://matplotlib.org/stable/index.html)

## Author
- **Kristiyan Stoykov**
  - Specialty: Faculty of Computer Systems and Technologies
  - Faculty Number: 121221086
