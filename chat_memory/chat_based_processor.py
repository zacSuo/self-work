#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天式任务处理器
专门用于在当前对话环境中直接处理任务安排和工作沟通
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os


class ChatTaskProcessor:
    """聊天式任务处理器"""
    
    def __init__(self):
        self.data_file = "chat_memory.json"
        self.tasks = []
        self.notes = []
        self.decisions = []
        self.meetings = []
        self.ideas = []
        self._load_data()
        
        # 智能处理规则
        self.rules = {
            'task_patterns': [
                r'(需要|要|得|必须|应该|得).*?(完成|做|处理|解决|准备|安排|计划|编写|设计|开发|测试|部署|修复|优化|学习|研究|分析|总结|报告|整理|清理|检查|审核|评估|规划|创建|建立|实施|执行|实现)',
                r'(todo|任务|待办|checklist|清单|计划|安排|schedule|plan).*?[:：]',
                r'^(完成|做|处理|解决|准备|安排).*?[。！？!?]'
            ],
            'decision_patterns': [
                r'(决定|选择|决策|考虑|思考|觉得|认为|打算|准备|计划).*?[。！？!?]',
                r'(选择|使用|采用|决定).*?(而不是|替代|替代品|替代方案)',
                r'(利弊|优缺点|优劣|对比|比较|评估|分析).*?[后然后]'
            ],
            'meeting_patterns': [
                r'(会议|讨论|沟通|会谈|碰头|汇报|报告|分享|演示).*?[。！？!?]',
                r'(与|和|跟).*?(开会|讨论|沟通|交流|协商)',
                r'(定于|安排在|计划在|约在).*?(时间|时候|日期)'
            ],
            'idea_patterns': [
                r'(想法|创意|灵感|点子|主意|建议|提议|方案|思路|构想|设想|脑洞).*?[。！？!?]',
                r'(可以|考虑|尝试|试试|或许|也许|可能).*?(改进|优化|创新|变化|调整|改变)',
                r'(如果|要是|假如|假设).*?(那么|就|则|会)'
            ]
        }
        
    def _load_data(self):
        """加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.notes = data.get('notes', [])
                    self.decisions = data.get('decisions', [])
                    self.meetings = data.get('meetings', [])
                    self.ideas = data.get('ideas', [])
        except Exception as e:
            print(f"加载数据失败: {e}")
            self._init_data()
    
    def _init_data(self):
        """初始化数据"""
        self.tasks = []
        self.notes = []
        self.decisions = []
        self.meetings = []
        self.ideas = []
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {
                'tasks': self.tasks,
                'notes': self.notes,
                'decisions': self.decisions,
                'meetings': self.meetings,
                'ideas': self.ideas,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def process_conversation(self, user_message: str, ai_response: str = "") -> Dict[str, Any]:
        """处理对话内容，提取结构化信息"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'ai_response': ai_response,
            'extracted_items': [],
            'suggested_actions': [],
            'system_updates': []
        }
        
        # 提取任务信息
        tasks_found = self._extract_tasks(user_message)
        if tasks_found:
            analysis['extracted_items'].extend([
                {'type': 'task', 'content': task} for task in tasks_found
            ])
            for task in tasks_found:
                self._add_task(task, analysis['system_updates'])
        
        # 提取决策信息
        decisions_found = self._extract_decisions(user_message)
        if decisions_found:
            analysis['extracted_items'].extend([
                {'type': 'decision', 'content': decision} for decision in decisions_found
            ])
            for decision in decisions_found:
                self._add_decision(decision, analysis['system_updates'])
        
        # 提取会议信息
        meetings_found = self._extract_meetings(user_message)
        if meetings_found:
            analysis['extracted_items'].extend([
                {'type': 'meeting', 'content': meeting} for meeting in meetings_found
            ])
            for meeting in meetings_found:
                self._add_meeting(meeting, analysis['system_updates'])
        
        # 提取想法信息
        ideas_found = self._extract_ideas(user_message)
        if ideas_found:
            analysis['extracted_items'].extend([
                {'type': 'idea', 'content': idea} for idea in ideas_found
            ])
            for idea in ideas_found:
                self._add_idea(idea, analysis['system_updates'])
        
        # 生成建议行动
        analysis['suggested_actions'] = self._generate_suggestions(analysis)
        
        # 保存数据
        self._save_data()
        
        return analysis
    
    def _extract_tasks(self, message: str) -> List[str]:
        """从消息中提取任务"""
        tasks = []
        
        # 使用正则表达式匹配
        for pattern in self.rules['task_patterns']:
            matches = re.finditer(pattern, message)
            for match in matches:
                # 提取任务句子
                sentence_start = max(0, message.rfind('。', 0, match.start()))
                sentence_end = message.find('。', match.end())
                if sentence_end == -1:
                    sentence_end = len(message)
                
                task_sentence = message[sentence_start:sentence_end].strip(' 。，、；')
                if task_sentence and len(task_sentence) > 3:
                    tasks.append(task_sentence)
        
        # 如果没有匹配到模式，尝试提取明显的任务表述
        if not tasks:
            # 简单的句子分割
            sentences = re.split(r'[。！？!?]', message)
            for sentence in sentences:
                if any(keyword in sentence for keyword in ['需要', '要', '得', '必须', '应该', '完成', '做', '处理']):
                    tasks.append(sentence.strip())
        
        return list(set(tasks))  # 去重
    
    def _extract_decisions(self, message: str) -> List[str]:
        """从消息中提取决策"""
        decisions = []
        
        for pattern in self.rules['decision_patterns']:
            matches = re.finditer(pattern, message)
            for match in matches:
                sentence_start = max(0, message.rfind('。', 0, match.start()))
                sentence_end = message.find('。', match.end())
                if sentence_end == -1:
                    sentence_end = len(message)
                
                decision_sentence = message[sentence_start:sentence_end].strip(' 。，、；')
                if decision_sentence and len(decision_sentence) > 3:
                    decisions.append(decision_sentence)
        
        return list(set(decisions))
    
    def _extract_meetings(self, message: str) -> List[str]:
        """从消息中提取会议信息"""
        meetings = []
        
        for pattern in self.rules['meeting_patterns']:
            matches = re.finditer(pattern, message)
            for match in matches:
                sentence_start = max(0, message.rfind('。', 0, match.start()))
                sentence_end = message.find('。', match.end())
                if sentence_end == -1:
                    sentence_end = len(message)
                
                meeting_sentence = message[sentence_start:sentence_end].strip(' 。，、；')
                if meeting_sentence and len(meeting_sentence) > 3:
                    meetings.append(meeting_sentence)
        
        return list(set(meetings))
    
    def _extract_ideas(self, message: str) -> List[str]:
        """从消息中提取想法"""
        ideas = []
        
        for pattern in self.rules['idea_patterns']:
            matches = re.finditer(pattern, message)
            for match in matches:
                sentence_start = max(0, message.rfind('。', 0, match.start()))
                sentence_end = message.find('。', match.end())
                if sentence_end == -1:
                    sentence_end = len(message)
                
                idea_sentence = message[sentence_start:sentence_end].strip(' 。，、；')
                if idea_sentence and len(idea_sentence) > 3:
                    ideas.append(idea_sentence)
        
        return list(set(ideas))
    
    def _add_task(self, task_description: str, updates: List[str]):
        """添加任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 分析任务特性
        priority = 'medium'
        if any(word in task_description for word in ['紧急', '重要', '尽快', '立即', '马上']):
            priority = 'high'
        elif any(word in task_description for word in ['不紧急', '次要', '以后', '有时间']):
            priority = 'low'
        
        task = {
            'id': task_id,
            'description': task_description,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'category': self._categorize_task(task_description)
        }
        
        self.tasks.append(task)
        updates.append(f"📝 已添加任务: {task_description[:50]}...")
    
    def _add_decision(self, decision_description: str, updates: List[str]):
        """添加决策"""
        decision_id = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        decision = {
            'id': decision_id,
            'description': decision_description,
            'type': self._categorize_decision(decision_description),
            'timestamp': datetime.now().isoformat(),
            'status': 'recorded'
        }
        
        self.decisions.append(decision)
        updates.append(f"🤔 已记录决策: {decision_description[:50]}...")
    
    def _add_meeting(self, meeting_description: str, updates: List[str]):
        """添加会议"""
        meeting_id = f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 尝试提取时间信息
        time_info = '未指定'
        time_patterns = [
            r'(\d{1,2}月\d{1,2}日)',
            r'(\d{1,2}[:：]\d{1,2})',
            r'(今天|明天|后天|下周|下月)',
            r'(\d+点|\d+时)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, meeting_description)
            if match:
                time_info = match.group(1)
                break
        
        meeting = {
            'id': meeting_id,
            'description': meeting_description,
            'time_info': time_info,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat()
        }
        
        self.meetings.append(meeting)
        updates.append(f"📅 已记录会议: {meeting_description[:50]}...")
    
    def _add_idea(self, idea_description: str, updates: List[str]):
        """添加想法"""
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        idea = {
            'id': idea_id,
            'description': idea_description,
            'category': self._categorize_idea(idea_description),
            'timestamp': datetime.now().isoformat(),
            'status': 'new'
        }
        
        self.ideas.append(idea)
        updates.append(f"💡 已记录想法: {idea_description[:50]}...")
    
    def _categorize_task(self, description: str) -> str:
        """分类任务"""
        categories = {
            '开发': ['代码', '编程', '开发', '实现', '调试', '测试', '部署'],
            '文档': ['文档', '报告', '总结', '记录', '说明', '手册'],
            '沟通': ['沟通', '会议', '讨论', '汇报', '分享', '演示'],
            '学习': ['学习', '研究', '阅读', '了解', '掌握', '培训'],
            '管理': ['管理', '安排', '计划', '协调', '组织', '监督'],
            '其他': []
        }
        
        for category, keywords in categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return '其他'
    
    def _categorize_decision(self, description: str) -> str:
        """分类决策"""
        categories = {
            '技术': ['技术', '工具', '框架', '语言', '平台', '系统'],
            '业务': ['业务', '产品', '市场', '客户', '合作', '战略'],
            '个人': ['个人', '职业', '发展', '学习', '成长', '生活'],
            '团队': ['团队', '合作', '沟通', '管理', '协作', '组织'],
            '其他': []
        }
        
        for category, keywords in categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return '其他'
    
    def _categorize_idea(self, description: str) -> str:
        """分类想法"""
        categories = {
            '创新': ['创新', '创意', '新颖', '突破', '改进', '优化'],
            '问题解决': ['解决', '改进', '优化', '修复', '提升', '完善'],
            '机会': ['机会', '可能', '潜在', '前景', '方向', '趋势'],
            '其他': []
        }
        
        for category, keywords in categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return '其他'
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """生成建议行动"""
        suggestions = []
        
        # 基于提取的项目建议
        items = analysis['extracted_items']
        if items:
            task_count = sum(1 for item in items if item['type'] == 'task')
            if task_count > 0:
                suggestions.append(f"📋 建议明确{task_count}个任务的具体要求和截止时间")
            
            decision_count = sum(1 for item in items if item['type'] == 'decision')
            if decision_count > 0:
                suggestions.append(f"🤔 建议记录决策的详细理由和预期结果")
            
            meeting_count = sum(1 for item in items if item['type'] == 'meeting')
            if meeting_count > 0:
                suggestions.append(f"📅 建议确认会议的具体时间、地点和议程")
        
        # 基于系统状态建议
        pending_tasks = len([t for t in self.tasks if t['status'] == 'pending'])
        if pending_tasks > 5:
            suggestions.append(f"⚠️ 当前有{pending_tasks}个待办任务，建议进行优先级排序")
        
        if len(self.ideas) > 10:
            suggestions.append("💡 想法记录较多，建议定期回顾和整理")
        
        return suggestions
    
    def get_status_summary(self) -> Dict:
        """获取状态摘要"""
        return {
            'total_tasks': len(self.tasks),
            'pending_tasks': len([t for t in self.tasks if t['status'] == 'pending']),
            'completed_tasks': len([t for t in self.tasks if t['status'] == 'completed']),
            'total_decisions': len(self.decisions),
            'total_meetings': len(self.meetings),
            'total_ideas': len(self.ideas),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_today_focus(self) -> List[Dict]:
        """获取今日关注点"""
        today_focus = []
        
        # 高优先级任务
        high_priority_tasks = [t for t in self.tasks if t['priority'] == 'high' and t['status'] == 'pending']
        today_focus.extend(high_priority_tasks[:3])
        
        # 今天的会议
        today = datetime.now().date()
        today_meetings = []
        for meeting in self.meetings:
            if meeting['status'] == 'scheduled':
                # 简单判断今天相关的会议
                if '今天' in meeting['description'] or '今日' in meeting['description']:
                    today_meetings.append(meeting)
        
        today_focus.extend(today_meetings[:2])
        
        return today_focus
    
    def mark_task_completed(self, task_description: str) -> bool:
        """标记任务完成"""
        for task in self.tasks:
            if task['description'] == task_description:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                self._save_data()
                return True
        return False
    
    def add_note(self, content: str, category: str = "对话记录"):
        """添加笔记"""
        note_id = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        note = {
            'id': note_id,
            'content': content,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        self.notes.append(note)
        self._save_data()


# 全局处理器实例
processor = ChatTaskProcessor()


def analyze_conversation(user_message: str, ai_response: str = "") -> str:
    """分析对话并返回处理结果"""
    analysis = processor.process_conversation(user_message, ai_response)
    
    response_parts = []
    
    # 显示提取的内容
    if analysis['extracted_items']:
        response_parts.append("📋 **对话分析结果**")
        
        item_counts = {}
        for item in analysis['extracted_items']:
            item_type = item['type']
            item_counts[item_type] = item_counts.get(item_type, 0) + 1
        
        for item_type, count in item_counts.items():
            type_icons = {
                'task': '📝',
                'decision': '🤔', 
                'meeting': '📅',
                'idea': '💡'
            }
            icon = type_icons.get(item_type, '📌')
            response_parts.append(f"{icon} {item_type}: {count}项")
    
    # 显示系统更新
    if analysis['system_updates']:
        response_parts.append("\n🔄 **系统更新**")
        for update in analysis['system_updates']:
            response_parts.append(f"• {update}")
    
    # 显示建议
    if analysis['suggested_actions']:
        response_parts.append("\n💡 **建议行动**")
        for suggestion in analysis['suggested_actions']:
            response_parts.append(f"• {suggestion}")
    
    # 显示系统状态
    summary = processor.get_status_summary()
    response_parts.append(f"\n📊 **系统状态**")
    response_parts.append(f"待办任务: {summary['pending_tasks']}/{summary['total_tasks']}")
    response_parts.append(f"决策记录: {summary['total_decisions']}")
    response_parts.append(f"想法收集: {summary['total_ideas']}")
    
    # 显示今日关注
    today_focus = processor.get_today_focus()
    if today_focus:
        response_parts.append("\n⚠️ **今日重点关注**")
        for i, item in enumerate(today_focus[:3], 1):
            item_type = '任务' if 'task' in item['id'] else '会议' if 'meeting' in item['id'] else '事项'
            response_parts.append(f"{i}. [{item_type}] {item['description'][:60]}...")
    
    return "\n".join(response_parts)


def get_detailed_summary() -> str:
    """获取详细摘要"""
    summary = processor.get_status_summary()
    
    response_parts = ["📋 **系统详细摘要**"]
    response_parts.append("="*50)
    
    response_parts.append(f"\n📊 **统计信息**")
    response_parts.append(f"• 总任务数: {summary['total_tasks']}")
    response_parts.append(f"• 待办任务: {summary['pending_tasks']}")
    response_parts.append(f"• 已完成: {summary['completed_tasks']}")
    response_parts.append(f"• 决策记录: {summary['total_decisions']}")
    response_parts.append(f"• 会议安排: {summary['total_meetings']}")
    response_parts.append(f"• 想法收集: {summary['total_ideas']}")
    
    # 显示任务分类
    tasks_by_category = {}
    for task in processor.tasks:
        category = task.get('category', '其他')
        tasks_by_category[category] = tasks_by_category.get(category, 0) + 1
    
    if tasks_by_category:
        response_parts.append(f"\n📈 **任务分类**")
        for category, count in tasks_by_category.items():
            response_parts.append(f"• {category}: {count}个")
    
    # 显示高优先级任务
    high_priority = [t for t in processor.tasks if t.get('priority') == 'high' and t.get('status') == 'pending']
    if high_priority:
        response_parts.append(f"\n🎯 **高优先级任务**")
        for i, task in enumerate(high_priority[:5], 1):
            response_parts.append(f"{i}. {task['description'][:80]}...")
    
    # 显示最近决策
    recent_decisions = processor.decisions[-3:]
    if recent_decisions:
        response_parts.append(f"\n🤔 **最近决策**")
        for decision in recent_decisions:
            response_parts.append(f"• {decision['description'][:100]}...")
    
    response_parts.append(f"\n⏰ **最后更新**: {summary['last_updated'][:16]}")
    
    return "\n".join(response_parts)


# 测试函数
def test_processor():
    """测试处理器"""
    test_conversations = [
        ("我今天需要完成项目报告，这个任务很紧急，下午还要和团队开会讨论技术方案", "好的，我来帮您记录"),
        ("我决定使用Python而不是Java进行新项目开发，因为Python开发效率更高", "这是个不错的决策考虑"),
        ("我有个想法，可以优化我们的代码审查流程，提高团队协作效率", "听起来是个很好的改进方向"),
        ("明天上午10点需要准备产品演示，下午还要处理客户反馈", "我来帮您安排这些任务")
    ]
    
    for user_msg, ai_resp in test_conversations:
        print(f"\n💬 对话:")
        print(f"用户: {user_msg}")
        print(f"AI: {ai_resp}")
        print("-" * 60)
        
        result = analyze_conversation(user_msg, ai_resp)
        print(result)
        print("-" * 60)
    
    print("\n" + "="*60)
    print(get_detailed_summary())


if __name__ == "__main__":
    test_processor()