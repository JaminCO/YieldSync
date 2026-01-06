import requests
import json

ALCHEMY_API_KEY = "-KJak5aDli5wfcLVuALgu"
base_url = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
etherscan_api_key = "JHKMF9HJENPWW7BDAMNNSQFKGGGM5I69NY"


# Normal transactions → ETH spending behavior.
# 
# Internal transactions → DeFi interactions, contract activity.
# 
# Token transfers → Portfolio composition, token preferences.
# 
# Combined, these give a full picture of user activity, critical for personalization.
# 
# Scoring Mechanism
# 
# Each user can be assigned an activity score:
# 
# High frequency of swaps, multiple token holdings → higher engagement score.
# 
# Frequent failed transactions → lower reliability score.
# 
# Scoring can include weighted factors:
# 
# score = w1*ETH_activity + w2*Token_activity + w3*DeFi_interactions - w4*Failed_tx

def get_token_balances(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [address],
        "id": 42
    }
    response = requests.post(base_url, json=payload)
    result = response.json().get("result", {})
    token_balances = result.get("tokenBalances", [])
    # Filter out zero balances
    non_zero = [token for token in token_balances if token["tokenBalance"] != "0"]
    return non_zero

def get_token_metadata(contract_address):
    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenMetadata",
        "params": [contract_address],
        "id": 1
    }
    response = requests.post(base_url, json=payload)
    return response.json().get("result", {})

def get_token_usdt_price(contract_address):
    url = "https://api.coingecko.com/api/v3/simple/token_price/ethereum"
    params = {
        "contract_addresses": contract_address,
        "vs_currencies": "usdt"
    }
    response = requests.get(url, params=params)
    data = response.json()
    price = data.get(contract_address.lower(), {}).get("usdt", None)
    return price

def get_token_balances_and_metadata(address):
    token_list = []
    tokens = get_token_balances(address)
    print(f"Token balances of {address}:\n")
    for i, token in enumerate(tokens, start=1):
        balance = int(token["tokenBalance"], 16)
        metadata = get_token_metadata(token["contractAddress"])
        decimals = metadata.get("decimals")
        if decimals is None:
            decimals = 18  # fallback to 18 if missing
        name = metadata.get("name", "Unknown")
        symbol = metadata.get("symbol", "")
        human_balance = balance / (10 ** int(decimals))
        contract_address = token["contractAddress"]
        token_list.append({
            "name": name,
            "symbol": symbol,
            "balance": round(human_balance, 2),
            "contract_address": contract_address
        })
    return token_list

def get_wallet_balance(address):
    url = f"https://api.etherscan.io/v2/api"
    params = {
        "chainid": 1,
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": etherscan_api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") == "1":
        wei_balance = int(data["result"])
        eth_balance = wei_balance / 1e18
        # Get ETH price in USD
        price_url = "https://api.coingecko.com/api/v3/simple/price"
        price_params = {"ids": "ethereum", "vs_currencies": "usd"}
        price_response = requests.get(price_url, params=price_params)
        price_data = price_response.json()
        eth_price_usd = price_data.get("ethereum", {}).get("usd", None)
        if eth_price_usd is not None:
            usd_balance = eth_balance * eth_price_usd
            return {
            "wei": wei_balance,
            "eth": eth_balance,
            "usd": usd_balance
            }
        else:
            return {
            "wei": wei_balance,
            "eth": eth_balance,
            "usd": None,
            "error": "Failed to fetch ETH price"
            }
    else:
        return {"error": data.get("message", "Failed to fetch balance")}


def get_wallet_data(address):
    wallet_balance = get_wallet_balance(address)
    token_balances = get_token_balances_and_metadata(address)
    return {
        "wallet_balance": wallet_balance,
        "token_balances": token_balances
    }

from datetime import datetime

ETHERSCAN_API_KEY = etherscan_api_key
BASE_URL = "https://api.etherscan.io/v2/api"

transaction_list = []
token_transfer_list = []
internal_transaction_list = []
limit = 50

