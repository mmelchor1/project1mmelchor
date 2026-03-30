# Distributed Stock Execution Platform
**CS451: Introduction to Parallel and Distributed Computing - Spring 2026**

## 1. Project Overview
This project implements a high-throughput **Distributed Automated Stock Trading System** designed to simulate a real-market environment. Using a master-worker architecture, the system streams historical asset prices from a central provider to multiple distributed agents that execute trading logic in parallel. 

The primary goal of this initial update is to demonstrate a functional 5-node topology on the FABRIC testbed and establish the communication pipeline for performance scaling analysis.

## 2. System Architecture & Topology
The project utilizes a **5-node setup** to measure distributed performance:
* **Market Provider (1 Node):** Acts as the data source, streaming stock ticks via ZeroMQ.
* **Trading Workers (4 Nodes):** Distributed agents that subscribe to the market feed and calculate technical indicators.
* **Control Center:** Managed via JupyterHub using the `fablib` library for orchestration.



## 3. Implementation Modules
The project is structured into the following functional modules located in the `/src` directory:
* **`FabricManager.py`**: Handles slice reservation, SSH authentication, and automated script deployment to FABRIC nodes.
* **`MarketStreamer.py`**: Reads historical data from `data/stocks.csv` and broadcasts JSON payloads to all active workers.
* **`TradingLogic.py`**: Implements a moving average crossover algorithm to generate `BUY`, `SELL`, or `HOLD` signals.
* **`Telemetry.py`**: Captures "tick to action" latency by comparing timestamps between data transmission and signal generation.

## 4. Dependencies
To run this project on FABRIC, the following Python libraries are required:
* `fablib`: FABRIC testbed management.
* `pyzmq`: High-speed asynchronous messaging.
* `pandas` & `numpy`: Data manipulation and technical analysis.
* `matplotlib`: Visualization of scaling performance.

## 5. Usage Instructions

### Step 1: Environment Setup
1. Upload `fabric_setup.ipynb` to your JupyterHub instance.
2. Ensure your FABRIC credentials (`fabric_config.json`) are configured in your environment.

### Step 2: Deployment
1. Run the cells in `fabric_setup.ipynb` to reserve the 5-node slice.
2. The notebook will automatically install dependencies and push the `src/` modules to the respective remote nodes.

### Step 3: Execution
1. **Start the Provider:** Access the MarketProvider node and run:
   ```bash
   python3 MarketStreamer.py
