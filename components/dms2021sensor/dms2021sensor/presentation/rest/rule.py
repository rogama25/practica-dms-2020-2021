""" Rule class module.
"""

import json
from dms2021core.data.rest import RestResponse
from dms2021sensor.logic import RuleManager
from dms2021sensor.data.db.exc import RuleNotExistsError, RuleExistsError

class Rule():
    """ Class responsible of handling the log-related REST requests.
    """

    def __init__(self, rule_manager: RuleManager):
        """ Constructor method.

        Initializes the user REST interface.
        ---
        Parameters:
            - rule_manager: Instance responsible of the rule logic operations.
        """
        self.__set_rule_manager(rule_manager)

    def get_rule_manager(self) -> RuleManager:
        """ Gets the rule manager object being used by this instance.
        ---
        Returns:
            The user manager instance in use.
        """
        return self.__rule_manager

    def __set_rule_manager(self, rule_manager: RuleManager):
        """ Sets the new user manager object to be used by this instance.
        ---
        Parameters:
            - rule_manager: The new rule manager instance.
        """
        self.__rule_manager = rule_manager

    def get_all_rules(self) -> RestResponse:
        """ Gets all rules.
        ---
        Returns:
            A RestResponse object holding the result of the operation.
        """
        result = self.get_rule_manager().get_all_rules()
        json_content = [str(rule) for rule in result]
        json_response = json.dumps(json_content)
        return RestResponse(json_response, mime_type="application/json")

    def get_rule(self, rule_name: str) -> RestResponse:
        """ Gets a rule.
        ---
        Parameters:
            - rule_name: The rule name.
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            result = self.get_rule_manager().get_rule(rule_name)
            json_response = json.dumps(str(result))
            return RestResponse(json_response, mime_type="application/json")
        except ValueError:
            return RestResponse(code=400, mime_type="text/plain")
        except RuleNotExistsError:
            return RestResponse(code=400, mime_type="text/plain")

    def delete_rule(self, rule_name: str) -> RestResponse:
        """ Deletes a rule.
        ---
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            self.get_rule_manager().delete_rule(rule_name)
        except ValueError:
            return RestResponse(code=400, mime_type="text/plain")
        except RuleNotExistsError:
            return RestResponse(code=404, mime_type="text/plain")
        return RestResponse(mime_type="text/plain")

    def create_rule(self, rule_name:str, rule_type: str, data: str, frequency: int) -> RestResponse:
        """ Creates a rule.
        ---
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            self.get_rule_manager().create_rule(rule_name, rule_type, data, frequency)
        except ValueError:
            return RestResponse(code=400, mime_type="text/plain")
        except RuleExistsError:
            return RestResponse(code=409, mime_type="text/plain")
        return RestResponse(mime_type="text/plain")
