""" Log class module.
"""

from datetime import datetime
import json
from sqlalchemy import Table, MetaData, Column, String, DateTime, ForeignKey # type: ignore
from .resultbase import ResultBase

class Log(ResultBase):
    """ Definition and storage of log ORM records.
    """

    def __init__(self, rule_name: str, time: datetime, result: str):
        """ Constructor method.

        Initializes a rule log.
        ---
        Parameters:
            - rule_name: A string with the rule name.
            - time: A string with the time of the log.
            - result: Either a boolean or a string with the result of the log.
        """
        self.rule_name: str = rule_name
        self.time: datetime = time
        self.result: str = result

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.
        ---
        Parameters:
            - metadata: The database schema metadata
        Returns:
            A Table object with the table definition.
        """
        return Table(
            "logs",
            metadata,
            Column("rule_name", String(32), ForeignKey("rules.rule_name", ondelete="CASCADE"), primary_key=True),
            Column("time", DateTime, primary_key=True),
            Column("result", String(8192), nullable=False)
        )

    def __str__(self) -> str:
        """ Gets the object as a string.
        ---
        Returns:
            The object formatted as a json-formatted string.
        """
        return json.dumps({
            "rule_name": self.rule_name,
            "time": self.time.strftime("%d %b %Y %H:%M:%S"),
            "result": self.result
        })
