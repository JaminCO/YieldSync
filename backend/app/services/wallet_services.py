from app.models.models import Wallet, User, Transaction, TokenTransfer, WalletActivityScore
from app.db import get_db
from app.models.schemas import WalletCreate, WalletSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests

load_dotenv()

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
base_url = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")

def create_wallet(db: Session, wallet_data: WalletCreate):
    db_wallet = db.query(Wallet).filter(Wallet.address == wallet_data.address).first()
    if db_wallet:
        raise HTTPException(status_code=400, detail="Wallet already exists")
    wallet = Wallet(**wallet_data.dict())
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet

def delete_wallet(db: Session, wallet: Wallet):
    db.delete(wallet)
    db.commit()
    return {"message": "Wallet deleted successfully"}

def get_wallet_balance_eth(address):
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


def get_wallet_by_address(db: Session, address: str):
    return db.query(Wallet).filter(Wallet.address == address).first()

def wallet_analysis():
    pass


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
