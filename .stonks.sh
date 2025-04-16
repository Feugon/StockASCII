#!/bin/bash

# Arguments:
#   Ticker ($1)

# Make the API call and store JSON into .stonkJSON
curl "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=$1&interval=5min&apikey=$STOCK_API_KEY" -o .stonkJSON 

clear

# Extract close prices into a comma-separated string.
# The paste command joins the output lines with a comma.
prices_str=$(jq -r '."Time Series (5min)" 
    | to_entries 
    | sort_by(.key) 
    | .[] 
    | .value["4. close"]' .stonkJSON | paste -sd "," -)

# Extract times into a comma-separated string.
times_str=$(jq -r '."Time Series (5min)" 
    | to_entries 
    | sort_by(.key) 
    | .[] 
    | .key' .stonkJSON | paste -sd "," -)

# Call the Python script, passing the prices and times strings.
python ASCII_plotter.py "$prices_str" "$times_str"