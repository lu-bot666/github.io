#!/usr/bin/env python3
"""
生成老年人能力评估师能力图谱数据
输出JSONL格式，可导入ontology系统
"""

import json
import uuid
from datetime import datetime

def create_entity(entity_type, properties):
    """创建实体对象"""
    entity_id = f"{entity_type.lower()[:4]}_{uuid.uuid4().hex[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "op": "create",
        "entity": {
            "id": entity_id,
            "type": entity_type,
            "properties": properties,
            "created": now,
            "updated": now
        },
        "timestamp": now
    }

def create_relation(from_id, relation_type, to_id, properties=None):
    """创建关系对象"""
    now = datetime.utcnow().isoformat() + "Z"
    rel = {
        "op": "relate",
        "from": from_id,
        "rel": relation_type,
        "to": to_id,
        "timestamp": now
    }
    if properties:
        rel["properties"] = properties
    return rel

def main():
    entities = []
    relations = []
    
    # 1. 能力框架
    framework = create_entity("CompetencyFramework", {
        "name": "老年人能力评估师职业能力框架",
        "version": "1.0",
        "description": "基于职教1号文要求的老年人能力评估师职业能力图谱，包含知识、技能、素养三个维度",
        "effective_date": "2026-01-01",
        "industry": "养老服务",
        "standard_reference": "职教1号文能力图谱要求"
    })
    framework_id = framework["entity"]["id"]
    entities.append(framework)
    
    # 2. 技能分类
    categories = {
        "knowledge": create_entity("SkillCategory", {
            "name": "专业知识",
            "dimension": "knowledge",
            "description": "老年人能力评估相关理论知识体系",
            "weight": 0.4
        }),
        "skill": create_entity("SkillCategory", {
            "name": "专业技能",
            "dimension": "skill",
            "description": "评估操作、工具使用和实践能力",
            "weight": 0.4
        }),
        "attitude": create_entity("SkillCategory", {
            "name": "职业素养",
            "dimension": "attitude",
            "description": "职业道德、态度和价值观",
            "weight": 0.2
        })
    }
    for cat in categories.values():
        entities.append(cat)
        # 关联分类到框架
        relations.append(create_relation(cat["entity"]["id"], "defined_by_framework", framework_id))
    
    # 3. 熟练度等级（沿用现有等级）
    proficiency_levels = [
        {"name": "初学者", "rank": 1, "description": "基本了解，需要指导和监督"},
        {"name": "有经验者", "rank": 2, "description": "能独立完成常规任务"},
        {"name": "熟练者", "rank": 3, "description": "熟练掌握，能处理复杂情况"},
        {"name": "专家", "rank": 4, "description": "专业领域专家，能创新和改进"},
        {"name": "权威", "rank": 5, "description": "领域权威，能制定标准和培训他人"}
    ]
    prof_ids = []
    for i, level in enumerate(proficiency_levels):
        prof = create_entity("ProficiencyLevel", level)
        entities.append(prof)
        prof_ids.append(prof["entity"]["id"])
    
    # 4. 技能项
    skills = [
        # 专业知识
        {
            "name": "老年人综合评估理论",
            "description": "老年人能力评估的理论框架、模型和方法学",
            "level": "intermediate",
            "training_hours": 60,
            "certification_required": True,
            "category": "knowledge"
        },
        {
            "name": "老年生理学与病理学基础",
            "description": "老年人身体机能变化、常见疾病和健康问题",
            "level": "basic",
            "training_hours": 40,
            "certification_required": False,
            "category": "knowledge"
        },
        {
            "name": "老年心理学与社会学",
            "description": "老年人心理特点、社会适应和心理健康",
            "level": "basic",
            "training_hours": 30,
            "certification_required": False,
            "category": "knowledge"
        },
        # 专业技能
        {
            "name": "ADL日常生活活动评估",
            "description": "使用标准化工具评估老年人日常生活自理能力",
            "level": "intermediate",
            "training_hours": 30,
            "certification_required": True,
            "category": "skill"
        },
        {
            "name": "MMSE简易精神状态检查",
            "description": "评估老年人认知功能和精神状态",
            "level": "intermediate",
            "training_hours": 25,
            "certification_required": True,
            "category": "skill"
        },
        {
            "name": "IADL工具性日常生活活动评估",
            "description": "评估老年人使用工具完成复杂生活活动的能力",
            "level": "intermediate",
            "training_hours": 20,
            "certification_required": True,
            "category": "skill"
        },
        {
            "name": "跌倒风险评估",
            "description": "识别老年人跌倒风险因素并制定预防措施",
            "level": "intermediate",
            "training_hours": 20,
            "certification_required": False,
            "category": "skill"
        },
        {
            "name": "沟通与访谈技巧",
            "description": "与老年人及其家属有效沟通和访谈的能力",
            "level": "advanced",
            "training_hours": 20,
            "certification_required": False,
            "category": "skill"
        },
        {
            "name": "评估报告撰写",
            "description": "规范、准确撰写评估报告的能力",
            "level": "intermediate",
            "training_hours": 30,
            "certification_required": False,
            "category": "skill"
        },
        {
            "name": "个性化照护计划制定",
            "description": "基于评估结果制定个性化照护计划",
            "level": "advanced",
            "training_hours": 50,
            "certification_required": True,
            "category": "skill"
        },
        # 职业素养
        {
            "name": "伦理与隐私保护",
            "description": "遵守职业道德，保护老年人隐私和权益",
            "level": "advanced",
            "training_hours": 15,
            "certification_required": False,
            "category": "attitude"
        },
        {
            "name": "同理心与尊重",
            "description": "对老年人的同理心、尊重和人文关怀",
            "level": "advanced",
            "training_hours": 15,
            "certification_required": False,
            "category": "attitude"
        },
        {
            "name": "客观公正评估",
            "description": "保持客观、公正、无偏见的评估态度",
            "level": "advanced",
            "training_hours": 15,
            "certification_required": False,
            "category": "attitude"
        }
    ]
    
    skill_ids = []
    for skill_data in skills:
        skill = create_entity("Skill", {
            "name": skill_data["name"],
            "description": skill_data["description"],
            "level": skill_data["level"],
            "training_hours": skill_data["training_hours"],
            "certification_required": skill_data["certification_required"]
        })
        skill_id = skill["entity"]["id"]
        entities.append(skill)
        skill_ids.append(skill_id)
        
        # 关联技能到分类
        category_key = skill_data["category"]
        category_id = categories[category_key]["entity"]["id"]
        relations.append(create_relation(skill_id, "belongs_to_category", category_id))
        
        # 关联技能到熟练度等级（每个技能关联到3个等级：基础、目标、高级）
        # 根据技能level决定关联的等级
        level_map = {"basic": 1, "intermediate": 2, "advanced": 3}
        base_level = level_map.get(skill_data["level"], 2)
        for i in range(3):  # 关联3个等级
            prof_index = min(base_level + i - 1, 4)  # 不超过5级
            relations.append(create_relation(skill_id, "has_proficiency", prof_ids[prof_index]))
    
    # 5. 工作角色
    job_role = create_entity("JobRole", {
        "title": "老年人能力评估师",
        "category": "评估服务",
        "description": "负责老年人综合能力评估，制定个性化照护计划，提供专业评估服务",
        "min_experience_years": 2,
        "certification_required": True,
        "qualification_standard": "符合职教1号文能力要求"
    })
    job_role_id = job_role["entity"]["id"]
    entities.append(job_role)
    
    # 6. 角色技能要求
    # 核心技能要求 (必需)
    core_skill_indices = [0, 3, 4, 5, 9]  # 综合评估理论、ADL、MMSE、IADL、个性化计划
    for idx in core_skill_indices:
        relations.append(create_relation(
            job_role_id, 
            "requires_skill", 
            skill_ids[idx],
            {"required_level": "熟练者", "priority": "required"}
        ))
    
    # 重要技能要求 (优先)
    important_skill_indices = [1, 2, 6, 7, 8]  # 生理学、心理学、跌倒风险、沟通、报告撰写
    for idx in important_skill_indices:
        relations.append(create_relation(
            job_role_id,
            "requires_skill",
            skill_ids[idx],
            {"required_level": "有经验者", "priority": "preferred"}
        ))
    
    # 职业素养要求 (必需)
    attitude_skill_indices = [10, 11, 12]  # 伦理、同理心、客观公正
    for idx in attitude_skill_indices:
        relations.append(create_relation(
            job_role_id,
            "requires_skill",
            skill_ids[idx],
            {"required_level": "熟练者", "priority": "required"}
        ))
    
    # 输出JSONL
    output_file = "elderly_assessor_graph.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for entity in entities:
            f.write(json.dumps(entity, ensure_ascii=False) + "\n")
        for relation in relations:
            f.write(json.dumps(relation, ensure_ascii=False) + "\n")
    
    print(f"已生成 {len(entities)} 个实体和 {len(relations)} 条关系")
    print(f"数据已保存到: {output_file}")
    
    # 统计信息
    print("\n=== 老年人能力评估师能力图谱统计 ===")
    print(f"能力框架: 1个")
    print(f"技能分类: 3个 (知识、技能、素养)")
    print(f"熟练度等级: 5级")
    print(f"技能项: {len(skills)}个")
    print(f"工作角色: 1个 (老年人能力评估师)")
    
    # 生成可视化数据摘要
    summary = {
        "framework": framework["entity"]["properties"]["name"],
        "total_nodes": len(entities),
        "total_edges": len(relations),
        "node_types": list(set([e["entity"]["type"] for e in entities])),
        "skill_categories": 3,
        "skills_count": len(skills),
        "proficiency_levels": 5,
        "job_role": job_role["entity"]["properties"]["title"]
    }
    
    summary_file = "elderly_assessor_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"摘要已保存到: {summary_file}")

if __name__ == "__main__":
    main()