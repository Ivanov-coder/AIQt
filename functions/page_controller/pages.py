from .detailed.status import PageStatus, UserAction

# PAGE STATUS HERE
MAIN_PART = PageStatus.MAINPART.value
CHAT_PART = PageStatus.CHAT.value
INFO_PART = PageStatus.INFOPART.value
EXIT_PROGRAM = PageStatus.EXIT.value
INSETTING = PageStatus.INSETTING.value
SETTINGSPART_FOR_MAIN = PageStatus.SETTINGSPART_FOR_MAIN.value
SETTINGSPART_FOR_CHOOSE_API = PageStatus.SETTINGSPART_FOR_CHOOSE_API.value
SETTINGSPART_FOR_OLLAMA_AND_OTHER = PageStatus.SETTINGSPART_FOR_OLLAMA_AND_OTHER.value
SETTINGSPART_FOR_SPARK = PageStatus.SETTINGSPART_FOR_SPARK.value
SETTINGSPART_FOR_TTS = PageStatus.SETTINGSPART_FOR_TTS.value


# USER ACTION HERE
MAINTAIN = UserAction.MAINTAIN.value
FORWARD = UserAction.FORWARD.value
BACKWARD = UserAction.BACKWARD.value
EXIT = UserAction.EXIT.value


class MainPart:
    r"""
    Contains:
    1. welcome_page
    2. main_page => main_page_avaliable_func: dict[str: list[str, str]]
    (The first element in the list is PageStatus, the second element is UserAction)
    """

# XXX: When debugger, Close it
#     welcome_page = r"""
#   (!@$ Hello~ I'm Ferne! The developer of this program $@!)
# [^_^$           Please Press Any Key to Start         $^_^]
#   {%$                  Have Fun here!                 $%}
# 	"""

    main_page = r"""
	+--------+--------------+
	| Choice |   Function   |
	+--------+--------------+
	|    1   |     Chat     |
	|    2   |   Settings   |
	|    3   |     Info     |
	+--------+--------------+
	|    E   |     Exit     |
	+--------+--------------+
	"""
    main_page_avaliable_func: dict[str : list[str, str]] = {
        # The first element in the list is PageStatus, the second element is UserAction
        "1": (CHAT_PART, FORWARD),
        "2": (SETTINGSPART_FOR_MAIN, FORWARD),
        "3": (INFO_PART, FORWARD),
        "E": (EXIT_PROGRAM, EXIT),
    }


class Chat:
    r"""
    Contains:
    1. chat_page => chat_page_avaliable_func: dict[str: list[str, str]]
    """

    chat_page = r"""
		+--------+-----------+
		| Choice |   Value   |
		+--------+-----------+
		|    1   |   ollama  |
		|    2   |   spark   |
		|    3   |   other   |
		+--------+-----------+
		|    B   |  Backward |
		+--------+-----------+
		Hey! I guess you are using the program for the first time.
		It doesn't matter, let me guide you!
		Please enter the app you want to use, and then enter the model you want to use.
		Use Space to split:
		For example:
		1 llama3.1
		"""
    chat_page_avaliable_func: dict[str : list[str, str]] = {
        # The first element in the list is PageStatus, the second element is UserAction
        "M": (CHAT_PART, MAINTAIN),
        "B": (MAIN_PART, BACKWARD),
    }


