from ._pages import *
from utils import json
from ._chat import ChatWithAI
from abc import ABC, abstractmethod
from utils.colorful import SetColor
from utils.settings import logger
from ._status import PageStatusTransite


frcolor = SetColor.set_frcolor
page_status_transite = PageStatusTransite()


class ForPages(ABC):
	@abstractmethod
	def for_self_part(self):
		pass

	def update_status(
		self, *, available_dict: dict, choice: str, current_page: str
	) -> str:
		r"""
		:params:
																		available_dict: dict
																																		The dictionary that contains the available page status and user action
																		choice: str
																		The choice of the user
																		current_page: str
																		The current page status
		:return:
																		current_page_status: str
		"""
		new_page_status, user_action = available_dict.get(
			choice, [current_page, "Maintain"]
		)

		current_page_status = page_status_transite.transite_to(
			new_page_status, user_action
		)

		return current_page_status


class ForMainPart(ForPages):
	def for_self_part(self):
		r"""Return the current PageStatus [MAINPART]"""
		print(MainPart.main_page)
		choice = input(frcolor(text="\nPlease Enter the Key you want: "))
		current_page_status = self.update_status(
			current_page="MainPart",
			available_dict=MainPart.main_page_avaliable_func,
			choice=choice,
		)
		return current_page_status


class ForChatPart(ForPages):
	def for_self_part(self):
		r"""Return the current PageStatus [CHAT]"""
		try:
			num, model = self._read_conf()
		except:
			print(Chat.chat_page_for_the_first_time)
			num, model = input("Please enter your choice here: ").split(" ")
			self._write_into_conf(choice=num, model=model)

		try:
			ChatWithAI(num, model).chat()
			current_page_status = self.update_status(
				current_page="Chat",
				available_dict=Chat.chat_page_avaliable_func,
				choice=choice,
			)

		except KeyboardInterrupt:
			choice = "B"
			current_page_status = self.update_status(
				current_page="MainPart",
				available_dict=Chat.chat_page_for_backward_func,
				choice=choice,
			)

		return current_page_status

	def _write_into_conf(self, **kwargs) -> None:
		r"""
		kwargs: Give Params with the formation:
																																																																		choice = str
																																																																		model = str
		"""
		# TODO: 第一次使用时将选择和大模型写入文件 之后再通过设置界面更改
		# TODO: 需要对三个方式都保存调用哪个模型
		with open("./config/conf.json", "w") as f:
			json.dump(kwargs, f)

	def _read_conf(self) -> dict:
		# 读取配置文件
		with open("./config/conf.json", "r") as f:
			data = json.load(f)
			return data["choice"], data["model"]


class ForSettingsPart(ForPages):
	# TODO: 这里需要有关于进入到第几个页面的逻辑，方便转出和对应打印哪个页面
	# TODO: 最好加入一个退出所有界面的选项
	# FIXME: 嘶……感觉会相当难维护了……
	Summary_ORM = {
		"settings_page_main": (
			SettingsPart.settings_page_main,
			SettingsPart.settings_page_main_avaliable_func,
		),
		"settings_page_for_choose_API": (
			SettingsPart.settings_page_for_choose_API,
			SettingsPart.settings_page_for_choose_API_avaliable_func,
		),
		"settings_page_for_ollama_and_other": (
			SettingsPart.settings_page_for_ollama_and_other,
			SettingsPart.settings_page_for_ollama_and_other_avaliable_func,
		),  # Parallel
		"settings_page_for_spark": (
			SettingsPart.settings_page_for_spark,
			SettingsPart.settings_page_for_spark_avaliable_func,
		),  # Parallel
		"settings_if_enter_isTTS": (
			SettingsPart.settings_if_enter_isTTS,
			SettingsPart.settings_if_enter_isTTS_avaliable_func,
		),
	}

	choose_page_orm = {
		1: "settings_page_main",
		2: "settings_page_for_choose_API",
		# Here you need to check what did the user entered
		3: (
			"settings_page_for_ollama_and_other",
			"settings_page_for_spark",
		),
		4: "settings_if_enter_isTTS",
	}

	def for_self_part(self):
		r"""Return the current PageStatus [SETTINGS]"""
		current_page_num = 1  # Default to settings_page_main

		while current_page_status == "SettingsPart":

			# read the pagename from choose_page_orm
			should_print_page_name = self.choose_page_orm[current_page_num]

			if isinstance(should_print_page_name, str):
				# We may need to develop a different way to handle the tuple in choose_page_orm[3]
				page_detail, available_dict = self.Summary_ORM[
					should_print_page_name
				]  # XXX: Bugs may happend

			print(page_detail)
			
			choice = input(frcolor(text="\nPlease Enter the Key you want: "))
			
			if choice == "B":
				current_page_num -= 1
			else:
				# At first we decide to check if choose_page_orm[3], and write special logics here
				# But we decide to find a greater way to deal with that problem
				# if should_print_page_name != "settings_page_for_choose_API":
					current_page_num += 1
			

			current_page_status = self.update_status(
				current_page="SettingsPart",
				available_dict=available_dict,  # TODO: Here we need to check which page is in
				choice=choice,
			)
			return current_page_status


class ForInfoPart(ForPages):
	def for_self_part(self):
		r"""Return the current PageStatus [INFOPART]"""

		print(InfoPart.select_page)
		while choice := input(frcolor(text="\nPlease Enter the Key you want: ")):

			if choice != "B":
				print(InfoPart.about_page)
				current_page_status = self.update_status(
					current_page="InfoPart",
					available_dict=InfoPart.info_page_available_func,
					choice=choice,
				)

			else:
				current_page_status = self.update_status(
					current_page="InfoPart",
					available_dict=InfoPart.info_page_available_func,
					choice=choice,
				)

			return current_page_status


class ForExit(ForPages):
	def for_self_part(self):
		r"""Since exited, we don't need PageStatus here"""
		logger.info("Off the program")
		exit()


class HandlePages:

	def start_handle(self) -> None:
		r"""
		Get the function of the particular page and execute it
		"""
		current_page_status = "MainPart"  # Default PageStatus
		page_status_to_func_orm = {  # This is used to transfer the page status to the function, and then we can execute it successfully
			"MainPart": ForMainPart().for_self_part,
			"Chat": ForChatPart().for_self_part,
			"SettingsPart": ForSettingsPart().for_self_part,
			"InfoPart": ForInfoPart().for_self_part,
			"Exit": ForExit().for_self_part,
		}
		while True:
			try:
				current_page_status = page_status_to_func_orm.get(current_page_status)()
			except Exception as e:
				raise e
