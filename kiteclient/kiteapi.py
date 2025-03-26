import requests
import logging
LOGGER = logging.getLogger()

class KiteApiException(Exception):
    pass

class KiteApp:
    # Products
    PRODUCT_MIS = "MIS"
    PRODUCT_CNC = "CNC"
    PRODUCT_NRML = "NRML"
    PRODUCT_CO = "CO"

    # Order types
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_SLM = "SL-M"
    ORDER_TYPE_SL = "SL"

    # Varities
    VARIETY_REGULAR = "regular"
    VARIETY_CO = "co"
    VARIETY_AMO = "amo"

    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    # Validity
    VALIDITY_DAY = "DAY"
    VALIDITY_IOC = "IOC"

    # Exchanges
    EXCHANGE_NSE = "NSE"
    EXCHANGE_BSE = "BSE"
    EXCHANGE_NFO = "NFO"
    EXCHANGE_CDS = "CDS"
    EXCHANGE_BFO = "BFO"
    EXCHANGE_MCX = "MCX"

    # Margins segments
    MARGIN_EQUITY = "equity"
    MARGIN_COMMODITY = "commodity"

    def __init__(self, enctoken):
        self.headers = {"Authorization": f"enctoken {enctoken}"}
        self.session = requests.session()
        self.root_url = "https://kite.zerodha.com/oms"
        self.session.get(self.root_url, headers=self.headers)

    def quote(self, instruments):
        response = self.session.get(f"{self.root_url}/quote", params={"i": instruments}, headers=self.headers)

        if response.status_code !=200:
            response.raise_for_status()
        
        data = response.json().get("data")
        if not data:
            raise KiteApiException("Quote API Failed")
        return data

    def profile(self):
        response = self.session.get(f"{self.root_url}/user/profile", headers=self.headers)

        if response.status_code !=200:
            response.raise_for_status()
        
        data = response.json().get("data")
        if not data:
            LOGGER.info("Got response %s", response.json())
            raise KiteApiException("Profile API Failed")
        return data

    def ltp(self, instruments):
        response = self.session.get(
            f"{self.root_url}/quote/ltp",
            params={"i": instruments},
            headers=self.headers,
        )

        if response.status_code !=200:
            response.raise_for_status()
        
        data = response.json().get("data")
        if not data:
            LOGGER.info("Got response %s", response.json())
            raise KiteApiException("LTP API Failed")
        return data        

    def margins(self, segment=None):
        if segment:
            response = self.session.get(f"{self.root_url}/user/margins/{segment}", headers=self.headers)
        else:
            response =  self.session.get(f"{self.root_url}/user/margins", headers=self.headers)
        
        if response.status_code !=200:
            response.raise_for_status()
        
        data = response.json().get("data")
        if not data:
            LOGGER.info("Got response %s", response.json())
            raise KiteApiException("Margin API Failed")

    def orders(self):
        response = self.session.get(f"{self.root_url}/orders", headers=self.headers)

        if response.status_code !=200:
            response.raise_for_status()
        
        data = response.json().get("data")
        if not data:
            LOGGER.info("Got response %s", response.json())
            raise KiteApiException("Orders API Failed")

    def positions(self):
        response = self.session.get(f"{self.root_url}/portfolio/positions", headers=self.headers).json()["data"]

        if response.status_code !=200:
            response.raise_for_status()
        
        data = response.json().get("data")
        if not data:
            LOGGER.info("Got response %s", response.json())
            raise KiteApiException("Positions API Failed")

    def place_order(
        self,
        variety,
        exchange,
        tradingsymbol,
        transaction_type,
        quantity,
        product,
        order_type,
        price=None,
        validity=None,
        disclosed_quantity=None,
        trigger_price=None,
        squareoff=None,
        stoploss=None,
        trailing_stoploss=None,
        tag=None,
    ):
        params = locals()
        del params["self"]
        for k in list(params.keys()):
            if params[k] is None:
                del params[k]
        order_status = self.session.post(f"{self.root_url}/orders/{variety}", data=params, headers=self.headers)
        return order_status
        # return order_id

    def modify_order(
        self,
        variety,
        order_id,
        parent_order_id=None,
        quantity=None,
        price=None,
        order_type=None,
        trigger_price=None,
        validity=None,
        disclosed_quantity=None,
    ):
        params = locals()
        del params["self"]
        for k in list(params.keys()):
            if params[k] is None:
                del params[k]

        order_id = self.session.put(
            f"{self.root_url}/orders/{variety}/{order_id}",
            data=params,
            headers=self.headers,
        ).json()["data"]["order_id"]
        return order_id

    def cancel_order(self, variety, order_id, parent_order_id=None):
        order_id = self.session.delete(
            f"{self.root_url}/orders/{variety}/{order_id}",
            data={"parent_order_id": parent_order_id} if parent_order_id else {},
            headers=self.headers,
        ).json()["data"]["order_id"]
        return order_id

    def order_history(self, order_id):
        data = self.session.get(f"{self.root_url}/orders/{order_id}", headers=self.headers).json()["data"]
        return data
