#!/usr/bin/env python3
"""
将ontology JSONL格式转换为可视化所需的节点和边格式
"""

import json
import sys

def map_entity_type_to_color(entity_type):
    """根据实体类型映射颜色"""
    color_map = {
        "CompetencyFramework": "#FF6B6B",  # 红色
        "SkillCategory": "#4ECDC4",        # 青色
        "Skill": "#45B7D1",                # 蓝色
        "ProficiencyLevel": "#96CEB4",     # 绿色
        "JobRole": "#FFEAA7",              # 黄色
        "Person": "#DDA0DD",               # 紫色
        "AssessmentRecord": "#98D8C8",     # 浅绿
        "Project": "#F7DC6F",              # 金色
        "Task": "#F8C471",                 # 橙色
    }
    return color_map.get(entity_type, "#95A5A6")  # 默认灰色

def extract_label(properties):
    """从属性中提取标签"""
    if "name" in properties:
        return properties["name"]
    elif "title" in properties:
        return properties["title"]
    elif "description" in properties:
        desc = properties["description"]
        return desc[:30] + "..." if len(desc) > 30 else desc
    else:
        # 使用第一个属性值
        for key, value in properties.items():
            if isinstance(value, str):
                return value[:30]
        return "未命名"

def convert_jsonl_to_visualization(input_file, output_file):
    """转换JSONL文件为可视化数据格式"""
    nodes = []
    links = []
    node_ids = set()
    link_keys = set()
    
    # 读取JSONL文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            try:
                record = json.loads(line)
                op = record.get("op")
                
                if op == "create":
                    entity = record["entity"]
                    entity_id = entity["id"]
                    
                    # 避免重复节点
                    if entity_id in node_ids:
                        continue
                    
                    node_type = entity["type"]
                    properties = entity["properties"]
                    
                    # 创建节点
                    node = {
                        "id": entity_id,
                        "type": node_type,
                        "label": extract_label(properties),
                        "properties": properties,
                        "color": map_entity_type_to_color(node_type),
                        "size": 15  # 默认大小
                    }
                    
                    # 根据类型调整大小
                    if node_type == "CompetencyFramework":
                        node["size"] = 25
                    elif node_type in ["SkillCategory", "JobRole"]:
                        node["size"] = 20
                    elif node_type == "Skill":
                        node["size"] = 18
                    elif node_type == "ProficiencyLevel":
                        node["size"] = 16
                    
                    nodes.append(node)
                    node_ids.add(entity_id)
                    
                elif op == "relate":
                    from_id = record["from"]
                    to_id = record["to"]
                    rel_type = record["rel"]
                    
                    # 检查节点是否存在
                    if from_id not in node_ids or to_id not in node_ids:
                        # 可能节点在之前的记录中定义了，先跳过
                        continue
                    
                    # 避免重复边
                    link_key = f"{from_id}-{to_id}-{rel_type}"
                    if link_key in link_keys:
                        continue
                    
                    # 创建边
                    link = {
                        "source": from_id,
                        "target": to_id,
                        "type": rel_type,
                        "label": rel_type,
                        "properties": record.get("properties", {})
                    }
                    
                    links.append(link)
                    link_keys.add(link_key)
                    
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}, 行: {line}")
                continue
    
    # 构建最终数据结构
    graph_data = {
        "nodes": nodes,
        "links": links,
        "metadata": {
            "node_count": len(nodes),
            "link_count": len(links),
            "node_types": list(set([n["type"] for n in nodes])),
            "link_types": list(set([l["type"] for l in links]))
        }
    }
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成: {len(nodes)} 个节点, {len(links)} 条边")
    print(f"输出文件: {output_file}")
    
    # 打印统计信息
    print("\n=== 统计信息 ===")
    print(f"节点类型: {graph_data['metadata']['node_types']}")
    print(f"边类型: {graph_data['metadata']['link_types']}")
    
    # 按类型统计节点
    type_counts = {}
    for node in nodes:
        node_type = node["type"]
        type_counts[node_type] = type_counts.get(node_type, 0) + 1
    
    print("\n节点类型分布:")
    for node_type, count in type_counts.items():
        print(f"  {node_type}: {count}")
    
    return graph_data

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python convert_jsonl_to_visualization.py <输入jsonl文件> <输出json文件>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        convert_jsonl_to_visualization(input_file, output_file)
    except Exception as e:
        print(f"转换过程中出错: {e}")
        sys.exit(1)