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

### Step 1: Market Provider Setup (Master Node)
The Master node acts as the "Source of Truth," streaming stock data to the workers.

1.  **Create the Data Directory:**
    ```bash
    mkdir -p ~/data
    ```
2.  **Initialize the Dataset:** Ensure `stocks.csv` is present in `~/data/`. If creating manually:
    ```bash
    cat <<EOF > ~/data/stocks.csv
    symbol,price,timestamp
    AAPL,150.25,1711860000
    TSLA,180.10,1711860001
    MSFT,405.15,1711860002
    EOF
    ```
3.  **Launch the Streamer:**
    ```bash
    python3 MarketStreamer.py
    ```

### Step 2: Worker Node Setup (Nodes 1-4)
Each worker acts as an independent trading agent. **Repeat these steps on all four worker terminals.**

1.  **Sync Dependencies:**
    ```bash
    pip3 install --user pyzmq pandas numpy
    ```
2.  **Verify Local Modules:** Ensure `Telemetry.py` and `TradingLogic.py` are in the home directory.
3.  **Connect to the Cluster:**
    Replace `<MASTER_IP>` with the internal **FABNET IPv4** address (e.g., `10.130.129.4`).
    ```bash
    python3 TradingLogic.py --master_ip <MASTER_IP>
    ```
## 6. Performance Monitoring
The system tracks the "Time-of-Flight" for each message to analyze network overhead in a distributed environment.
* **Formula:** $Latency = (T_{receipt} - T_{sent}) \times 1000$
* **Target:** Sub-2ms latency for real-time high-frequency trading simulation.

## 🎥 Execution Video
Below is a screen recording demonstrating the synchronized startup of the MarketProvider and the subsequent connection of all four worker nodes.


https://github.com/user-attachments/assets/4734ec5b-1ed0-4af3-a96c-6efacb8e5766



## 📊 Project Outcomes: Test Scenarios

To validate the distributed logic and network resilience, the system was tested against three distinct data profiles. Each test confirms the workers' ability to process independent signals in parallel.

### **Test Input 1: System Connectivity & Baseline (Normal Market)**
* **Data Profile:** Standard prices for AAPL, TSLA, and MSFT within normal trading ranges.
* **Expected Result:** Workers maintain a **NEUTRAL** state.
* **Outcome:** Verified stable system connectivity. All 4 workers successfully subscribed to the Master and correctly identified a `HOLD` strategy based on the initial thresholds.

### **Test Input 2: Upper-Threshold Logic (High Market)**
* **Data Profile:** Artificially inflated prices (e.g., AAPL > $151.00).
* **Expected Result:** Distributed **SELL** signals across all nodes.
* **Outcome:** Verified threshold accuracy. Every worker node independently triggered a `SELL` action simultaneously, demonstrating zero-drop message propagation.

### **Test Input 3: Lower-Threshold Logic (Market Crash)**
* **Data Profile:** Significant price drops (e.g., TSLA < $180.00).
* **Expected Result:** Distributed **BUY** signals across all nodes.
* **Outcome:** Verified data-driven reactivity. The system pivoted from `SELL` to `BUY` signals in real-time as the input stream changed, confirming the reliability of the ZMQ pipeline.

## Documentation PDF
[MelchorMarlenDocumentation.pdf](https://github.com/user-attachments/files/26369326/MelchorMarlenDocumentation.pdf)


