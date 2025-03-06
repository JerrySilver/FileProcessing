import yaml

def load_yaml_tags(file_path: str) -> dict:
    """
    读取 YAML 文件，并返回解析后的字典数据
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)



# 在项目启动时加载 YAML 文件内容到全局变量
# 假设 YAML 文件路径为 ../config_table/MarkingRule.yaml
tag_data = load_yaml_tags('config_table/MarkingRule.yaml')

# print("加载的标签数据：", tag_data)
