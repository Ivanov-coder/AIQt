from enum import Enum


class PageStatus(Enum):
    r"""
    For recording the PageStatus

    MAINPART: main page, the default value should be this
    CHAT: chat page
    INSETTING: This state occurs when user writing something they need into the conf file
    SETTINGSPART_FOR_MAIN: "settings_page_main"
    SETTINGSPART_FOR_CHOOSE_API: "settings_page_for_choose_API"
    SETTINGSPART_FOR_OLLAMA_AND_OTHER: "settings_page_for_ollama_and_other"
    SETTINGSPART_FOR_SPARK: "settings_page_for_spark"
    SETTINGSPART_FOR_TTS: "settings_if_enter_isTTS"
    INFOPART: info page
    EXIT: Exit the program
    """

    MAINPART = "MainPart"
    CHAT = "Chat"
    INSETTING = "SettingsPart"  # This state occurs when user writing something they need into the conf file
    SETTINGSPART_FOR_MAIN = "settings_page_main"
    SETTINGSPART_FOR_CHOOSE_API = "settings_page_for_choose_API"
    SETTINGSPART_FOR_OLLAMA_AND_OTHER = "settings_page_for_ollama_and_other"
    SETTINGSPART_FOR_SPARK = "settings_page_for_spark"
    SETTINGSPART_FOR_TTS = "settings_if_enter_isTTS"
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
            # MAINPART
            PageStatus.MAINPART: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.MAINPART,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.CHAT,
                        PageStatus.SETTINGSPART_FOR_MAIN,
                        PageStatus.INFOPART,
                    ]
                },
                {
                    UserAction.BACKWARD: [],
                },
                {
                    UserAction.EXIT: [
                        PageStatus.EXIT,
                    ]
                },
            ],
            # CHAT
            PageStatus.CHAT: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.CHAT,
                    ]
                },
                {
                    UserAction.FORWARD: [],
                },
                {
                    UserAction.BACKWARD: [
                        PageStatus.MAINPART,
                    ]
                },
                {
                    UserAction.EXIT: [],
                },
            ],
            # SETTINGSPART
            PageStatus.SETTINGSPART_FOR_MAIN: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.SETTINGSPART_FOR_MAIN,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.SETTINGSPART_FOR_CHOOSE_API,
                        PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER,
                        PageStatus.SETTINGSPART_FOR_SPARK,
                    ]
                },
                {UserAction.BACKWARD: [PageStatus.MAINPART]},
                {UserAction.EXIT: []},
            ],
            PageStatus.SETTINGSPART_FOR_CHOOSE_API: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.SETTINGSPART_FOR_CHOOSE_API,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER,
                        PageStatus.SETTINGSPART_FOR_SPARK,
                        # HERE FOR NOTHING, SINCE CHOOSING API TO CHAT
                    ]
                },
                {UserAction.BACKWARD: [PageStatus.SETTINGSPART_FOR_MAIN]},
                {UserAction.EXIT: []},
            ],
            PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.INSETTING,
                        PageStatus.SETTINGSPART_FOR_TTS,
                    ]
                },  # TODO: Here may need something
                {
                    UserAction.BACKWARD: [
                        PageStatus.SETTINGSPART_FOR_MAIN,
                        PageStatus.SETTINGSPART_FOR_CHOOSE_API,
                    ]
                },
                {UserAction.EXIT: []},
            ],
            PageStatus.SETTINGSPART_FOR_SPARK: [
                {
                    UserAction.MAINTAIN: [
                        PageStatus.SETTINGSPART_FOR_SPARK,
                    ]
                },
                {
                    UserAction.FORWARD: [
                        PageStatus.INSETTING,
                    ]
                },  # TODO: Here may need something
                {
                    UserAction.BACKWARD: [
                        PageStatus.SETTINGSPART_FOR_MAIN,
                        PageStatus.SETTINGSPART_FOR_CHOOSE_API,
                    ]
                },
                {UserAction.EXIT: []},
            ],
            PageStatus.SETTINGSPART_FOR_TTS: [
                {UserAction.MAINTAIN: [PageStatus.SETTINGSPART_FOR_TTS]},
                {
                    UserAction.FORWARD: [
                        PageStatus.INSETTING,
                    ]
                },  # TODO: Here may need something
                {
                    UserAction.BACKWARD: [
                        PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER,
                    ]
                },
                {UserAction.EXIT: []},
            ],
            # INSETTING
            PageStatus.INSETTING: [
                {UserAction.MAINTAIN: [PageStatus.INSETTING]},
                {
                    UserAction.BACKWARD: [
                        PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER,
                        PageStatus.SETTINGSPART_FOR_SPARK,
                        PageStatus.SETTINGSPART_FOR_TTS,
                        PageStatus.SETTINGSPART_FOR_MAIN # Directly to the initial page
                    ]
                },
                {UserAction.EXIT: []},
            ],
            # INFOPART
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
                {
                    UserAction.BACKWARD: [
                        PageStatus.INFOPART,
                        PageStatus.MAINPART,
                    ]
                },
                {
                    UserAction.EXIT: [],
                },
            ],
            PageStatus.EXIT: {
                UserAction.MAINTAIN: [],
            },
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

    def _can_transite_to(self, new_page_status: str, user_action: str) -> bool:
        r"""
        Check if you can transite to that status
        :param: new_status: You just need to give the name of those Page Classes
        Avaliable Parameters:
            1. MainPart
            2. SettingsPart
            3. Chat
            4. InfoPart
            5. Exit

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

    def transite_to(self, new_page: str, user_action: str) -> str | None:
        r"""
        If can, transite, return the latest value of the Status for you to go ahead.
        If can't, raise InvalidTransition Error.
        """
        if not self._can_transite_to(new_page, user_action):
            raise InvalidTransition(
                f"Cannot transite from {self.current_PageStatus.value} to {new_page} By {user_action}"
            )
        self.current_PageStatus = PageStatus(new_page)
        return self.current_PageStatus.value
