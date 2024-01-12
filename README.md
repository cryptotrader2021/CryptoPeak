# CryptoPeak - Cryptocurrency Price Spike Detector

## Overview

This software is designed to identify price spikes in cryptocurrency within the M1 time frame. It can be utilized on both Windows (download the Zip package for Windows) and Linux (run CryptoPeak.py, keeping all files in the same folder). By adjusting various settings, users can establish an identification range to achieve the best entry point. Whenever a price spike is detected, your PC will emit a sound. If you have enabled the options, you can also receive emails and automatically open the Kucoin webpage, where you can view the cryptocurrency that triggered the spike and you can then decide whether to make the purchase. Additionally, the program can be delegated to execute buy and sell orders on your behalf.

## Requirements
1. You need to have an account on KuCoin
2. You must obtain an API key, API secret, and API passphrase, enable them for spot trading, and secure them by restricting access to only your IP address, which must be a static IP
3. To receive emails, you will need to obtain the App Password provided by Google and associate it with your email address, which you should enter in the corresponding field of the software. Additionally, you can use another email address to receive notifications, or you can use the same address

## Getting Started

1. **Windows:** Download the Zip package for Windows and run CryptoPeak.exe
2. **Linux:** Download all file and keeping in the same folder, run `CryptoPeak.py`

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

Checkboxes for "Browser Open" and "Send Email" activate or deactivate the respective functions. "Browser Open" opens the Kucoin link to view the cryptocurrency that caused the spike, useful when automatic orders are disabled. Caution: Setting a too low Percentage Change may open many web pages and send numerous emails. Exercise caution especially if not using "Symbol to Monitor," which limits the analysis to a specific group of cryptocurrencies. Generally, a Percentage Change value >1% and a Factor value of at least 2 are recommended, especially without using "Symbol to Monitor."

## System Requirements

Linux or Windows operating system, no other specific requirements.

## Contribution
If you find this software helpful and wish to support further developments, you can make a donation via PayPal to the user.

[![PayPal Donation](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?business=cryptotradingkukoin@gmail.com)

Proposals for modifications or improvements upon request are accepted.

## License

MIT license

