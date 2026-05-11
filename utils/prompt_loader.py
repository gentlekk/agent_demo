from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from utils.config_handler import prompts_conf


def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[main_prompt_path]在yaml中未找到系统提示语配置{str(e)}")
        raise e
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[main_prompt_path]加载系统提示语失败{str(e)}")
        raise e

def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[rag_summarize_prompt_path]在yaml中未找到系统提示语配置{str(e)}")
        raise e
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[rag_summarize_prompt_path]加载RAG总结提示词失败{str(e)}")
        raise e

def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[report_prompt_path]在yaml中未找到系统提示语配置{str(e)}")
        raise e
    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[report_prompt_path]加载系report提示词出错{str(e)}")
        raise e

if __name__ == '__main__':
    print(load_system_prompt())
    print(load_rag_prompt())
    print(load_report_prompt())