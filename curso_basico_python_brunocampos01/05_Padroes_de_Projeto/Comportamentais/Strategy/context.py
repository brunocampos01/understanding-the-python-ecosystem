from __future__ import annotations

import os
from abc import ABC, abstractmethod

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

from library.datalake_storage import DataLakeStorage
from library.database.azure_adls import AzureADSL
from library.logger_provider import LoggerProvider


class Context(ABC):
    """
    The Context defines the interface of interest to clients.
    """
    def __init__(self, spark: SparkSession, layer_name: str):
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """
        self.logger = LoggerProvider.get_logger()
        env = os.getenv("Environment")
        self.env = env.lower() if env else "dev"
        self._spark = spark
        self._layer_name = layer_name
        self._strategy = None

    @property
    def spark(self) -> SparkSession:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """
        return self._spark

    @property
    def layer_name(self) -> str:
        return self._layer_name

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    @abstractmethod
    def execute(self) -> None:
        pass

    def do_some_business_logic(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        if self._strategy is None:
            raise RuntimeError("Strategy not set")

        print("Context: Sorting data using the strategy (not sure how it'll do it)")
        result = self._strategy.do_algorithm(["a", "b", "c", "d", "e"])
        print(",".join(result))
