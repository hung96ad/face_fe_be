from pydantic import BaseModel
import typing as t
import json


class QueryParams(BaseModel):
    filter: t.Union[str, None] = {}
    range: t.Union[str, None] = []
    sort: t.Union[str, None] = None

    def get_query_params(self, like: str = None) -> t.Tuple[str, int, int, t.Dict, t.List, t.List]:
        value_like: str = None
        skip: int = 0
        limit: int = 10
        filter: t.Dict = {}
        sort: t.List = []
        range: t.List = [0, 9]
        if self.filter:
            filter: t.Dict = json.loads(self.filter)
            if like:
                if like in filter:
                    value_like = filter[like]
                    del filter[like]
        if self.range:
            range = json.loads(self.range)
            skip = range[0]
            limit = range[1] - range[0] + 1
        if self.sort:
            sort = json.loads(self.sort)
        else:
            sort = []
        return value_like, skip, limit, filter, sort, range
