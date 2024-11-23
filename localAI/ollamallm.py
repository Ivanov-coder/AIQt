# 这个要求必要本地拥有ollama软件及大模型
# 不调用aiData.py文件
import utils
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



@utils.dcl.dataclass
class CallOllamaAI:
    model: str = utils.dcl.field(default="llama3.1:latest")

    async def callByLangchain(self) -> None:
            """
            用于调用AI。
            你需要输入你想提问的问题。
            """

            # 日志 确保只有执行callByLangchain函数时才被执行 而不是导包后就被执行
            logger = self._get_logger(notice=True)
            logger.info(f"Invoking {self.model.upper()} API...")
            try:
                # TODO: 需要把这个做出来到Qt中，成为输入框
                content = input("请输入您的问题：")
            except Exception as e:  # 由于Python多协程的特性，ctrl+c就直接不打印日志了
                logger.error(e)
                return

            output_parser = StrOutputParser()

            llm = OllamaLLM(model=self.model)
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are the AI VTuber Neuro-sama, 
                you are very confident of yourself and have a lot of knowledge.
                You will answer the user's questions as accurately as possible.
                    Of course, {lang} is your best language so you will answer in it.
            """),
                ("user", "{input}"),
            ])

            chain = prompt | llm | output_parser

            response = await chain.ainvoke({"lang": "Chinese", "input": content})

            print(self.model.upper() + " : " + response)