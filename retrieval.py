from flask import Flask, render_template, request
from datetime import datetime
import numpy as np
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega, rho
import numpy as np
from scipy.stats import norm
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

app = Flask(__name__)

def calculate_T(date):
    newDateForm = datetime.strptime(date, "%Y-%m-%d")
    T = abs((newDateForm - datetime.now())).days / 365.0
    return T

def fetchData(symbol, date):
    ticker = yf.Ticker(symbol)
    S = ticker.info['regularMarketPreviousClose']

    expiration = date
    opts = ticker.option_chain(expiration)

    K_calls = opts.calls['strike']
    sigma_calls = opts.calls['impliedVolatility']
    K_puts = opts.puts['strike']
    sigma_puts = opts.puts['impliedVolatility']

    r = 0.0524

    newDateForm = datetime.strptime(date, "%Y-%m-%d")
    T = abs((newDateForm - datetime.now())).days / 365.0

    return r, S, K_calls, sigma_calls, K_puts, sigma_puts, T

def blackScholes (r, S, K, T, sigma, type="c"):
    d1 = (np.log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    try:
        if type == "c":
            price = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * norm.cdf(d2, 0 ,1)
        elif type == "p":
            price = K * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)
        return price
    except:
        print("Please enter a valid type: 'c' for call, 'p' for put")


def gamma (r, S, K, T, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1, 0, 1) / (S * sigma * np.sqrt(T))
    return gamma

def strikeGraph(r, S, K_calls, sigma_calls, K_puts, sigma_puts, T):
    callGammas = {}
    putGammas = {}
    for i in range(len(K_calls)):
        if(T!=0):
            callGammas[K_calls[i]] = gamma(r, S, K_calls[i], T, sigma_calls[i])
    for i in range(len(K_puts)):
        if(T!=0):
            putGammas[K_puts[i]] = gamma(r, S, K_puts[i], T, sigma_puts[i])
    plot(callGammas, putGammas, "Strike Price ($)")

def optionPriceGraph(r, S, K_calls, sigma_calls, K_puts, sigma_puts, T):
    callGammas = {}
    putGammas = {}
    for i in range(len(K_calls)):
        if(T!=0):
            price = blackScholes(r, S, K_calls[i], T, sigma_calls[i], "c")
            callGammas[price] = gamma(r, S, K_calls[i], T, sigma_calls[i])
    for i in range(len(K_puts)):
        if(T!=0):
            price = blackScholes(r, S, K_puts[i], T, sigma_puts[i], "p")
            putGammas[price] = gamma(r, S, K_puts[i], T, sigma_puts[i])
    plot(callGammas, putGammas, "Option Price ($)")

def plot(callGammas, putGammas, title):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(10, 6))
    plt.bar(callGammas.keys(), callGammas.values(), color='g', label='Calls')
    plt.bar(putGammas.keys(), [-value for value in putGammas.values()], color='r', label='Puts')
    plt.xlabel(title)
    plt.ylabel('Gamma')
    plt.title('Gamma levels vs Strike Price')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{abs(x):.2f}'))
    plt.xlim(min(min(callGammas.keys()), min(putGammas.keys())), max(max(callGammas.keys()), max(putGammas.keys())))
    plt.ylim(-max(max(callGammas.values()), max(putGammas.values())), max(max(callGammas.values()), max(putGammas.values())))
    plt.show()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    ticker = request.form['ticker']
    expiration_date = request.form['date']
    control = request.form['control']
    
    r, S, K_calls, sigma_calls, K_puts, sigma_puts, T = fetchData(ticker, expiration_date)
    
    if control == "s":
        strikeGraph(r, S, K_calls, sigma_calls, K_puts, sigma_puts, T)
    elif control == "op":
        optionPriceGraph(r, S, K_calls, sigma_calls, K_puts, sigma_puts, T)
    
    return render_template('output.html')

if __name__ == "__main__":
    app.run(debug=True)
    # inp = (input("Enter ticker and expiration date (YYYY-MM-DD), (SPY 2023-01-01): "))
    # ticker, expiration_date = inp.split()
    # r, S, K_calls, sigma_calls, K_puts, sigma_puts, T = fetchData(ticker, expiration_date)

    # control = input("Enter 's' for strike graph, 'op' for option price graph: ")
    # if control == "s":
    #     strikeGraph(r, S, K_calls, sigma_calls, K_puts, sigma_puts, T)
    # elif control == "op":
    #     optionPriceGraph(r, S, K_calls, sigma_calls, K_puts, sigma_puts, T)