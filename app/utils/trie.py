import logging

# 假设 logger 已经配置好
logger = logging.getLogger(__name__)
from app.utils.yaml_loader import tag_data  # 读取 YAML 的 tag_data


###########################
# Trie 树实现及预处理代码
###########################

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.word = word

    def search_in_text(self, text: str):
        """
        在文本中查找所有匹配的关键词，返回一个列表，列表元素为 (index, matched_word)。
        """
        matches = []
        for i in range(len(text)):
            node = self.root
            j = i
            while j < len(text) and text[j] in node.children:
                node = node.children[text[j]]
                if node.is_end:
                    matches.append((i, node.word))
                j += 1
        return matches


def build_trie_from_yaml_rules(tag_data: dict):
    """
    根据 YAML 规则构造 Trie 树，并生成二级关键词到一级标签的映射字典。
    返回 (trie, keyword_to_primary)。
    """
    trie = Trie()
    keyword_to_primary = {}
    for primary, secondary_list in tag_data.items():
        if secondary_list:
            for secondary in secondary_list:
                trie.insert(secondary)
                # 如果同一二级关键词出现在多个一级标签中，这里以最后一次出现为准
                keyword_to_primary[secondary] = primary
    return trie, keyword_to_primary


# 构建全局 Trie 树和映射字典
trie, keyword_to_primary = build_trie_from_yaml_rules(tag_data)