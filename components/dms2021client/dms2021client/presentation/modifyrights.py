""" Modifyrights class module.
"""
from typing import List, Callable, Tuple
from dms2021client.data.rest import AuthService
from dms2021client.presentation.menus import OrderedMenu
from dms2021client.data.rest.exc import NotFoundError, UnauthorizedError
from dms2021client.presentation import PrincipleMenu

class ModifyRights(OrderedMenu):
    """ options or revokes rights.
    """

    def __init__(self, session_token: str, username: str, authservice: AuthService):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - username: The username string.
            - authservice: REST cliente to connect to the authentication service authservice.
        """
        self.__session_token: str = session_token
        self.__username: str = username
        self.__authservice: AuthService = authservice

    def show_options(self) -> None:
        """ Shows options to option or revoke rights.
        """
        super().set_title("MODIFICAR PERMISOS")
        super().set_items(["Añadir permisos", "Eliminar permisos"])
        super().set_opt_fuctions([self.option_rights, self.revoke_rights])
        try:
            super().show_options()
        except UnauthorizedError:
            print("Usted no tiene permiso para cambiar permisos.")
        except NotFoundError:
            print("Error 404. Página no encontrada.")
        except Exception:
            print("Ha ocurrido un error inesperado.")
        PrincipleMenu(self.__session_token, self.__username, self.__authservice).show_options()

    def option_rights(self):
        """ Give rights to a user.
        """
        option: int = 1
        self.modify_rights(option)

    def revoke_rights(self):
        """ Revokes rights to a user.
        """
        option: int = 2
        self.modify_rights(option)

    def modify_rights(self, option):
        """ Modify rights to a user.
        ---
        Parameters:
            - option: 1, grant, 2, revoke int.
        """
        username: str = input("Dime el nombre del usuario: ")
        rights, functions = self.get_rights(username, option)
        if not rights:
            if option == 1:
                print("El usuario ya tiene todos los permisos.")
                return
            print("El usuario no tiene ningún permiso.")
            return
        super().set_title("PERMISOS")
        super().set_items(rights)
        super().set_opt_fuctions(functions)
        super().show_options()

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
                functions.append(self.__authservice.revoke(username, i, self.__session_token))
            else:
                right_result.append(i)
                functions.append(self.__authservice.grant(username, i, self.__session_token))

        return right_result, functions