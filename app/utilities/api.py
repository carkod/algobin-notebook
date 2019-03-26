class EnumDefinitions:
    def __init__(self):
        self.symbol_status = ("PRE_TRADING","TRADING","POST_TRADING","END_OF_DAY","HALT","AUCTION_MATCH","BREAK")
        self.symbol_type = ("SPOT")
        self.order_status = ("NEW","PARTIALLY_FILLED","FILLED","CANCELED","REJECTED","EXPIRED")
        self.order_types = ("LIMIT","MARKET","STOP_LOSS","STOP_LOSS_LIMIT","TAKE_PROFIT","TAKE_PROFIT_LIMIT","LIMIT_MAKER")
        self.order_side = ("BUY","SELL")
        self.time_in_force = ("GTC","IOC","FOK")
        self.chart_intervals = ("1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1M")
        self.rate_limit_intervals = ("SECOND","MINUTE","DAY")