from enum import Enum


class PageStatus(Enum):
    r"""
    Just for recording the PageStatus

    MAINPART: main page, the default value should be this
    CHAT: chat page
    SETTINGSPART: settings page
    INFOPART: info page
    EXIT: Exit the program
    """

    MAINPART = "MainPart"
    CHAT = "Chat"
    SETTINGSPART = "SettingsPart"
    INFOPART = "InfoPart"
    EXIT = "Exit"


class UserAction(Enum):
    r"""
    This is used to record the actions of user

    MAINTAIN: no actions, the default value should be this
    FORWARD: go forward to the next page
    BACKWARD: go back to the previous page
    EXIT: exit the program
    """

    MAINTAIN = "Maintain"
    FORWARD = "Forward"
    BACKWARD = "Backward"
    EXIT = "Exit"


# define an Exception to handle invalid transitions
class InvalidTransition(Exception):
    pass


class PageStatusTransite:
    r"""
    Check if changeable and return the latest PageStatus
    """

    def __init__(self):
        self.current_PageStatus: PageStatus = PageStatus.MAINPART

        self._transite_rules: dict[
            PageStatus : list[dict[UserAction : list[PageStatus]]]
        ] = {
            PageStatus.MAINPART: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.MAINPART,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.SETTINGSPART,
                        PageStatus.INFOPART,
                    ]
                },
                {
                    UserAction.EXIT: [
                        PageStatus.EXIT,
                    ]
                },
            ],
            PageStatus.CHAT: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.CHAT,
                    ]
                },
                {
                    UserAction.BACKWARD: [
                        PageStatus.MAINPART,
                    ]
                },
            ],
            PageStatus.SETTINGSPART: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.SETTINGSPART,
                    ]
                },
                {
                    UserAction.MAINTAIN: [
                        PageStatus.SETTINGSPART,
                    ]
                },
                {
                    UserAction.BACKWARD: [
                        PageStatus.MAINPART,
                        PageStatus.SETTINGSPART,
                    ]
                },
            ],
            PageStatus.INFOPART: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.INFOPART,
                    ]
                },
                {
                    UserAction.MAINTAIN: [
                        PageStatus.INFOPART,
                    ]
                },
                {
                    UserAction.BACKWARD: [
                        PageStatus.INFOPART,
                        PageStatus.MAINPART,
                    ]
                },
            ],
            PageStatus.EXIT: {UserAction.MAINTAIN: []},
        }
        self._user_action_to_num_orm: dict[PageStatus:int] = {
            # It is used to be the index of the list in self._transite_rules
            # And if you add a new UserAction, you should add it here
            # Also, define the list in self._transite_rules by this order
            # Otherwise, it will raise an IndexError :/
            UserAction.MAINTAIN: 0,
            UserAction.FORWARD: 1,
            UserAction.BACKWARD: 2,
            UserAction.EXIT: 3,
        }

    def _can_transite_to(self, new_page_status: str, user_action: str):
        r"""
        Check if you can transite to that status
        :param: new_status: You just need to give the name of those Page Classes
        Avaliable Parameters:
            1. MainPart
            2. SettingsPart
            3. InfoPart
            4. Exit

        :param: new_status:
        Avaliable Parameters:
            1. Maintain
            2. Forward
            3. Backward
            4. Exit
        """

        available_actions_dict_list = self._transite_rules[
            self.current_PageStatus
        ]  # get the list of actions

        orm_idx = self._user_action_to_num_orm[
            UserAction(user_action)
        ]  # get the index to the proper UserAction

        available_transitions = available_actions_dict_list[orm_idx].get(
            UserAction(user_action), []
        )  # get the list of PageStatus, if can't match, return []

        if PageStatus(new_page_status) in available_transitions:
            return True
        else:
            return False

    def transite_to(
        self, new_page: str, user_action: str
    ) -> tuple[str, UserAction] | None:
        r"""
        If can, transite, return the latest value of the Status for you to go ahead.

        You can ignore the returned value [UserAction.MAINTAIN], it's just a placeholder.

        If can't, raise InvalidTransition Error.
        """
        if self._can_transite_to(new_page, user_action):
            self.current_PageStatus = PageStatus(new_page)
            return (
                self.current_PageStatus.value,
                UserAction.MAINTAIN,
            )  # Since user enter the new page, the UserAction should be "MAINTAIN" until he/she do the next action.
        else:
            raise InvalidTransition(
                f"Cannot transite from {self.current_PageStatus.value} to {new_page} By {user_action}"
            )
