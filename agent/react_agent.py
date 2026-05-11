from langchain.agents import create_agent

from agent.tools.agent_tools import rag_summarize, get_user_location, get_user_id, fill_context_for_report, \
    fetch_external_data, get_current_month, get_weather
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_user_location, get_user_id,get_weather,
                   get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool,log_before_model,report_prompt_switch],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages"  : [
                {"role": "user","content": query}
            ]
        }
        # context就是上下文runtime中的信息
        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False}):
            lastest_message = chunk["messages"][-1]
            if lastest_message.content:
                yield lastest_message.content.strip() + "\n"


if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成一个使用报告"):
        print(chunk,end="",flush=True)
