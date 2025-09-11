from dataclasses import dataclass


@dataclass
class Datasources:
    """Container for all data sources"""

    pass

    @staticmethod
    def create_datasources():
        """Factory method to create datasources"""
        return Datasources()
