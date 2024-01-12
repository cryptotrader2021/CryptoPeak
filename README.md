# CryptoPeak - Cryptocurrency Price Spike Detector

## Overview

This software is designed to identify price spikes in cryptocurrency within the M1 time frame. It can be utilized on both Windows (download the Zip package for Windows) and Linux (run CryptoPeak.py, keeping all files in the same folder). By adjusting various settings, users can establish an identification range to achieve the best entry point.

## Getting Started

1. **Windows:** Download the [Zip package for Windows](#).
2. **Linux:** Run `CryptoPeak.py` while keeping all files in the same folder.

## Usage

After analyzing charts and determining the ideal settings:

1. Set all values according to your analysis.
2. Click on "Start Monitoring" to initiate the program.

The software will record the opening and closing prices of the previous candle for over 1000 cryptocurrencies (unless a specific list is provided), calculating the body size. Afterward, it waits for the specified seconds and downloads the price list again, comparing the percentage increase from the previous closing price. It then compares the previous body size with the current price increase; if the defined conditions are met for a specified number of times (Factor), a sound signal is triggered. Optionally, it can send an email and execute a market buy and limit sell order based on user-set parameters.

Before using the automatic order function, it is strongly recommended to conduct a careful price analysis and select a range of cryptocurrencies that fit the software's methodology. Indiscriminate detection of every peak for every cryptocurrency should be done without automatic orders, evaluating whether to make the purchase each time.

## Mandatory Fields

- **Percentage Change:** The minimum percentage increase that the price must have compared to the previous closing.
- **Seconds:** The time interval after which the price should be downloaded for comparison with the previous closing.
- **"Factor Candle's Body":** The number of times the body of the previous candle can fit in the price range between the previous closing and the intercepted price after the specified seconds.

## Optional Fields

- **Symbol to Monitor:** If you want to monitor a specific set of cryptocurrencies, enter their symbols separated by commas (e.g., BTC, ETH, DOGE, TRX).
- **Max Nr. Order, Order Amount, Profit Percentage:** Fill in only if you want to execute automatic orders; otherwise, leave them empty.

## Email Parameters (Optional)

- **Personal Email:** The address to receive notifications.
- **Google Email:** The email associated with the Google App Password.
- **Google App Password:** The password for sending emails through applications like this.

## Caution

Checkboxes for "Browser Open" and "Send Email" activate or deactivate the respective functions. "Browser Open" opens the Kucoin link to view the cryptocurrency that caused the spike, useful when automatic orders are disabled. Caution: Setting a too low Percentage Change may open many web pages and send numerous emails. Exercise caution, especially if not using "Symbol to Monitor," which limits the analysis to a specific group of cryptocurrencies. Generally, a Percentage Change value >1% and a Factor value of at least 2 are recommended, especially without using "Symbol to Monitor."

