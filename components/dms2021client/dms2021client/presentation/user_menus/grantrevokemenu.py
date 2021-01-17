""" GrantRevokeMenu class module.
"""
from functools import partial
from typing import List, Callable, Tuple
from http.client import HTTPException
from dms2021client.data.rest import AuthService
from dms2021client.presentation.orderedmenu import OrderedMenu
from dms2021client.data.rest.exc import NotFoundError, UnauthorizedError

class GrantRevokeMenu(OrderedMenu):
    """ Grant or revoke rights.
    """

    def __init__(self, session_token: str, auth_service: AuthService, option: int):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - authservice: REST cliente to connect to the authentication service authservice.
        """
        self.__session_token: str = session_token
        self.__authservice: AuthService = auth_service
        self.__option: int = option

    def show_options(self):
        """ Shows options to grant or revoke rights.
        """
        username: str = input("Introduzca el nombre del usuario: ")
        self._returning = False
        while not self._returning:
            rights, functions = self.get_rights(username, self.__option)
            if not rights:
                if self.__option == 1:
                    print("El usuario ya tiene todos los permisos.")
                    return
                print("El usuario no tiene ningún permiso.")
                return
            super().set_title("PERMISOS")
            super().set_items(rights)
            super().set_opt_fuctions(functions)
            try:
                super().show_options()
            except UnauthorizedError:
                print("Usted no tiene permiso para cambiar permisos.")
                self._returning = True
            except NotFoundError:
                print("No se pueden modificar permisos de un usuario inexistente.")
                self._returning = True
            except HTTPException:
                print("Ha ocurrido un error inesperado.")
                self._returning = True
        self._returning = False

    def get_rights(self, username: str, option: int) -> Tuple[List[str], List[Callable]]:
        """ Gets rights of a user (what he has or not depends on the option)
        ---
        Parameters:
            - username: The user name string.
            - option: 1, grant, 2, revoke int.
        Returns:
            - right_result: The rights a user has o not.
            - functions: The functions to execute.
        """
        rights: List[str] = ["AdminRights", "AdminUsers", "AdminRules", "AdminSensors",
        "ViewReports"]
        functions: List[Callable] = []
        right_result: List[str] = []

        for i in rights:
            if self.__authservice.has_right(username, i) and option == 2:
                right_result.append(i)
                fun = partial(self.__authservice.revoke, username, i, self.__session_token)
                functions.append(fun)
            elif not self.__authservice.has_right(username, i) and option == 1:
                right_result.append(i)
                fun = partial(self.__authservice.grant, username, i, self.__session_token)
                functions.append(fun)

        return right_result, functions