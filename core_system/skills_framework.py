#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多技能框架系统
支持动态加载和执行各种技能包
"""

import os
import json
import importlib.util
import inspect
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod


class Skill(ABC):
    """技能基类"""
    
    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.enabled = True
        self.last_executed = None
        self.execution_count = 0
    
    @abstractmethod
    def execute(self, input_data: Any, context: Dict = None) -> Dict:
        """执行技能的主要逻辑"""
        pass
    
    def get_info(self) -> Dict:
        """获取技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "enabled": self.enabled,
            "last_executed": self.last_executed,
            "execution_count": self.execution_count
        }
    
    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据"""
        return True


class SkillsFramework:
    """多技能框架"""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self.skills: Dict[str, Skill] = {}
        self.context: Dict[str, Any] = {
            "user_preferences": {},
            "execution_history": [],
            "system_config": {}
        }
        self._load_skills()
    
    def _load_skills(self):
        """动态加载技能包"""
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
            print(f"创建技能目录: {self.skills_dir}")
            return
        
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                skill_name = filename[:-3]  # 移除.py后缀
                self._load_skill(skill_name)
    
    def _load_skill(self, skill_name: str):
        """加载单个技能"""
        try:
            spec = importlib.util.spec_from_file_location(
                skill_name, 
                os.path.join(self.skills_dir, f"{skill_name}.py")
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 查找继承自Skill的类
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (inspect.isclass(attr) and 
                    issubclass(attr, Skill) and 
                    attr != Skill):
                    skill_instance = attr()
                    self.skills[skill_name] = skill_instance
                    print(f"✅ 加载技能: {skill_name}")
                    break
        except Exception as e:
            print(f"❌ 加载技能 {skill_name} 失败: {e}")
    
    def execute_skill(self, skill_name: str, input_data: Any) -> Dict:
        """执行指定技能"""
        if skill_name not in self.skills:
            return {"error": f"技能 '{skill_name}' 未找到", "success": False}
        
        skill = self.skills[skill_name]
        if not skill.enabled:
            return {"error": f"技能 '{skill_name}' 已禁用", "success": False}
        
        try:
            # 验证输入
            if not skill.validate_input(input_data):
                return {"error": "输入数据验证失败", "success": False}
            
            # 执行技能
            result = skill.execute(input_data, self.context)
            
            # 更新执行记录
            skill.last_executed = datetime.now()
            skill.execution_count += 1
            
            # 记录执行历史
            execution_record = {
                "skill_name": skill_name,
                "timestamp": datetime.now().isoformat(),
                "input": input_data,
                "result": result
            }
            self.context["execution_history"].append(execution_record)
            
            return {"success": True, "result": result, "skill_info": skill.get_info()}
            
        except Exception as e:
            return {"error": f"执行技能时出错: {e}", "success": False}
    
    def list_skills(self) -> List[Dict]:
        """列出所有可用技能"""
        return [skill.get_info() for skill in self.skills.values()]
    
    def enable_skill(self, skill_name: str):
        """启用技能"""
        if skill_name in self.skills:
            self.skills[skill_name].enabled = True
    
    def disable_skill(self, skill_name: str):
        """禁用技能"""
        if skill_name in self.skills:
            self.skills[skill_name].enabled = False
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict]:
        """获取技能详细信息"""
        if skill_name in self.skills:
            return self.skills[skill_name].get_info()
        return None
    
    def save_context(self, filepath: str = "framework_context.json"):
        """保存框架上下文"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, ensure_ascii=False, indent=2)
    
    def load_context(self, filepath: str = "framework_context.json"):
        """加载框架上下文"""
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.context = json.load(f)


