import asyncio
from bot import send_message
from tinkoff.invest import OrderTrades, OrderDirection
from pickle import loads
from repo import TCSAssetRepo
from tinkoff.invest.utils import quotation_to_decimal
import redis.asyncio as redis
import os
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG
)


def parse_tcs_trade(trades: OrderTrades) -> str:
    repo = TCSAssetRepo()
    ticker = repo[trades.instrument_uid].ticker
    quantity = 0
    total_price = 0
    for trade in trades.trades:
        quantity += trade.quantity
        total_price += quotation_to_decimal(trade.price) * trade.quantity
    if quantity == 0:
        return f'Empty order report received: {trades}'
    exec_price = float(total_price / quantity)
    direction = (
        'SOLD'
        if trades.direction == OrderDirection.ORDER_DIRECTION_SELL
        else 'BOUGHT'
    )
    details = f'{ticker} {direction} {quantity} for {exec_price}'
    return f'TCS order filled: {details}'


async def main():
    await send_message('trade reporter', 'Reporter operational')
    r = redis.from_url(os.getenv('REDIS_TRADES_URL'))
    while True:
        async with r as client:
            _, trades = await client.brpop('tcs_trades')
            trade_report = parse_tcs_trade(loads(trades))
            logging.info(f'trade report received: {trade_report}')
            await send_message('trade reporter', trade_report)


if __name__ == '__main__':
    asyncio.run(main())
