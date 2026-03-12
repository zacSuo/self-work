#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作优先级排序技能包
基于多种因素对工作任务进行智能优先级排序
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from ..skills_framework import Skill


class PrioritySorter(Skill):
    """工作优先级排序技能"""
    
    def __init__(self):
        super().__init__(
            name="priority_sorter",
            description="基于紧急性、重要性、工作量、截止日期等因素对工作任务进行智能优先级排序",
            version="1.2.0"
        )
        
        # 加载用户偏好和规则
        self.user_preferences = self._load_user_preferences()
        self.priority_rules = self._load_priority_rules()
        self.history_file = "priority_history.json"
        
    def _load_user_preferences(self) -> Dict:
        """加载用户偏好设置"""
        default_preferences = {
            "preferred_working_hours": ["09:00", "18:00"],
            "max_daily_tasks": 8,
            "focus_time_slots": ["09:00-11:00", "14:00-16:00"],
            "avoid_distractions": True,
            "energy_levels": {
                "morning": "high",
                "afternoon": "medium", 
                "evening": "low"
            }
        }
        
        # 尝试加载用户自定义偏好
        prefs_file = "user_preferences.json"
        if os.path.exists(prefs_file):
            try:
                with open(prefs_file, 'r', encoding='utf-8') as f:
                    user_prefs = json.load(f)
                    # 合并默认值和用户设置
                    default_preferences.update(user_prefs)
            except:
                pass
                
        return default_preferences
    
    def _load_priority_rules(self) -> Dict:
        """加载优先级排序规则"""
        return {
            "weights": {
                "urgency": 0.30,      # 紧急性权重
                "importance": 0.35,    # 重要性权重
                "effort": 0.20,        # 工作量权重
                "deadline": 0.15,      # 截止日期权重
            },
            "categories": {
                "紧急重要": {
                    "min_score": 0.80, 
                    "color": "#ff4444",
                    "recommended_time": "focus_time",
                    "description": "需要立即处理的重要任务"
                },
                "重要不紧急": {
                    "min_score": 0.60, 
                    "color": "#ffaa00",
                    "recommended_time": "morning",
                    "description": "重要但可以稍后处理的任务"
                },
                "紧急不重要": {
                    "min_score": 0.40, 
                    "color": "#44aa44",
                    "recommended_time": "afternoon", 
                    "description": "紧急但不重要的任务"
                },
                "不紧急不重要": {
                    "min_score": 0.00, 
                    "color": "#888888",
                    "recommended_time": "evening",
                    "description": "可以推迟或委托的任务"
                }
            },
            "scoring_ranges": {
                "urgency": (1, 10),
                "importance": (1, 10), 
                "effort": (1, 10)
            }
        }
    
    def execute(self, input_data: Any, context: Dict = None) -> Dict:
        """执行优先级排序"""
        try:
            # 解析输入数据
            tasks = self._parse_input(input_data)
            
            if not tasks:
                return {"error": "未找到有效的任务数据", "success": False}
            
            # 对任务进行优先级排序
            prioritized_tasks = self._prioritize_tasks(tasks)
            
            # 生成每日工作计划
            daily_plan = self._generate_daily_plan(prioritized_tasks)
            
            # 保存执行历史
            self._save_execution_history(prioritized_tasks)
            
            return {
                "success": True,
                "prioritized_tasks": prioritized_tasks,
                "daily_plan": daily_plan,
                "summary": self._generate_summary(prioritized_tasks),
                "recommendations": self._generate_recommendations(prioritized_tasks)
            }
            
        except Exception as e:
            return {"error": f"执行优先级排序时出错: {str(e)}", "success": False}
    
    def _parse_input(self, input_data: Any) -> List[Dict]:
        """解析输入数据"""
        tasks = []
        
        if isinstance(input_data, str):
            # 文本输入：支持多种格式
            tasks = self._parse_text_input(input_data)
        elif isinstance(input_data, list):
            # 任务列表输入
            tasks = self._validate_task_list(input_data)
        elif isinstance(input_data, dict) and "tasks" in input_data:
            # 包含任务列表的字典
            tasks = self._validate_task_list(input_data["tasks"])
        else:
            raise ValueError("不支持的输入格式")
        
        return tasks
    
    def _parse_text_input(self, text: str) -> List[Dict]:
        """从文本中解析任务"""
        tasks = []
        lines = text.strip().split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith(('#', '//', '--')):
                continue
                
            # 尝试解析不同格式
            task = self._parse_task_line(line, i+1)
            if task:
                tasks.append(task)
        
        return tasks
    
    def _parse_task_line(self, line: str, line_num: int) -> Optional[Dict]:
        """解析单行任务文本"""
        # 支持多种格式：
        # 1. 简单任务标题
        # 2. 任务标题 [紧急度/重要性/工作量]
        # 3. JSON格式
        
        task = {
            "id": f"task_{line_num}",
            "title": line,
            "urgency": 5,
            "importance": 5, 
            "effort": 3,
            "deadline": None,
            "category": "工作",
            "estimated_time": 60,  # 默认60分钟
            "dependencies": [],
            "tags": []
        }
        
        # 尝试解析带参数的任务
        if '[' in line and ']' in line:
            try:
                title_part = line.split('[')[0].strip()
                params_part = line.split('[')[1].split(']')[0]
                
                task["title"] = title_part
                
                # 解析参数：紧急度/重要性/工作量
                params = params_part.split('/')
                if len(params) >= 1:
                    task["urgency"] = min(max(int(params[0]), 1), 10)
                if len(params) >= 2:
                    task["importance"] = min(max(int(params[1]), 1), 10)
                if len(params) >= 3:
                    task["effort"] = min(max(int(params[2]), 1), 10)
                    
            except:
                pass  # 保持默认值
        
        return task
    
    def _validate_task_list(self, tasks: List[Dict]) -> List[Dict]:
        """验证任务列表"""
        validated_tasks = []
        
        for i, task in enumerate(tasks):
            if isinstance(task, dict):
                # 确保必要字段存在
                validated_task = {
                    "id": task.get("id", f"task_{i+1}"),
                    "title": task.get("title", "未命名任务"),
                    "urgency": min(max(task.get("urgency", 5), 1), 10),
                    "importance": min(max(task.get("importance", 5), 1), 10),
                    "effort": min(max(task.get("effort", 3), 1), 10),
                    "deadline": task.get("deadline"),
                    "category": task.get("category", "工作"),
                    "estimated_time": task.get("estimated_time", 60),
                    "dependencies": task.get("dependencies", []),
                    "tags": task.get("tags", [])
                }
                validated_tasks.append(validated_task)
        
        return validated_tasks
    
    def _prioritize_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """对任务进行优先级排序"""
        prioritized = []
        
        for task in tasks:
            # 计算优先级分数
            score = self._calculate_priority_score(task)
            
            # 添加排序信息
            task["priority_score"] = score
            task["priority_category"] = self._categorize_priority(score)
            task["recommended_time"] = self._get_recommended_time(task)
            task["sort_timestamp"] = datetime.now().isoformat()
            
            prioritized.append(task)
        
        # 按优先级分数排序
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # 添加排名
        for i, task in enumerate(prioritized, 1):
            task["rank"] = i
        
        return prioritized
    
    def _calculate_priority_score(self, task: Dict) -> float:
        """计算任务优先级分数"""
        weights = self.priority_rules["weights"]
        
        # 标准化各项指标（0-1范围）
        urgency = (task.get("urgency", 5) - 1) / 9.0
        importance = (task.get("importance", 5) - 1) / 9.0
        effort = (10 - task.get("effort", 5)) / 9.0  # 工作量越小越好
        
        # 截止日期影响
        deadline_score = self._calculate_deadline_score(task.get("deadline"))
        
        # 加权计算总分
        total_score = (
            urgency * weights["urgency"] +
            importance * weights["importance"] +
            effort * weights["effort"] +
            deadline_score * weights["deadline"]
        )
        
        return round(total_score, 3)
    
    def _calculate_deadline_score(self, deadline: Optional[str]) -> float:
        """计算截止日期分数"""
        if not deadline:
            return 0.5
        
        try:
            if isinstance(deadline, str):
                deadline_date = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
            else:
                return 0.5
                
            days_until_deadline = (deadline_date - datetime.now()).days
            
            if days_until_deadline <= 0:
                return 1.0  # 已过期或今天到期
            elif days_until_deadline <= 1:
                return 0.9  # 明天到期
            elif days_until_deadline <= 3:
                return 0.8  # 3天内到期
            elif days_until_deadline <= 7:
                return 0.6  # 一周内到期
            elif days_until_deadline <= 14:
                return 0.4  # 两周内到期
            else:
                return 0.2  # 两周以上
        except:
            return 0.5
    
    def _categorize_priority(self, score: float) -> str:
        """根据分数分类优先级"""
        categories = self.priority_rules["categories"]
        
        for category, config in categories.items():
            if score >= config["min_score"]:
                return category
        
        return "不紧急不重要"
    
    def _get_recommended_time(self, task: Dict) -> str:
        """获取推荐执行时间"""
        category = task["priority_category"]
        category_config = self.priority_rules["categories"].get(category, {})
        
        return category_config.get("recommended_time", "flexible")
    
    def _generate_daily_plan(self, tasks: List[Dict]) -> Dict:
        """生成每日工作计划"""
        max_daily_tasks = self.user_preferences.get("max_daily_tasks", 8)
        
        # 筛选今日可完成的任务
        today_tasks = []
        total_time = 0
        max_daily_time = 8 * 60  # 8小时工作制
        
        for task in tasks[:max_daily_tasks]:
            task_time = task.get("estimated_time", 60)
            if total_time + task_time <= max_daily_time:
                today_tasks.append(task)
                total_time += task_time
            else:
                break
        
        # 按推荐时间分组
        time_slots = {
            "morning": [],
            "focus_time": [], 
            "afternoon": [],
            "evening": [],
            "flexible": []
        }
        
        for task in today_tasks:
            time_slot = task.get("recommended_time", "flexible")
            time_slots[time_slot].append(task)
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_tasks": len(today_tasks),
            "total_time_minutes": total_time,
            "time_slots": time_slots,
            "completion_estimate": f"{total_time // 60}小时{total_time % 60}分钟"
        }
    
    def _generate_summary(self, tasks: List[Dict]) -> Dict:
        """生成排序摘要"""
        total_tasks = len(tasks)
        category_counts = {}
        total_score = 0
        
        for task in tasks:
            category = task["priority_category"]
            category_counts[category] = category_counts.get(category, 0) + 1
            total_score += task["priority_score"]
        
        return {
            "total_tasks": total_tasks,
            "category_distribution": category_counts,
            "highest_priority": tasks[0] if tasks else None,
            "average_score": round(total_score / total_tasks, 3) if tasks else 0,
            "urgency_level": self._calculate_overall_urgency(tasks)
        }
    
    def _calculate_overall_urgency(self, tasks: List[Dict]) -> str:
        """计算整体紧急程度"""
        if not tasks:
            return "低"
        
        urgent_count = sum(1 for t in tasks if t["priority_category"] == "紧急重要")
        total_count = len(tasks)
        
        urgent_ratio = urgent_count / total_count
        
        if urgent_ratio > 0.5:
            return "非常高"
        elif urgent_ratio > 0.3:
            return "高"
        elif urgent_ratio > 0.1:
            return "中等"
        else:
            return "低"
    
    def _generate_recommendations(self, tasks: List[Dict]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 分析任务特性给出建议
        urgent_tasks = [t for t in tasks if t["priority_category"] == "紧急重要"]
        high_effort_tasks = [t for t in tasks if t.get("effort", 0) >= 7]
        
        if len(urgent_tasks) > 3:
            recommendations.append("⚠️ 紧急任务较多，建议优先处理最关键的2-3项")
        
        if len(high_effort_tasks) > 2:
            recommendations.append("💪 高工作量任务较多，考虑拆分或寻求帮助")
        
        if any(t.get("dependencies") for t in tasks):
            recommendations.append("🔗 存在依赖关系的任务，请按依赖顺序处理")
        
        # 基于用户偏好的建议
        if self.user_preferences.get("avoid_distractions", True):
            recommendations.append("🔇 建议在专注时段处理重要任务，避免干扰")
        
        return recommendations
    
    def _save_execution_history(self, tasks: List[Dict]):
        """保存执行历史"""
        try:
            history = []
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            execution_record = {
                "timestamp": datetime.now().isoformat(),
                "total_tasks": len(tasks),
                "categories": {},
                "highest_priority_task": tasks[0]["title"] if tasks else None
            }
            
            # 统计分类情况
            for task in tasks:
                category = task["priority_category"]
                execution_record["categories"][category] = execution_record["categories"].get(category, 0) + 1
            
            history.append(execution_record)
            
            # 只保留最近30次记录
            if len(history) > 30:
                history = history[-30:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据"""
        if not input_data:
            return False
        
        if isinstance(input_data, (str, list, dict)):
            return True
        
        return False


def main():
    """技能测试"""
    sorter = PrioritySorter()
    
    # 测试数据
    test_tasks = [
        {
            "title": "完成项目报告并提交",
            "urgency": 9,
            "importance": 8,
            "effort": 7,
            "deadline": "2025-03-15",
            "estimated_time": 120
        },
        {
            "title": "回复重要客户邮件",
            "urgency": 8,
            "importance": 7,
            "effort": 2,
            "deadline": "2025-03-14",
            "estimated_time": 30
        },
        {
            "title": "学习新技术框架",
            "urgency": 3,
            "importance": 8,
            "effort": 6,
            "deadline": None,
            "estimated_time": 180
        }
    ]
    
    print("🧠 工作优先级排序技能测试")
    print("=" * 50)
    
    result = sorter.execute(test_tasks)
    
    if result["success"]:
        print("✅ 排序成功!")
        print("\n📋 优先级排序结果:")
        
        for task in result["prioritized_tasks"]:
            print(f"  {task['rank']}. [{task['priority_category']}] {task['title']}")
            print(f"     分数: {task['priority_score']} | 紧急度: {task['urgency']} | 重要性: {task['importance']}")
        
        summary = result["summary"]
        print(f"\n📈 摘要: 共{summary['total_tasks']}个任务，整体紧急度: {summary['urgency_level']}")
        
        print("\n💡 建议:")
        for rec in result["recommendations"]:
            print(f"  - {rec}")
    else:
        print(f"❌ 排序失败: {result['error']}")


if __name__ == "__main__":
    main()