class SettingsPart:
    r"""
    Contains:
    1. settings_page_main => func
    2. settings_page_for_choose_API => func
    3. settings_page_for_ollama_and_other => func
    4. settings_page_for_spark => func
    5. settings_if_enter_isTTS => func
    """

    r"""
	Workflow:
			=> api => end(Choose application to use)
	main =|
			=> detail => api(Choose aplication to set conf)
	"""

    # TODO: Rewrite all func(dict) with "SettingsPart"

    settings_page_main = r"""
	+--------+-----------+
	| Choice |   Value   |
	+--------+-----------+
	|    1   |    API    |
	|    2   |   Detail  |
	+--------+-----------+
	|    B   |  Backward |
	+--------+-----------+
	Hey! These are infos:
	1. API is for you to choose which one do you want to use:
		Available:
		- ollama: This one requires you to install an APP on PC called "Ollama"
			Website: !$["https://ollama.com/download"]$!.
		- Spark: If you choose this one, you need to enter your API key.
		- Other: If you choose this one, you need to enter the Request URL and API key.

	2. Detail is for you to set the detailed settings of these 3 options above.
	"""

    settings_page_main_avaliable_func = {
        # The first element in the list is PageStatus, the second element is UserAction
        "1": (SETTINGSPART_FOR_CHOOSE_API, FORWARD),
        "2": (SETTINGSPART_FOR_CHOOSE_API, FORWARD),
        "B": (MAIN_PART, BACKWARD),
    }

    settings_page_for_choose_API = r"""
	+--------+-----------+
	| Choice |   Value   |
	+--------+-----------+
	|    1   |   ollama  |
	|    2   |   spark   |
	|    3   |   other   |
	+--------+-----------+
	|    B   |  Backward |
	+--------+-----------+
	Please enter the app you want to use, and then enter the model you want to use.
	Use Space to split:
	For example:
	1 llama3.1
"""

    settings_page_for_choose_API_avaliable_func = {
        # The first element in the list is PageStatus, the second element is UserAction
        "1": (INSETTING, FORWARD),
        "2": (INSETTING, FORWARD),
        "3": (INSETTING, FORWARD),
        "B": (SETTINGSPART_FOR_MAIN, BACKWARD),
    }

    # TODO: 看下能不能把spark的页面和ollama_and_others的页面合并一下
    settings_page_for_spark = r"""
	+--------+------------+
	| Choice |  Function  |
	+--------+------------+
	|    1   |   Model    |
	|    2   |   top_p    |
	+--------+------------+
	|    B   |  Backward  |
	+--------+------------+
	Hey! These are infos:

	1. Model is for you to choose:
	Avaliable: 
		- lite
		- generalv3
		- pro-128k
		- generalv3.5
		- max-32k
		- 4.0Ultra

	2. top_p is used to control the randomness of the response,
		default to 0.7,
		Please enter a number between 0 and 1.

		If you want the Agent give interesting (maybe sometimes ridiculous) 
		ideas, the lower the better!
	"""

    settings_page_for_spark_avaliable_func = {
        # The first element in the list is PageStatus, the second element is UserAction
        "1": (INSETTING, FORWARD),
        "2": (INSETTING, FORWARD),
        "B": (SETTINGSPART_FOR_CHOOSE_API, BACKWARD),
    }

    settings_page_for_ollama_and_other = r"""
	+--------+---------------------+
	| Choice |       Function      |
	+--------+---------------------+
	|    1   |   	  Model        |
	|    2   |   	  isTTS        |
	|    3   |  	  Prompt       |
	+--------+---------------------+
	|    B   |  	 Backward      |
	+--------+---------------------+
	Hey! These are infos:

	1. Model is for you to choose!
		If you use "ollama", then just enter the name of the model in the website: 
		!$["https://ollama.com/library"]$!
		And then the program will download it automatically.

		If you use "other", go to find the support models in the document of that website

	2. isTTS means if you need text to speech,
		default to False.
		If you select True, you may need to wait for a while.
		The program will download some files on your computer when you first use it.
		I highly RECCOMMEND FALSE (@!_!@) IF YOU HAVEN'T CUDA! Since waiting makes annoyance.
		But if you want to have a try, just go ahead.
		And you can choose the voice you like haha. (#^_^#)

	3. Prompt is used to control the character of the AI.
		For example:
		Input: I'm the confident AI VTuber Neuro-sama

		if you enter the sentence like that, the Agent will think it as Neuro-sama.
		Just let your ideas fly here! (@^_^@)
	"""
    # TODO: Finish it, though Model should let user enter words in the terminal
    settings_page_for_ollama_and_other_avaliable_func = {
        # The first element in the list is PageStatus, the second element is UserAction
        "1": (INSETTING, FORWARD),
        "2": (SETTINGSPART_FOR_TTS, FORWARD),
        "3": (INSETTING, FORWARD),
        "B": (SETTINGSPART_FOR_CHOOSE_API, BACKWARD),
    }

    settings_if_enter_isTTS = r"""
	+--------+-----------+
	| Choice |   Value   |
	+--------+-----------+
	|    1   |   True    |
	|    2   |   False   |
	+--------+-----------+
	|    B   |  Backward |
	+--------+-----------+
	"""
    # TODO: Finish it, later write a conf file for code to read
    # And user enter keywords, change the value of the conf file
    settings_if_enter_isTTS_avaliable_func = {
        # The first element in the list is PageStatus, the second element is UserAction
        "1": (INSETTING, FORWARD),
        "2": (INSETTING, FORWARD),
        "B": (SETTINGSPART_FOR_OLLAMA_AND_OTHER, BACKWARD),
    }

    # FIXME: 嘶……感觉会相当难维护了…… 想办法优化
    Summary_ORM = {
        "settings_page_main": (
            settings_page_main,
            settings_page_main_avaliable_func,
        ),
        "settings_page_for_choose_API": (
            settings_page_for_choose_API,
            settings_page_for_choose_API_avaliable_func,
        ),
        "settings_page_for_ollama_and_other": (
            settings_page_for_ollama_and_other,
            settings_page_for_ollama_and_other_avaliable_func,
        ),
        "settings_page_for_spark": (
            settings_page_for_spark,
            settings_page_for_spark_avaliable_func,
        ),
        "settings_if_enter_isTTS": (
            settings_if_enter_isTTS,
            settings_if_enter_isTTS_avaliable_func,
        ),
    }


class InfoPart:
    r"""
    Contains:
    1. select_page
    2. about_page
    3. info_page_availale_func
    """

    select_page = r"""
	+--------+--------------+
	| Choice |  Information |
	+--------+--------------+
	|    1   |   About Us   |
	+--------+--------------+
	|    B   |   Backward   |
	+--------+--------------+
	"""
    about_page = r"""
(!@$ Hello~ I'm Ferne! The developer of this program $@!)
{    Well as you see, this is a project about AI,       }
/       I've been doing it for about 1/4 of a year        /
\ You can use it to know how to use some advanced features about Python \
$                  Such as Enum, Finite Machines                        $
[             *^____^*I'll write detailed comments*^____^*              ]
[            !Welcome to share experience!            ]
"""

    info_page_available_func = {
        "1": (INFO_PART, MAINTAIN),
        "B": (MAIN_PART, BACKWARD),
    }
