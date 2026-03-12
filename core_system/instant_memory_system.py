#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即时交互式记忆系统
直接在对话中处理任务安排和工作沟通
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class InstantMemorySystem:
    """即时交互式记忆系统"""
    
    def __init__(self):
        self.memory_file = "instant_memory.json"
        self.tasks = []
        self.habits = []
        self.decisions = []
        self.work_patterns = []
        self._load_memory()
        
    def _load_memory(self):
        """加载记忆数据"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.habits = data.get('habits', [])
                    self.decisions = data.get('decisions', [])
                    self.work_patterns = data.get('work_patterns', [])
        except Exception as e:
            print(f"加载记忆数据失败: {e}")
            self._init_default_data()
    
    def _init_default_data(self):
        """初始化默认数据"""
        self.tasks = []
        self.habits = []
        self.decisions = []
        self.work_patterns = []
    
    def _save_memory(self):
        """保存记忆数据"""
        try:
            data = {
                'tasks': self.tasks,
                'habits': self.habits,
                'decisions': self.decisions,
                'work_patterns': self.work_patterns,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记忆数据失败: {e}")
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """处理用户消息，自动识别并处理相关内容"""
        result = {
            'type': 'unknown',
            'content': message,
            'timestamp': datetime.now().isoformat(),
            'extracted_data': {},
            'actions_taken': []
        }
        
        # 自动识别消息类型
        if self._is_task_related(message):
            task_data = self._extract_task_info(message)
            if task_data:
                result['type'] = 'task'
                result['extracted_data'] = task_data
                self._handle_task(task_data, result['actions_taken'])
        
        elif self._is_habit_related(message):
            habit_data = self._extract_habit_info(message)
            if habit_data:
                result['type'] = 'habit'
                result['extracted_data'] = habit_data
                self._handle_habit(habit_data, result['actions_taken'])
        
        elif self._is_decision_related(message):
            decision_data = self._extract_decision_info(message)
            if decision_data:
                result['type'] = 'decision'
                result['extracted_data'] = decision_data
                self._handle_decision(decision_data, result['actions_taken'])
        
        elif self._is_work_pattern_related(message):
            pattern_data = self._extract_work_pattern_info(message)
            if pattern_data:
                result['type'] = 'work_pattern'
                result['extracted_data'] = pattern_data
                self._handle_work_pattern(pattern_data, result['actions_taken'])
        
        # 保存更新
        self._save_memory()
        
        return result
    
    def _is_task_related(self, message: str) -> bool:
        """判断是否为任务相关消息"""
        task_keywords = ['任务', 'todo', '要做', '完成', '安排', '计划', '需要', '待办', 'checklist']
        return any(keyword in message.lower() for keyword in task_keywords)
    
    def _is_habit_related(self, message: str) -> bool:
        """判断是否为习惯相关消息"""
        habit_keywords = ['习惯', '每天', '经常', '定期', '例行', '坚持', '养成', 'hobby', 'routine']
        return any(keyword in message.lower() for keyword in habit_keywords)
    
    def _is_decision_related(self, message: str) -> bool:
        """判断是否为决策相关消息"""
        decision_keywords = ['决定', '选择', '决策', '思考', '考虑', '决定', 'decisi', 'choose', 'think']
        return any(keyword in message.lower() for keyword in decision_keywords)
    
    def _is_work_pattern_related(self, message: str) -> bool:
        """判断是否为工作模式相关消息"""
        pattern_keywords = ['工作方式', '工作习惯', '模式', '流程', '方法', 'style', 'pattern', 'method']
        return any(keyword in message.lower() for keyword in pattern_keywords)
    
    def _extract_task_info(self, message: str) -> Dict:
        """从消息中提取任务信息"""
        # 简单的正则匹配
        task_info = {
            'title': '',
            'priority': 'medium',
            'deadline': None,
            'estimated_time': 60,  # 默认60分钟
            'category': '工作',
            'status': 'pending'
        }
        
        # 提取任务标题（通常是第一个句子）
        sentences = re.split(r'[。！？!?]', message)
        if sentences:
            task_info['title'] = sentences[0].strip()
        
        # 提取优先级
        priority_patterns = {
            'high': ['紧急', '重要', 'urgent', 'important', '尽快'],
            'medium': ['一般', '中等', '正常', 'medium'],
            'low': ['不紧急', '次要', 'low', 'minor']
        }
        
        message_lower = message.lower()
        for priority, keywords in priority_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                task_info['priority'] = priority
                break
        
        # 提取截止日期（简化版）
        date_pattern = r'(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?|\d{1,2}[月/-]\d{1,2}[日]?)'
        dates = re.findall(date_pattern, message)
        if dates:
            task_info['deadline'] = dates[0]
        
        # 提取时间估算
        time_pattern = r'(\d+)(分钟|小时|天|min|hour|day)'
        time_matches = re.findall(time_pattern, message)
        if time_matches:
            value, unit = time_matches[0]
            value = int(value)
            if '小时' in unit or 'hour' in unit:
                task_info['estimated_time'] = value * 60
            elif '天' in unit or 'day' in unit:
                task_info['estimated_time'] = value * 8 * 60  # 假设每天8小时
            else:
                task_info['estimated_time'] = value
        
        return task_info
    
    def _extract_habit_info(self, message: str) -> Dict:
        """从消息中提取习惯信息"""
        habit_info = {
            'name': '',
            'frequency': 'daily',
            'success_rate': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'benefit': ''
        }
        
        # 提取习惯名称
        sentences = re.split(r'[。！？!?]', message)
        if sentences:
            habit_info['name'] = sentences[0].strip()
        
        # 提取频率
        freq_patterns = {
            'daily': ['每天', '每日', '天天', 'daily'],
            'weekly': ['每周', '星期', 'weekly'],
            'monthly': ['每月', 'monthly']
        }
        
        message_lower = message.lower()
        for freq, keywords in freq_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                habit_info['frequency'] = freq
                break
        
        # 提取好处
        if '好' in message or 'benefit' in message_lower or 'advantage' in message_lower:
            # 简单提取好处描述
            benefit_match = re.search(r'(好处|益处|优点|benefit|advantage)[:：]?\s*(.+)', message)
            if benefit_match:
                habit_info['benefit'] = benefit_match.group(2).strip()
        
        return habit_info
    
    def _extract_decision_info(self, message: str) -> Dict:
        """从消息中提取决策信息"""
        decision_info = {
            'type': '工作',
            'description': '',
            'result': 'pending',
            'confidence': 7,
            'learnings': ''
        }
        
        # 提取决策描述
        sentences = re.split(r'[。！？!?]', message)
        if sentences:
            decision_info['description'] = sentences[0].strip()
        
        # 提取决策类型
        type_patterns = {
            '工作': ['工作', '项目', '业务', 'work', 'project'],
            '个人': ['个人', '生活', '家庭', 'personal', 'life'],
            '技术': ['技术', '工具', '技术栈', 'technical', 'tech']
        }
        
        message_lower = message.lower()
        for dtype, keywords in type_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                decision_info['type'] = dtype
                break
        
        # 提取信心度
        if '信心' in message or 'confidence' in message_lower:
            conf_match = re.search(r'信心[度]?[:：]?\s*(\d+)|confidence[:：]?\s*(\d+)', message)
            if conf_match:
                conf_value = conf_match.group(1) or conf_match.group(2)
                if conf_value:
                    decision_info['confidence'] = min(max(int(conf_value), 1), 10)
        
        return decision_info
    
    def _extract_work_pattern_info(self, message: str) -> Dict:
        """从消息中提取工作模式信息"""
        pattern_info = {
            'pattern_name': '',
            'description': '',
            'effectiveness': 7,
            'tools_used': [],
            'best_for': ''
        }
        
        # 提取模式名称/描述
        sentences = re.split(r'[。！？!?]', message)
        if sentences:
            pattern_info['description'] = sentences[0].strip()
            pattern_info['pattern_name'] = sentences[0].strip()[:20]  # 取前20字符作为名称
        
        # 提取工具使用
        tool_keywords = ['工具', '软件', '应用', 'platform', 'tool', 'software']
        if any(keyword in message.lower() for keyword in tool_keywords):
            # 简单提取工具名称
            tool_matches = re.findall(r'([A-Za-z]+[A-Za-z0-9]*\s*[A-Za-z0-9]*)', message)
            if tool_matches:
                pattern_info['tools_used'] = tool_matches[:3]  # 最多取3个
        
        return pattern_info
    
    def _handle_task(self, task_data: Dict, actions: List[str]):
        """处理任务信息"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task = {
            'id': task_id,
            **task_data,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        actions.append(f"已创建任务: {task_data['title']}")
        
        # 自动进行优先级排序
        prioritized_tasks = self._prioritize_tasks()
        if prioritized_tasks:
            actions.append(f"当前共有 {len(prioritized_tasks)} 个待办任务")
            if len(prioritized_tasks) >= 3:
                actions.append(f"最高优先级: {prioritized_tasks[0]['title']}")
    
    def _handle_habit(self, habit_data: Dict, actions: List[str]):
        """处理习惯信息"""
        habit_id = f"habit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        habit = {
            'id': habit_id,
            **habit_data,
            'created_at': datetime.now().isoformat(),
            'streak': 0
        }
        
        self.habits.append(habit)
        actions.append(f"已记录习惯: {habit_data['name']}")
        actions.append(f"频率: {habit_data['frequency']}")
    
    def _handle_decision(self, decision_data: Dict, actions: List[str]):
        """处理决策信息"""
        decision_id = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        decision = {
            'id': decision_id,
            **decision_data,
            'created_at': datetime.now().isoformat(),
            'context': '对话记录'
        }
        
        self.decisions.append(decision)
        actions.append(f"已记录决策: {decision_data['description'][:50]}...")
        actions.append(f"信心度: {decision_data['confidence']}/10")
    
    def _handle_work_pattern(self, pattern_data: Dict, actions: List[str]):
        """处理工作模式信息"""
        pattern_id = f"pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        pattern = {
            'id': pattern_id,
            **pattern_data,
            'created_at': datetime.now().isoformat()
        }
        
        self.work_patterns.append(pattern)
        actions.append(f"已记录工作模式: {pattern_data['pattern_name']}")
        if pattern_data['tools_used']:
            actions.append(f"使用工具: {', '.join(pattern_data['tools_used'])}")
    
    def _prioritize_tasks(self) -> List[Dict]:
        """对任务进行简单优先级排序"""
        if not self.tasks:
            return []
        
        # 按优先级和创建时间排序
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        
        def task_score(task):
            base_score = priority_order.get(task.get('priority', 'medium'), 2)
            # 如果有截止日期，增加紧急度
            if task.get('deadline'):
                base_score += 1
            return base_score
        
        sorted_tasks = sorted(self.tasks, key=task_score, reverse=True)
        return sorted_tasks
    
    def get_summary(self) -> Dict:
        """获取系统摘要"""
        return {
            'total_tasks': len(self.tasks),
            'pending_tasks': len([t for t in self.tasks if t.get('status') == 'pending']),
            'completed_tasks': len([t for t in self.tasks if t.get('status') == 'completed']),
            'total_habits': len(self.habits),
            'total_decisions': len(self.decisions),
            'total_patterns': len(self.work_patterns),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_today_tasks(self) -> List[Dict]:
        """获取今日相关任务"""
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        
        # 简单的今日任务筛选
        today_tasks = []
        for task in self.tasks:
            if task.get('deadline') and today_str in task['deadline']:
                today_tasks.append(task)
            elif task.get('priority') == 'high':
                today_tasks.append(task)
        
        return today_tasks[:5]  # 最多返回5个
    
    def add_task_directly(self, title: str, priority: str = 'medium', **kwargs):
        """直接添加任务"""
        task_data = {
            'title': title,
            'priority': priority,
            **kwargs
        }
        self._handle_task(task_data, [])
        self._save_memory()
    
    def complete_task(self, task_title: str):
        """标记任务为完成"""
        for task in self.tasks:
            if task['title'] == task_title:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                task['updated_at'] = datetime.now().isoformat()
                self._save_memory()
                return True
        return False


# 全局实例
memory_system = InstantMemorySystem()


def process_user_message(message: str) -> str:
    """处理用户消息并生成响应"""
    result = memory_system.process_message(message)
    
    response_parts = []
    
    # 根据类型生成响应
    if result['type'] == 'task':
        response_parts.append(f"📝 **任务已记录**")
        response_parts.append(f"标题: {result['extracted_data']['title']}")
        response_parts.append(f"优先级: {result['extracted_data']['priority']}")
        if result['extracted_data'].get('deadline'):
            response_parts.append(f"截止日期: {result['extracted_data']['deadline']}")
    
    elif result['type'] == 'habit':
        response_parts.append(f"🔄 **习惯已记录**")
        response_parts.append(f"名称: {result['extracted_data']['name']}")
        response_parts.append(f"频率: {result['extracted_data']['frequency']}")
    
    elif result['type'] == 'decision':
        response_parts.append(f"🤔 **决策已记录**")
        response_parts.append(f"描述: {result['extracted_data']['description'][:100]}...")
        response_parts.append(f"信心度: {result['extracted_data']['confidence']}/10")
    
    elif result['type'] == 'work_pattern':
        response_parts.append(f"💼 **工作模式已记录**")
        response_parts.append(f"描述: {result['extracted_data']['description'][:100]}...")
    
    else:
        response_parts.append(f"💬 **对话已记录**")
        response_parts.append(f"内容: {message[:150]}...")
    
    # 添加系统状态
    summary = memory_system.get_summary()
    response_parts.append(f"\n📊 **系统状态**")
    response_parts.append(f"待办任务: {summary['pending_tasks']}个")
    response_parts.append(f"已完成: {summary['completed_tasks']}个")
    response_parts.append(f"习惯记录: {summary['total_habits']}个")
    
    # 显示今日任务提醒
    today_tasks = memory_system.get_today_tasks()
    if today_tasks:
        response_parts.append(f"\n⚠️ **今日重点关注**")
        for i, task in enumerate(today_tasks[:3], 1):
            response_parts.append(f"{i}. {task['title']} ({task.get('priority', 'medium')})")
    
    return "\n".join(response_parts)


def get_system_summary() -> str:
    """获取系统详细摘要"""
    summary = memory_system.get_summary()
    tasks = memory_system._prioritize_tasks()
    
    response_parts = ["📋 **系统完整摘要**"]
    response_parts.append("="*40)
    
    response_parts.append(f"\n📊 **统计概览**")
    response_parts.append(f"• 总任务数: {summary['total_tasks']}")
    response_parts.append(f"• 待办任务: {summary['pending_tasks']}")
    response_parts.append(f"• 已完成: {summary['completed_tasks']}")
    response_parts.append(f"• 习惯记录: {summary['total_habits']}")
    response_parts.append(f"• 决策记录: {summary['total_decisions']}")
    response_parts.append(f"• 工作模式: {summary['total_patterns']}")
    
    if tasks:
        response_parts.append(f"\n🎯 **优先级任务**")
        for i, task in enumerate(tasks[:5], 1):
            status = "✅" if task.get('status') == 'completed' else "⏳"
            response_parts.append(f"{i}. {status} {task['title']} ({task.get('priority', 'medium')})")
    
    if memory_system.habits:
        response_parts.append(f"\n🔄 **近期习惯**")
        for habit in memory_system.habits[-3:]:
            response_parts.append(f"• {habit['name']} ({habit['frequency']})")
    
    response_parts.append(f"\n⏰ **最后更新**: {summary['last_updated'][:16]}")
    
    return "\n".join(response_parts)


# 测试函数
def test_system():
    """测试系统功能"""
    test_messages = [
        "我今天需要完成项目报告，这个任务很紧急",
        "我养成了每天早晨6点起床的习惯",
        "我决定使用Python而不是Java进行新项目开发",
        "我发现早晨9-11点是我工作效率最高的时间段"
    ]
    
    for msg in test_messages:
        print(f"\n💬 输入: {msg}")
        print("-" * 50)
        response = process_user_message(msg)
        print(response)
        print("-" * 50)
    
    print("\n" + "="*50)
    print(get_system_summary())


if __name__ == "__main__":
    import os
    test_system()