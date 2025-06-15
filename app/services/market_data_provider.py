from abc import ABC, abstractmethod

class MarketDataProvider(ABC):
    @abstractmethod
    def get_latest_price(self, symbol: str) -> dict:
        """Fetches the latest price for a given symbol."""
        pass

class YahooFinanceProvider(MarketDataProvider):
    def get_latest_price(self, symbol: str) -> dict:
        import yfinance as yf
        try:
            ticker = yf.Ticker(symbol)
            # 'regularMarketPrice' is one of the fields yfinance provides
            price = ticker.info.get('regularMarketPrice')
            if price is None:
                return {"error": f"Could not fetch price for {symbol} from Yahoo Finance."}
            return {
                "symbol": symbol,
                "price": price,
                "provider": "yahoo_finance"
            }
        except Exception as e:
            return {"error": str(e)}

# A simple factory to get the provider instance
def get_provider(provider_name: str) -> MarketDataProvider:
    if provider_name == "yahoo_finance":
        return YahooFinanceProvider()
    # You could add other providers here, e.g., 'alpha_vantage'
    raise ValueError(f"Provider '{provider_name}' not supported.")