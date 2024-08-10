# Option Pricing Calculator

This is a Flask web application that calculates option prices and generates graphs based on user input. The application uses the Black-Scholes model to calculate option prices and gamma values.

## Features

- Calculate option prices using the Black-Scholes model.
- Generate gamma vs. strike price graphs.
- Generate option price vs. strike price graphs.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/option-pricing-calculator.git
    cd option-pricing-calculator
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open a web browser and go to `http://127.0.0.1:5000/`.

3. Enter the required information in the form:
    - **Ticker**: The stock ticker symbol.
    - **Expiration date**: The expiration date of the option in `YYYY-MM-DD` format.
    - **Graph type**: Enter `'s'` for a strike graph or `'op'` for an option price graph.

4. Click the "Calculate" button to generate the graph.
