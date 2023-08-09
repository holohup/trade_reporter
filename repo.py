from pickle import loads
import settings

import redis
from tinkoff.invest.schemas import Bond, Currency, Etf, Future, Share

R = redis.Redis.from_url(settings.get('TCS_ASSETS_URL'))


class TCSAssetRepo:
    def __getitem__(self, id_: str) -> Bond | Currency | Etf | Future | Share:
        pickled_asset = R.get(id_.upper())
        R.close()
        if not pickled_asset:
            return None
        return loads(pickled_asset)
