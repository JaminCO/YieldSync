import requests

def get_chain_id_chainlist(symbol_or_name):
    try:
        response = requests.get("https://chainid.network/chains.json")
        chains_data = response.json()
        
        for chain in chains_data:
            if (
                symbol_or_name.lower() == chain.get("chain", "").lower()
                or symbol_or_name.lower() == chain.get("nativeCurrency", {}).get("symbol", "").lower()
                or symbol_or_name.lower() == chain.get("name", "").lower()
            ):
                return chain["chainId"]
        return None
        
    except Exception as e:
        print(f"Error fetching from ChainList: {e}")
        return None
