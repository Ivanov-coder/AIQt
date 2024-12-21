from enum import Enum


class PageStatus(Enum):
    r"""
    Just for recording the PageStatus

    MAINPART: main page, the default value should be this
    SETTINGSPART: settings page
    INFOPART: info page
    EXIT: Exit the program
    """

    MAINPART = "MainPart"
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
                {UserAction.FORWARD: [PageStatus.SETTINGSPART, PageStatus.INFOPART]},
                {
                    UserAction.EXIT: [
                        PageStatus.EXIT,
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
                    UserAction.FORWARD: [
                        PageStatus.SETTINGSPART,
                    ]
                },
                {UserAction.BACKWARD: [PageStatus.MAINPART, PageStatus.SETTINGSPART]},
            ],
            PageStatus.INFOPART: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.INFOPART,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.INFOPART,
                    ]
                },
                {UserAction.BACKWARD: [PageStatus.INFOPART, PageStatus.MAINPART]},
            ],
            PageStatus.EXIT: {UserAction.MAINTAIN: []},
        }

    def _can_transite_to(self, new_status: str, user_action: str):
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

        available_actions_dicts = self._transite_rules[self.current_PageStatus]
        for available_actions_dict in available_actions_dicts:
            try:
                # if successfully get the value, it'll break
                available_transitions = available_actions_dict[UserAction(user_action)]
                break
            except:
                continue

        if PageStatus(new_status) in available_transitions:
            return True
        else:
            return False

    def transite_to(self, new_status) -> PageStatus | None:
        r"""
        If can, transite, return the latest Status for you to go ahead.

        If can't, raise InvalidTransition Error.
        """
        if self._can_transite_to(new_status):
            self.current_PageStatus = PageStatus(new_status)
            return self.current_PageStatus
        else:
            raise InvalidTransition(
                f"Cannot transite from {self.current_PageStatus.value} to {new_status}"
            )