def fetch_etherscan_data(address: str, wallet_id: int="test_wallet", chain: str = "ethereum"):
    def get(endpoint, params):
        params.update({"chainid":1, "module": "account", "address": address, "apikey": ETHERSCAN_API_KEY})
        # "offset": limit, "page": 1
        response = requests.get(BASE_URL, params=params)
        return response.json().get("result", [])

    # Fetch normal transactions
    normal_txs = get("txlist", {"action": "txlist", "startblock": 0, "endblock": 99999999, "sort": "desc"})
    for tx in normal_txs[:10]:
        transaction_list.append({
            "wallet_id": wallet_id,
            "chain": chain,
            "tx_hash": tx["hash"],
            "tx_type": "normal",
            "from_address": tx["from"],
            "to_address": tx.get("to"),
            "value": float(tx["value"]) / float(1e18),
            "gas_used": int(tx["gasUsed"]),
            "gas_price": float(tx["gasPrice"]) / float(1e9),
            "timestamp": str(datetime.fromtimestamp(int(tx["timeStamp"]))),
            "input_data": tx.get("input"),
            "is_error": tx["isError"] == "1",
            "internal_tx_count": 0,
            "status": "success" if tx.get("txreceipt_status") == "1" else "failure"
        })


    # Fetch internal transactions
    internal_txs = get("txlistinternal", {"action": "txlistinternal", "startblock": 0, "endblock": 99999999, "sort": "desc"})
    internal_count = {}
    for tx in internal_txs[:10]:
        tx_hash = tx["hash"]
        internal_count[tx_hash] = internal_count.get(tx_hash, 0) + 1
        internal_transaction_list.append({
            "wallet_id": wallet_id,
            "chain": chain,
            "tx_hash": tx_hash,
            "tx_type": "internal",
            "from_address": tx["from"],
            "to_address": tx.get("to"),
            "value": float(tx["value"]) / float(1e18),
            "gas_used": int(tx["gasUsed"]),
            "gas_price": float(tx["gas"]) / float(1e9),  # fallback if gasPrice missing
            "timestamp": str(datetime.fromtimestamp(int(tx["timeStamp"]))),
            "input_data": None,
            "is_error": tx["isError"] == "1",
            "internal_tx_count": internal_count[tx_hash],
            "status": "success" if tx.get("isError") == "0" else "failure"
        })

    # Fetch token transfers
    token_txs = get("tokentx", {"action": "tokentx", "startblock": 0, "endblock": 99999999, "sort": "desc"})
    for tx in token_txs[:10]:
        token_amount = float(tx["value"]) / float(10 ** int(tx["tokenDecimal"]))
        token_transfer_list.append({
            "wallet_id": wallet_id,
            "chain": chain,
            "tx_hash": tx["hash"],
            "token_decimal": tx["tokenDecimal"],
            "token_name": tx["tokenName"],
            "token_address": tx["contractAddress"],
            "token_symbol": tx["tokenSymbol"],
            "from_address": tx["from"],
            "to_address": tx.get("to"),
            "token_amount": token_amount,
            "token_type": "ERC20",  # You can add logic to detect ERC721 if needed
            "timestamp": str(datetime.fromtimestamp(int(tx["timeStamp"])))
        })

    return {
        "transaction_list": transaction_list,
        "internal_transaction_list": internal_transaction_list,
        "token_transfer_list": token_transfer_list
    }

user_address = "0x2908537D5e56F5BCEf80A1Fd7E8Ad3E05971C99E"
print(json.dumps(fetch_etherscan_data(user_address)))


# print("\nFetching wallet data...\n")
# print(get_wallet_data(user_address))


# import requests

# def get_chain_id_chainlist(symbol_or_name):
#     try:
#         response = requests.get("https://chainid.network/chains.json")
#         chains_data = response.json()
        
#         for chain in chains_data:
#             if (
#                 symbol_or_name.lower() == chain.get("chain", "").lower()
#                 or symbol_or_name.lower() == chain.get("nativeCurrency", {}).get("symbol", "").lower()
#                 or symbol_or_name.lower() == chain.get("name", "").lower()
#             ):
#                 return chain["chainId"]
#         return None
        
#     except Exception as e:
#         print(f"Error fetching from ChainList: {e}")
#         return None

# # Usage
# chain_id = get_chain_id_chainlist("BSC")  # Returns 137
# print(chain_id)