from typing import List

from ..base.mapping import MappingValue, Mapping


class ElasticMappingValue(MappingValue):
    def _get_values(self, model, prefix) -> List[str]:
        search = model.search().extra(size=0).query('query_string', **{"fields": self.sources, "query": f'*{prefix}*'})
        for source in self.sources:
            search.aggs.bucket(source, "terms", field=source)

        aggs = search.execute().to_dict()["aggregations"]
        result = []
        for source in self.sources:
            if aggs[source]["buckets"]:
                result.extend(
                    [val for val
                     in [str(val["key"]) for val in aggs[source]["buckets"]]
                     if prefix in val]
                )

        return list(set(result))


class ElasticMapping(Mapping):
    _value_class = ElasticMappingValue