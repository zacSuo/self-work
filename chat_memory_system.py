#!/usr/bin/env python3
"""
对话式记忆系统 - 自动总结对话内容
支持开机自启动和实时记录
"""

import json
import datetime
import os
import time
import threading
from typing import Dict, List, Any, Optional
import re

class ChatMemorySystem:
    """对话式记忆系统"""
    
    def __init__(self, storage_path: str = "chat_memory_data.json"):
        self.storage_path = storage_path
        self.data = {
            'conversations': [],           # 对话记录
            'habits': [],                  # 自动识别的习惯
            'work_styles': [],             # 工作方式总结
            'decisions': [],               # 决策记录
            'tasks': [],                   # 任务安排
            'user_profile': {}             # 用户画像
        }
        self.load_data()
        self.auto_save_thread = None
        self.running = True
        
        # 启动自动保存线程
        self.start_auto_save()
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"✓ 加载了 {len(self.data['conversations'])} 条对话记录")
            except Exception as e:
                print(f"✗ 加载数据失败: {e}")
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"✗ 保存失败: {e}")
    
    def start_auto_save(self):
        """启动自动保存线程"""
        def auto_save():
            while self.running:
                time.sleep(300)  # 每5分钟自动保存
                self.save_data()
        
        self.auto_save_thread = threading.Thread(target=auto_save, daemon=True)
        self.auto_save_thread.start()
    
    def stop(self):
        """停止系统"""
        self.running = False
        self.save_data()
    
    def analyze_conversation(self, user_input: str) -> Dict[str, Any]:
        """分析对话内容，自动识别关键信息"""
        analysis = {
            'type': 'general',
            'topics': [],
            'habits': [],
            'decisions': [],
            'tasks': [],
            'sentiment': 'neutral'
        }
        
        # 识别对话类型
        input_lower = user_input.lower()
        
        # 习惯相关关键词
        habit_keywords = ['习惯', '每天', '经常', '总是', 'routine', 'daily', '经常性']
        if any(keyword in input_lower for keyword in habit_keywords):
            analysis['type'] = 'habit'
            # 提取习惯信息
            self.extract_habits(user_input, analysis)
        
        # 工作方式关键词
        work_keywords = ['工作', '方式', '方法', '习惯', '流程', 'work', 'method', 'process']
        if any(keyword in input_lower for keyword in work_keywords):
            analysis['type'] = 'work_style'
            
        # 决策关键词
        decision_keywords = ['决定', '选择', '决策', '应该', '需要', 'decision', 'choose']
        if any(keyword in input_lower for keyword in decision_keywords):
            analysis['type'] = 'decision'
            self.extract_decisions(user_input, analysis)
        
        # 任务关键词
        task_keywords = ['任务', '要做', '完成', '计划', '安排', 'task', 'todo', 'plan']
        if any(keyword in input_lower for keyword in task_keywords):
            analysis['type'] = 'task'
            self.extract_tasks(user_input, analysis)
        
        # 情感分析（简单版）
        positive_words = ['好', '喜欢', '满意', '成功', '高兴', 'great', 'like', 'happy']
        negative_words = ['不好', '不喜欢', '问题', '困难', '失败', 'bad', 'problem', 'difficult']
        
        if any(word in input_lower for word in positive_words):
            analysis['sentiment'] = 'positive'
        elif any(word in input_lower for word in negative_words):
            analysis['sentiment'] = 'negative'
        
        return analysis
    
    def extract_habits(self, text: str, analysis: Dict[str, Any]):
        """从文本中提取习惯信息"""
        # 简单的模式匹配
        patterns = [
            r'(每天|经常|总是|通常)(.+?)(的习惯|行为|做法)',
            r'我(喜欢|习惯|经常)(.+?)(做|用|处理)',
            r'(.+?)是我(的)?(日常|经常)(习惯|做法)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                habit_text = match.group().strip()
                if habit_text and len(habit_text) > 3:
                    analysis['habits'].append({
                        'text': habit_text,
                        'frequency': 'daily',
                        'confidence': 0.7
                    })
    
    def extract_decisions(self, text: str, analysis: Dict[str, Any]):
        """从文本中提取决策信息"""
        decision_keywords = ['决定', '选择', '应该', '需要', '打算', '计划']
        
        for keyword in decision_keywords:
            if keyword in text:
                # 简单的决策提取
                start_idx = text.find(keyword)
                decision_text = text[start_idx:start_idx+50]  # 取50个字符
                analysis['decisions'].append({
                    'text': decision_text,
                    'type': 'general',
                    'confidence': 0.6
                })
    
    def extract_tasks(self, text: str, analysis: Dict[str, Any]):
        """从文本中提取任务信息"""
        task_patterns = [
            r'要(完成|做|处理)(.+?)(任务|工作|事情)',
            r'计划(.+?)(完成|实现|处理)',
            r'需要(.+?)(做|完成|处理)'
        ]
        
        for pattern in task_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                task_text = match.group().strip()
                if task_text and len(task_text) > 3:
                    analysis['tasks'].append({
                        'text': task_text,
                        'priority': 'medium',
                        'status': 'pending'
                    })
    
    def record_conversation(self, user_input: str, system_response: str = ""):
        """记录对话内容并自动分析"""
        analysis = self.analyze_conversation(user_input)
        
        conversation = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_input': user_input,
            'system_response': system_response,
            'analysis': analysis,
            'summary': self.generate_summary(user_input, analysis)
        }
        
        self.data['conversations'].append(conversation)
        
        # 根据分析结果更新相关数据
        self.update_related_data(user_input, analysis)
        
        return conversation
    
    def generate_summary(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """生成对话摘要"""
        summary_parts = []
        
        if analysis['type'] == 'habit':
            summary_parts.append("用户讨论了个人习惯相关话题")
            if analysis['habits']:
                summary_parts.append(f"提到了 {len(analysis['habits'])} 个习惯")
        
        elif analysis['type'] == 'decision':
            summary_parts.append("用户在进行决策讨论")
            if analysis['decisions']:
                summary_parts.append(f"涉及 {len(analysis['decisions'])} 个决策点")
        
        elif analysis['type'] == 'task':
            summary_parts.append("用户讨论了任务安排")
            if analysis['tasks']:
                summary_parts.append(f"提到了 {len(analysis['tasks'])} 个任务")
        
        else:
            summary_parts.append("常规对话交流")
        
        # 添加情感信息
        if analysis['sentiment'] != 'neutral':
            sentiment_text = '积极' if analysis['sentiment'] == 'positive' else '消极'
            summary_parts.append(f"情感倾向: {sentiment_text}")
        
        return "; ".join(summary_parts)
    
    def update_related_data(self, user_input: str, analysis: Dict[str, Any]):
        """根据分析结果更新相关数据"""
        # 更新用户画像
        self.update_user_profile(user_input, analysis)
        
        # 如果有明确的习惯信息，添加到习惯库
        for habit_info in analysis['habits']:
            if habit_info['confidence'] > 0.5:
                self.add_habit_from_analysis(habit_info, user_input)
        
        # 如果有明确的决策信息，添加到决策库
        for decision_info in analysis['decisions']:
            if decision_info['confidence'] > 0.5:
                self.add_decision_from_analysis(decision_info, user_input)
        
        # 如果有明确的任务信息，添加到任务库
        for task_info in analysis['tasks']:
            self.add_task_from_analysis(task_info, user_input)
    
    def update_user_profile(self, user_input: str, analysis: Dict[str, Any]):
        """更新用户画像"""
        profile = self.data['user_profile']
        
        # 更新对话统计
        profile.setdefault('conversation_count', 0)
        profile['conversation_count'] += 1
        
        # 更新话题偏好
        topics = profile.setdefault('preferred_topics', {})
        if analysis['type'] != 'general':
            topics[analysis['type']] = topics.get(analysis['type'], 0) + 1
        
        # 更新情感倾向
        sentiment = profile.setdefault('sentiment_trend', {})
        sentiment[analysis['sentiment']] = sentiment.get(analysis['sentiment'], 0) + 1
        
        profile['last_updated'] = datetime.datetime.now().isoformat()
    
    def add_habit_from_analysis(self, habit_info: Dict[str, Any], context: str):
        """从分析结果添加习惯"""
        habit = {
            'name': f"习惯_{len(self.data['habits']) + 1}",
            'description': habit_info['text'],
            'frequency': habit_info['frequency'],
            'priority': 5,
            'created_at': datetime.datetime.now().isoformat(),
            'last_practiced': datetime.datetime.now().isoformat(),
            'context': context,
            'confidence': habit_info['confidence']
        }
        self.data['habits'].append(habit)
    
    def add_decision_from_analysis(self, decision_info: Dict[str, Any], context: str):
        """从分析结果添加决策"""
        decision = {
            'type': decision_info['type'],
            'description': decision_info['text'],
            'context': context,
            'timestamp': datetime.datetime.now().isoformat(),
            'confidence': decision_info['confidence']
        }
        self.data['decisions'].append(decision)
    
    def add_task_from_analysis(self, task_info: Dict[str, Any], context: str):
        """从分析结果添加任务"""
        task = {
            'title': f"任务_{len(self.data['tasks']) + 1}",
            'description': task_info['text'],
            'priority': task_info['priority'],
            'status': task_info['status'],
            'created_at': datetime.datetime.now().isoformat(),
            'context': context
        }
        self.data['tasks'].append(task)
    
    def get_user_summary(self) -> Dict[str, Any]:
        """获取用户总结"""
        profile = self.data['user_profile']
        
        summary = {
            'total_conversations': len(self.data['conversations']),
            'habits_count': len(self.data['habits']),
            'decisions_count': len(self.data['decisions']),
            'tasks_count': len(self.data['tasks']),
            'preferred_topics': profile.get('preferred_topics', {}),
            'sentiment_trend': profile.get('sentiment_trend', {}),
            'last_updated': profile.get('last_updated', '从未更新')
        }
        
        return summary
    
    def get_recent_activity(self, days: int = 7) -> Dict[str, Any]:
        """获取最近活动"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        recent_conversations = [
            conv for conv in self.data['conversations']
            if datetime.datetime.fromisoformat(conv['timestamp']) > cutoff_date
        ]
        
        return {
            'recent_conversations': len(recent_conversations),
            'recent_habits': len([h for h in self.data['habits'] 
                                if datetime.datetime.fromisoformat(h['created_at']) > cutoff_date]),
            'recent_decisions': len([d for d in self.data['decisions'] 
                                   if datetime.datetime.fromisoformat(d['timestamp']) > cutoff_date]),
            'recent_tasks': len([t for t in self.data['tasks'] 
                               if datetime.datetime.fromisoformat(t['created_at']) > cutoff_date])
        }


def create_startup_script():
    """创建开机自启动脚本"""
    script_content = '''@echo off
echo 启动对话式记忆系统...
cd /d "d:\code\workbuddy"
python chat_memory_system.py
echo 系统已启动，正在后台运行...
pause
'''
    
    script_path = "d:\\code\\workbuddy\\start_memory_system.bat"
    
    with open(script_path, 'w', encoding='gbk') as f:
        f.write(script_content)
    
    return script_path


def main():
    """主函数 - 对话式交互"""
    memory = ChatMemorySystem()
    
    print("🧠 对话式记忆系统已启动")
    print("系统会自动分析您的对话内容并总结")
    print("输入 'exit' 退出系统")
    print("输入 'summary' 查看总结")
    print("-" * 50)
    
    # 显示初始状态
    summary = memory.get_user_summary()
    print(f"📊 当前状态: {summary['total_conversations']} 条对话记录")
    
    while True:
        try:
            user_input = input("\n💬 请输入您的对话内容: ").strip()
            
            if user_input.lower() in ['exit', '退出', 'quit']:
                print("\n感谢使用！系统正在保存数据...")
                memory.stop()
                break
            
            elif user_input.lower() in ['summary', '总结', '状态']:
                summary = memory.get_user_summary()
                recent = memory.get_recent_activity(7)
                
                print("\n" + "="*50)
                print("📊 系统总结")
                print("="*50)
                print(f"总对话记录: {summary['total_conversations']} 条")
                print(f"习惯记录: {summary['habits_count']} 个")
                print(f"决策记录: {summary['decisions_count']} 个")
                print(f"任务记录: {summary['tasks_count']} 个")
                print(f"\n📈 最近7天活动:")
                print(f"  对话: {recent['recent_conversations']} 条")
                print(f"  习惯: {recent['recent_habits']} 个")
                print(f"  决策: {recent['recent_decisions']} 个")
                print(f"  任务: {recent['recent_tasks']} 个")
                
                # 显示话题偏好
                if summary['preferred_topics']:
                    print(f"\n🎯 话题偏好:")
                    for topic, count in summary['preferred_topics'].items():
                        print(f"  {topic}: {count} 次")
                
                continue
            
            elif not user_input:
                continue
            
            # 记录并分析对话
            conversation = memory.record_conversation(user_input)
            
            # 显示分析结果
            print(f"\n📝 系统分析:")
            print(f"   类型: {conversation['analysis']['type']}")
            print(f"   情感: {conversation['analysis']['sentiment']}")
            print(f"   摘要: {conversation['summary']}")
            
            # 如果有提取到具体信息，显示出来
            if conversation['analysis']['habits']:
                print(f"\n📅 识别的习惯:")
                for habit in conversation['analysis']['habits']:
                    print(f"   - {habit['text']}")
            
            if conversation['analysis']['decisions']:
                print(f"\n🤔 识别的决策:")
                for decision in conversation['analysis']['decisions']:
                    print(f"   - {decision['text']}")
            
            if conversation['analysis']['tasks']:
                print(f"\n✅ 识别的任务:")
                for task in conversation['analysis']['tasks']:
                    print(f"   - {task['text']}")
        
        except KeyboardInterrupt:
            print("\n\n系统被中断，正在保存数据...")
            memory.stop()
            break
        except Exception as e:
            print(f"发生错误: {e}")
            continue


if __name__ == "__main__":
    # 创建开机自启动脚本
    startup_script = create_startup_script()
    print(f"✓ 已创建开机启动脚本: {startup_script}")
    print("💡 设置开机自启动方法:")
    print("1. 按 Win+R 输入 'shell:startup'")
    print("2. 将上面的 .bat 文件复制到启动文件夹")
    print("3. 重启电脑即可自动启动")
    print("-" * 50)
    
    main()