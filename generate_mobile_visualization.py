#!/usr/bin/env python3
"""
生成移动端可视化HTML文件，将数据嵌入其中
"""

import json
import re

def load_json_data(json_file):
    """加载JSON数据文件"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def embed_data_in_html(template_file, data_file, output_file):
    """将数据嵌入HTML模板"""
    # 加载数据
    graph_data = load_json_data(data_file)
    
    # 加载模板
    with open(template_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 将数据转换为JSON字符串
    data_json = json.dumps(graph_data, ensure_ascii=False)
    
    # 替换占位符
    # 注意：需要处理JSON中的特殊字符，避免破坏HTML
    data_json_escaped = data_json.replace('<', '\\u003c').replace('>', '\\u003e')
    
    html_content = html_content.replace('<%=GRAPH_DATA_JSON%>', data_json_escaped)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已生成移动端可视化文件: {output_file}")
    print(f"节点数: {len(graph_data['nodes'])}，边数: {len(graph_data['links'])}")
    
    return output_file

if __name__ == "__main__":
    template_file = "elderly_assessor_mobile.html"
    data_file = "elderly_assessor_data.json"
    output_file = "elderly_assessor_mobile_final.html"
    
    try:
        embed_data_in_html(template_file, data_file, output_file)
        print("\n✅ 生成成功！")
        print(f"文件位置: /home/lsy/.openclaw/workspace/{output_file}")
        print("\n📱 移动端访问方式:")
        print("1. 下载文件并在手机浏览器中打开")
        print("2. 通过HTTP服务器访问: http://<your-ip>:8080/{output_file}")
        print("3. 上传至飞书文档作为附件")
        
        # 生成简短说明
        with open("elderly_assessor_README.md", "w", encoding="utf-8") as f:
            f.write(f"""# 老年人能力评估师能力图谱 - 移动端可视化

## 文件说明
- `{output_file}` - 移动端可视化主文件（已包含数据）
- `elderly_assessor_data.json` - 原始数据文件
- `elderly_assessor_graph.jsonl` - 原始JSONL图谱数据

## 快速访问
1. **本地打开**: 在手机浏览器中打开 `{output_file}` 文件
2. **HTTP服务器**: 启动Python HTTP服务器:
   ```bash
   python3 -m http.server 8080
   ```
   然后在手机浏览器访问: `http://<电脑IP>:8080/{output_file}`

## 功能特性
- 📱 响应式移动端设计
- 👆 触摸友好的交互: 缩放、拖拽、点击
- 🎨 按类型着色的节点
- 📊 实时统计信息
- ℹ️ 详细节点信息面板
- 🔄 视图重置功能

## 数据统计
- 能力框架: 1个
- 技能分类: 3个 (知识、技能、素养)
- 技能项: {len(graph_data['nodes']) - 1 - 3 - 5 - 1}个
- 熟练度等级: 5级
- 工作角色: 1个 (老年人能力评估师)
- 总节点: {len(graph_data['nodes'])}
- 总关系: {len(graph_data['links'])}

## 技术要求
- 现代浏览器 (Chrome, Safari, Firefox)
- 支持JavaScript
- 建议屏幕宽度 ≥ 320px

## 交互指南
- **双指缩放**: 放大/缩小图谱
- **单指拖拽**: 移动节点位置
- **点击节点**: 查看详细信息
- **底部按钮**: 重置视图、切换标签、显示说明
""")
        print(f"\n📝 说明文档已生成: elderly_assessor_README.md")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()