"""
提供模型
"""
from abc import ABC, abstractmethod
from typing import Optional

from langchain_community.embeddings import DashScopeEmbeddings

from utils.config_handler import rag_conf
from langchain_community.chat_models import ChatTongyi
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel


class BaseModelFactory(ABC):        # ABC全称Abstract Base Class（抽象基类） keys 让这个类成为抽象基类 不能直接创建对象 专门用来做 父类 / 规范模板
    """
    模型工厂
    keys 定义一套接口规范：所有模型工厂类，必须实现 generator 方法。
    """
    @abstractmethod     # 把方法变成抽象方法 只有定义、没有实现的方法 keys 子类必须重写实现，不写就报错
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    """
    聊天模型工厂
    """
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return  ChatTongyi(model = rag_conf["chat_model_name"])

class EmbeddingModelFactory(BaseModelFactory):
    """
    嵌入模型工厂
    """
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingModelFactory().generator()