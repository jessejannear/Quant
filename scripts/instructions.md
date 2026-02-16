# Developer Guide

## Project Structure
- `src/`: Source code for the Python client.
- `docs/`: Documentation.
- `theta_terminal/`: Contains the Theta Terminal JAR and credentials.

## Setup Instructions
1.  **Install Java**: Ensure Java 11+ is installed (`java -version`).
2.  **Start Theta Terminal**:
    ```bash
    cd theta_terminal
    java -jar ThetaTerminalv3.jar
    ```
    This must be running in the background for the API to work.
3.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Common Workflows

### Fetching Option Data
1.  **Get Roots**: Call `client.get_roots()` to find available symbols.
2.  **Get Expirations**: Call `client.get_expirations(root)` to find dates.
3.  **Get Strikes**: Call `client.get_strikes(root, expiration)` to find strikes.
4.  **Get Data**: Call `client.get_history(...)` for OHLC data.

## Troubleshooting
- **Connection Failed**: Check if Theta Terminal is running on port 25503.
- **No Data**: Ensure the market is open or you have the correct subscription level.
