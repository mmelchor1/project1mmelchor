# Distributed Stock Execution Platform
**CS451: Introduction to Parallel and Distributed Computing**

## Project Overview
This project implements a high-throughput **Distributed Automated Stock Trading System** that simulates a real-market environment.It uses a master-worker architecture where a **Market Provider** streams historical asset prices to multiple **Trading Workers** The system is built to demonstrate performance scaling by measuring "tick to action" latency as resources increase from 1 to 4 worker nodes

## Repository Structure
* **`fabric_setup.ipynb`**: The control center (Jupyter Notebook) used to reserve FABRIC nodes, deploy code, and start the experiment using the `fablib` library.
* **`src/MarketStreamer.py`**: A Python service (Node 1) that reads stock data and broadcasts it to workers using ZeroMQ or TCP Sockets.
* **`src/TradingLogic.py`**: Distributed agents running moving average crossover logic to identify "BUY," "SELL," or "HOLD" signals.
* **`src/Telemetry.py`**: A dedicated module that records timestamps to calculate the "tick to action" latency for performance metrics.
* **`data/stocks.csv`**: Historical price data used to mimic a live exchange feed.

## Dependencies
The following Python libraries are required for the implementation:
* **`fablib`**: To manage FABRIC slices, nodes, and SSH authentication.
* **`pandas` & `numpy`**: To handle price data and calculate technical indicators.
* **`zmq`**: For lightweight, high-speed message passing between distributed nodes.
* **`ipywidgets`**: To provide an interactive dashboard in Jupyter for controlling trades.
* **`matplotlib`**: To plot the final performance and scaling results.

## Setup and Execution on FABRIC

### 1. Node Reservation
1. Open `fabric_setup.ipynb` on JupyterHub
2. Execute the cells to reserve a **5-node topology** (1 Market Provider and 4 Trading Workers) on the FABRIC testbed
3. Wait for the slice to reach the "Active" state.

### 2. Deployment
1. Run the configuration cells to install `pip` dependencies on all remote nodes.
2. The notebook will automatically upload the `.py` modules from the `/src` folder to their respective FABRIC nodes

### 3. Running the Experiment
1. **Start the Streamer**: From the Jupyter Notebook or SSH, invoke `MarketStreamer.py` on the master node to begin broadcasting data
2. **Start the Workers**: Invoke `TradingLogic.py` on the worker nodes to begin processing the stream
3. **Monitor Output**: Workers will produce actions based on the input stream in the following format
    * `{"symbol": "AAPL", "price": 150.00}: HOLD`
    * `{"symbol": "TSLA", "price": 210.00}: BUY 10 shares`

## Performance Scaling
The project measures scaling by recording the latency of processing 10 stocks on 1 worker node versus processing 40 stocks across 4 worker nodes. Results are captured by `Telemetry.py` and visualized using `matplotlib` to show how resource scaling affects system throughput