import launch_buy
import launch_sell
from utilities.get_data import Account
from orders.new_order import BUY_ORDER, SELL_ORDER

def main():
    launch_sell.run_algo()
    # launch_buy.run_algo()

    # order = BUY_ORDER('DGDBTC')
    # order.post_order()

    # order = SELL_ORDER('DGDBTC')
    # order.post_order()

if __name__ == '__main__':
    main()
