import os
from pickle import loads
from typing import Union

import redis
from dotenv import load_dotenv
from tinkoff.invest.schemas import Bond, Currency, Etf, Future, Share

load_dotenv()
R = redis.Redis.from_url(os.getenv('REDIS_URL'))


class TCSAssetRepo:
    def __getitem__(self, id_: str) -> Bond | Currency | Etf | Future | Share:
        pickled_asset = R.get(id_.upper())
        R.close()
        if not pickled_asset:
            return None
        return loads(pickled_asset)
