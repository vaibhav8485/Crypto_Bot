# STD Modules
import json
import logging

# Set Stop Loss
def get_stop_loss(purchase_price, percentage_loss):
    stop_loss_price = purchase_price * (1 - (percentage_loss / 100))
    return int(stop_loss_price)

# Set Target
def get_target(purchase_price, percentage_target):
    target_price = purchase_price * (1 + (percentage_target / 100))
    return int(target_price)

# Automatic Status Change
def auto_status_change(filename, data, crypto_exists, symbol, current_price):
    for data in data.get('data', []):
        if data['symbol'] == symbol and data['status'] == 'manual' and crypto_exists == True:
            update_log_file(filename, symbol, current_price, 'auto')    
        elif data['symbol'] == symbol and data['status'] == 'hold' and crypto_exists == False:
            update_log_file(filename, symbol, 0, 'auto')

# Get Crypto Log Status
def get_status(data, symbol):
    for data in data.get('data', []):
        if data['symbol'] == symbol:
            return data['status']

# Load Log.JSON File
def load_log_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"File '{filename}' contains invalid JSON.")
        return None

# Save Log.JSON File
def save_log_file(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)  # Use indent=2 for pretty formatting (optional)
        # logging.info(f"Successfully saved log file: {filename}")
    except IOError as e:
        logging.error(f"Failed to save log file '{filename}': {e}")

# Update Log.JSON File
def update_log_file(filename, symbol, new_price, new_status):
    data = load_log_file(filename)
    if data:
        found = False
        for item in data.get('data', []):
            if item.get('symbol') == symbol:
                item['buy_price'] = new_price
                item['status'] = new_status
                found = True        
        if found:
            save_log_file(filename, data)
        else:
            logging.warning(f"Symbol '{symbol}' not found in file '{filename}'. No changes made.")
    else:
        logging.error(f"Error: File '{filename}' not found or is empty.")
