lines = "+------------------------------------------------------------------------------------------------------+"
line = "|         |"


class MainPart:
    r"""
    Contains:
    1. welcome_page
    2. main_page
    """

    welcome_page = r"""
            +------  +------  +------+     /\        /    +------
           /        /        /       /    /  \      /    / 
          +----    +----    +-------+    /    \    /    +----
         /        /        /    \       /      \  /    /
        /        +------  /      \__   /        \/    +------
        (!@$ Hello~ I'm Ferne! The developer of this program $@!)
       [^_^$           Please Press Any Key to Start         $^_^]
         {%$                  Have Fun here!                 $%}
  """

    main_page = r"""
  +--------+--------------+
  | Choice |   Function   |
  +--------+--------------+
  |    1   |     Chat     |
  |    2   |   Settings   |
  |    3   |     Info     |
  |    E   |     Exit     |
  +--------+--------------+
  """


class SettingPart:
    r"""
    Contains:
    1. settings_page_main
    2. settings_page_for_ollama_and_other
    3. settings_page_for_spark
    4. settings_if_enter_isTTS
    """

    settings_page_main = r"""
  +--------+-----------+
  | Choice |   Value   |
  +--------+-----------+
  |    1   |   ollama  |
  |    2   |   spark   |
  |    3   |   other   |
  +--------+-----------+
  Hey! Just choose one to enter the setting part!
  """

    settings_page_for_ollama_and_other = r"""
  +--------+-------------+
  | Choice |  Function   |
  +--------+-------------+
  |    1   |   model     |
  |    2   |   isTTS     |
  |    3   |   Prompt    |
  +--------+-------------+
  Hey! These are infos:

  1. model is for you to choose!
    If you use "ollama", then just enter the name of the model in the website: 
    !$["https://ollama.com/library"]$!
    And then the program will download it automatically.

    If you use "other", go to find the support models in the document of that website

  2. isTTS means if you need text to speech,
    default to False.
    If you select True, you may need to wait for a while
    We highly RECCOMMEND FALSE (@_@) Since waiting makes annoyance.

  3. Prompt is used to control the character of the AI.
    For example:
    Input: I'm the confident AI VTuber Neuro-sama

    if you enter the sentence like that, the Agent will think it as Neuro-sama.
    Just let your ideas fly here! (@^_^@)
  """
    settings_if_enter_isTTS = r"""
  +--------+-----------+
  | Choice |   Value   |
  +--------+-----------+
  |    1   |   True    |
  |    2   |   False   |
  +--------+-----------+
  """

    settings_page_for_spark = r"""
  +--------+-------------+
  | Choice |  Function   |
  +--------+-------------+
  |    1   |   model     |
  |    2   |   top_p     |
  +--------+-------------+
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


class InfoPart:
    r"""
    Here is to show my infos.
    """

    end_page = r"""
  +--------+----------------+
  | Choice |  Information   |
  +--------+----------------+
  |    1   |   About Us     |
  |    2   |   Contact      |
  |    3   |   Feedback     |
  +--------+----------------+
  """
