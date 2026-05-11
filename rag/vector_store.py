"""
向量存储
"""
import os.path
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import chroma_conf
from model.factory import embed_model
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_conf["collection_name"],
            embedding_function = embed_model,
            persist_directory = chroma_conf["persist_directory"],
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_conf["chunk_size"],
            chunk_overlap = chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function = len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs = {"k": chroma_conf["k"]})



    def load_document(self):
        """
        从数据文件夹内容读取数据文件,转为向量存入向量库
        计算md5值去重
        :return:
        """

        def check_md5_hex(md5_for_check:str):
            """
            去重 看看要存入的东西是否处理过
            存放md5值的文件里的文件不存在 那么没有处理过md5 本次的md5也没处理过 就创建这个文件并返回False
            如果存在了 打开存放md5的文件 一行一行读取与 md5_for_check(本次的md5值匹配)如果匹配成果证明处理过返回True 没有成果返回False
            :param md5_for_check:
            :return:
            """
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w",encoding="utf-8").close()
                return False            # 文件不存在 md5没处理过

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r",encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line== md5_for_check:
                        return True     # 处理过
                return False        # 没有处理过

        def save_md5_hex(md5_for_check: str):
            """
            保存md5值
            :param md5_for_check:
            :return:
            """
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a",encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path:str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allow_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )
        for path in allow_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内,跳过")
                continue
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效内容,跳过")
                    continue
                split_document : list[Document] = self.spliter.split_documents(documents)
                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效内容,跳过")
                    continue
                # 存入向量库
                self.vector_store.add_documents(split_document)
                # 保存md5值
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path}内容成功存入知识库")
            except Exception as e:
                # exc_info 为True 会记录详细的报错堆栈,如果为False仅会记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败{str(e)}", exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for i in res:
        print(i.page_content)
        print("="*20)