# https://levelup.gitconnected.com/design-patterns-in-python-strategy-pattern-2189c540756d
# context -> knows the strategy
# generate_catalog_strategy
# generate_catalog_bronze
# generate_catalog_bronze
# generate_catalog_bronze

from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    @abstractmethod
    def execute(self, df_origin: DataFrame, table_name: str) -> DataFrame:
        pass
