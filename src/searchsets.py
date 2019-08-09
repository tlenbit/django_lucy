from django.utils.decorators import classproperty

from src.fields.django import DjangoSearchField
from src.parser import LuceneToDjangoParserMixin
from src.utils import LuceneSearchError


class BaseSearchSet:
    _field_name_to_search_field_instance = None
    _field_sources = None
    _field_base_class = None

    @classproperty
    def field_name_to_field(cls):
        if cls._field_name_to_search_field_instance is None:
            cls._field_name_to_search_field_instance = {name: _cls
                                                        for name, _cls in cls.__dict__.items()
                                                        if isinstance(_cls, cls._field_base_class)}

        return cls._field_name_to_search_field_instance

    @classproperty
    def field_sources(cls):
        if cls._field_sources is None:
            cls._field_sources = [_cls.get_source(name) for name, _cls in cls.field_name_to_field.items()]
        return cls._field_sources

    @classmethod
    def get_query_for_field(cls, condition):
        if condition.name not in cls.field_name_to_field:
            raise LuceneSearchError()
        return cls.field_name_to_field[condition.name].get_query_by_condition(condition)


class DjangoSearchSet(LuceneToDjangoParserMixin, BaseSearchSet):
    _field_base_class = DjangoSearchField