class PrioritySkill(Skill):
    """工作优先级排序技能"""
    
    def __init__(self):
        super().__init__(
            name="priority_sorter",
            description="基于多种因素对工作任务进行优先级排序",
            version="1.0.0"
        )
        self.priority_rules = self._load_priority_rules()
    
    def _load_priority_rules(self) -> Dict:
        """加载优先级排序规则"""
        return {
            "urgency_weight": 0.3,  # 紧急性权重
            "importance_weight": 0.4,  # 重要性权重
            "effort_weight": 0.2,     # 工作量权重
            "deadline_weight": 0.1,   # 截止日期权重
            "categories": {
                "紧急重要": {"min_score": 0.8, "color": "#ff4444"},
                "重要不紧急": {"min_score": 0.6, "color": "#ffaa00"},
                "紧急不重要": {"min_score": 0.4, "color": "#44aa44"},
                "不紧急不重要": {"min_score": 0.0, "color": "#888888"}
            }
        }
    
    def execute(self, input_data: Any, context: Dict = None) -> Dict:
        """执行优先级排序"""
        if isinstance(input_data, str):
            # 如果是文本输入，尝试解析任务列表
            tasks = self._parse_tasks_from_text(input_data)
        elif isinstance(input_data, list):
            # 如果是任务列表
            tasks = input_data
        else:
            return {"error": "不支持的输入格式", "success": False}
        
        # 对任务进行优先级排序
        prioritized_tasks = self._prioritize_tasks(tasks)
        
        return {
            "success": True,
            "prioritized_tasks": prioritized_tasks,
            "summary": self._generate_summary(prioritized_tasks),
            "rules_used": self.priority_rules
        }
    
    def _parse_tasks_from_text(self, text: str) -> List[Dict]:
        """从文本中解析任务"""
        # 简化的文本解析逻辑
        tasks = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                task = {
                    "title": line,
                    "urgency": 5,  # 默认值
                    "importance": 5,
                    "effort": 3,
                    "deadline": None,
                    "category": "待分类"
                }
                tasks.append(task)
        
        return tasks
    
    def _prioritize_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """对任务进行优先级排序"""
        prioritized = []
        
        for task in tasks:
            # 计算优先级分数
            score = self._calculate_priority_score(task)
            task["priority_score"] = score
            task["priority_category"] = self._categorize_priority(score)
            prioritized.append(task)
        
        # 按优先级分数排序
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return prioritized
    
    def _calculate_priority_score(self, task: Dict) -> float:
        """计算任务优先级分数"""
        rules = self.priority_rules
        
        urgency = task.get("urgency", 5) / 10.0
        importance = task.get("importance", 5) / 10.0
        effort = (10 - task.get("effort", 5)) / 10.0  # 工作量越小越好
        
        # 截止日期影响
        deadline_score = self._calculate_deadline_score(task.get("deadline"))
        
        # 加权计算总分
        total_score = (
            urgency * rules["urgency_weight"] +
            importance * rules["importance_weight"] +
            effort * rules["effort_weight"] +
            deadline_score * rules["deadline_weight"]
        )
        
        return round(total_score, 2)
    
    def _calculate_deadline_score(self, deadline: Optional[str]) -> float:
        """计算截止日期分数"""
        if not deadline:
            return 0.5
        
        try:
            deadline_date = datetime.fromisoformat(deadline)
            days_until_deadline = (deadline_date - datetime.now()).days
            
            if days_until_deadline <= 0:
                return 1.0  # 已过期或今天到期
            elif days_until_deadline <= 3:
                return 0.8  # 3天内到期
            elif days_until_deadline <= 7:
                return 0.6  # 一周内到期
            else:
                return 0.3  # 一周以上
        except:
            return 0.5
    
    def _categorize_priority(self, score: float) -> str:
        """根据分数分类优先级"""
        categories = self.priority_rules["categories"]
        
        for category, config in categories.items():
            if score >= config["min_score"]:
                return category
        
        return "不紧急不重要"
    
    def _generate_summary(self, tasks: List[Dict]) -> Dict:
        """生成排序摘要"""
        total_tasks = len(tasks)
        category_counts = {}
        
        for task in tasks:
            category = task["priority_category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_tasks": total_tasks,
            "category_distribution": category_counts,
            "highest_priority": tasks[0]["title"] if tasks else "无任务",
            "average_score": round(sum(t["priority_score"] for t in tasks) / total_tasks, 2) if tasks else 0
        }


# 框架使用示例
def main():
    """框架使用示例"""
    # 创建框架实例
    framework = SkillsFramework()
    
    # 手动添加优先级排序技能（如果未自动加载）
    if "priority_sorter" not in framework.skills:
        framework.skills["priority_sorter"] = PrioritySkill()
    
    # 列出所有技能
    print("\n🛠️ 可用技能:")
    for skill_info in framework.list_skills():
        print(f"  - {skill_info['name']}: {skill_info['description']}")
    
    # 测试优先级排序技能
    test_tasks = [
        {
            "title": "完成项目报告",
            "urgency": 8,
            "importance": 9,
            "effort": 6,
            "deadline": "2025-03-15"
        },
        {
            "title": "回复客户邮件",
            "urgency": 7,
            "importance": 6,
            "effort": 2,
            "deadline": "2025-03-14"
        },
        {
            "title": "学习新技术",
            "urgency": 3,
            "importance": 8,
            "effort": 5,
            "deadline": None
        }
    ]
    
    print("\n📊 测试优先级排序:")
    result = framework.execute_skill("priority_sorter", test_tasks)
    
    if result["success"]:
        print("✅ 排序成功!")
        for i, task in enumerate(result["result"]["prioritized_tasks"], 1):
            print(f"  {i}. [{task['priority_category']}] {task['title']} (分数: {task['priority_score']})")
        
        summary = result["result"]["summary"]
        print(f"\n📈 摘要: 共{summary['total_tasks']}个任务，平均分数: {summary['average_score']}")
    else:
        print(f"❌ 排序失败: {result['error']}")


if __name__ == "__main__":
    main()