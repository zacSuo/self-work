#!/usr/bin/env python3
"""
简化的记忆系统 - 命令行版本
无需安装Flask依赖，直接在命令行使用
"""

import json
import datetime
import os
from typing import Dict, List, Any, Optional

class SimpleMemorySystem:
    """简化的记忆系统"""
    
    def __init__(self, storage_path: str = "private_data/data/simple_memory_data.json"):
        self.storage_path = storage_path
        self.data = {
            'habits': [],
            'work_styles': [],
            'decisions': [],
            'tasks': []
        }
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"✓ 加载了 {len(self.data['habits'])} 个习惯, {len(self.data['work_styles'])} 个工作方式, "
                      f"{len(self.data['decisions'])} 个决策, {len(self.data['tasks'])} 个任务")
            except Exception as e:
                print(f"✗ 加载数据失败: {e}")
        else:
            print("✓ 创建新的数据文件")
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("✓ 数据保存成功")
        except Exception as e:
            print(f"✗ 保存失败: {e}")
    
    def add_habit(self, name, description, frequency, priority=5):
        """添加习惯"""
        habit = {
            'name': name,
            'description': description,
            'frequency': frequency,
            'priority': priority,
            'created_at': datetime.datetime.now().isoformat(),
            'last_practiced': datetime.datetime.now().isoformat(),
            'success_rate': 0.0
        }
        self.data['habits'].append(habit)
        self.save_data()
        print(f"✓ 习惯 '{name}' 添加成功")
    
    def add_work_style(self, category, description, effectiveness=7, tools=None):
        """添加工作方式"""
        work_style = {
            'category': category,
            'description': description,
            'effectiveness': effectiveness,
            'preferred_tools': tools or [],
            'created_at': datetime.datetime.now().isoformat()
        }
        self.data['work_styles'].append(work_style)
        self.save_data()
        print(f"✓ 工作方式 '{category}' 添加成功")
    
    def record_decision(self, decision_type, description, outcome, confidence=7, lessons=""):
        """记录决策"""
        decision = {
            'decision_type': decision_type,
            'description': description,
            'outcome': outcome,
            'confidence_level': confidence,
            'timestamp': datetime.datetime.now().isoformat(),
            'lessons_learned': lessons
        }
        self.data['decisions'].append(decision)
        self.save_data()
        print(f"✓ 决策记录成功")
    
    def add_task(self, title, description, priority="medium", deadline=None):
        """添加任务"""
        if not deadline:
            deadline = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        
        task = {
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'pending',
            'deadline': deadline,
            'created_at': datetime.datetime.now().isoformat(),
            'completed_at': None
        }
        self.data['tasks'].append(task)
        self.save_data()
        print(f"✓ 任务 '{title}' 添加成功")
    
    def show_summary(self):
        """显示摘要"""
        print("\n" + "="*50)
        print("📊 记忆系统摘要")
        print("="*50)
        
        habits_count = len(self.data['habits'])
        work_styles_count = len(self.data['work_styles'])
        decisions_count = len(self.data['decisions'])
        tasks_count = len(self.data['tasks'])
        
        completed_tasks = len([t for t in self.data['tasks'] if t.get('status') == 'completed'])
        completion_rate = (completed_tasks / tasks_count * 100) if tasks_count > 0 else 0
        
        print(f"📅 习惯记录: {habits_count} 个")
        print(f"💼 工作方式: {work_styles_count} 个")
        print(f"🤔 决策记录: {decisions_count} 个")
        print(f"✅ 任务安排: {tasks_count} 个 (完成率: {completion_rate:.1f}%)")
        print("="*50)
    
    def show_habits(self):
        """显示习惯"""
        if not self.data['habits']:
            print("暂无习惯记录")
            return
        
        print("\n📅 您的习惯:")
        for i, habit in enumerate(self.data['habits'], 1):
            print(f"{i}. {habit['name']} - {habit['description']}")
            print(f"   频率: {habit['frequency']} | 优先级: {habit['priority']}/10")
            print(f"   成功率: {habit['success_rate']*100:.1f}%")
            print()
    
    def show_tasks(self):
        """显示任务"""
        if not self.data['tasks']:
            print("暂无任务记录")
            return
        
        print("\n✅ 您的任务:")
        pending_tasks = [t for t in self.data['tasks'] if t.get('status') != 'completed']
        
        for i, task in enumerate(pending_tasks, 1):
            status_icon = "⏳" if task.get('status') == 'in_progress' else "📝"
            print(f"{i}. {status_icon} {task['title']}")
            print(f"   描述: {task['description']}")
            print(f"   优先级: {task['priority']} | 截止: {task['deadline']}")
            print()


def main():
    """主函数"""
    memory = SimpleMemorySystem()
    
    while True:
        print("\n" + "="*50)
        print("🧠 个人记忆系统")
        print("="*50)
        print("1. 查看系统摘要")
        print("2. 添加新习惯")
        print("3. 记录工作方式")
        print("4. 记录决策")
        print("5. 添加任务")
        print("6. 查看习惯")
        print("7. 查看任务")
        print("8. 退出系统")
        print("="*50)
        
        choice = input("请选择操作 (1-8): ").strip()
        
        if choice == '1':
            memory.show_summary()
        
        elif choice == '2':
            print("\n📅 添加新习惯")
            name = input("习惯名称: ").strip()
            description = input("习惯描述: ").strip()
            frequency = input("执行频率 (daily/weekly/monthly): ").strip()
            priority = input("优先级 (1-10, 默认5): ").strip()
            priority = int(priority) if priority.isdigit() else 5
            memory.add_habit(name, description, frequency, priority)
        
        elif choice == '3':
            print("\n💼 记录工作方式")
            category = input("分类 (工作习惯/沟通方式/决策模式等): ").strip()
            description = input("详细描述: ").strip()
            effectiveness = input("有效性评分 (1-10, 默认7): ").strip()
            effectiveness = int(effectiveness) if effectiveness.isdigit() else 7
            memory.add_work_style(category, description, effectiveness)
        
        elif choice == '4':
            print("\n🤔 记录决策")
            decision_type = input("决策类型: ").strip()
            description = input("决策描述: ").strip()
            outcome = input("结果 (positive/negative/neutral): ").strip()
            confidence = input("信心度 (1-10, 默认7): ").strip()
            confidence = int(confidence) if confidence.isdigit() else 7
            lessons = input("经验教训: ").strip()
            memory.record_decision(decision_type, description, outcome, confidence, lessons)
        
        elif choice == '5':
            print("\n✅ 添加任务")
            title = input("任务标题: ").strip()
            description = input("任务描述: ").strip()
            priority = input("优先级 (low/medium/high, 默认medium): ").strip() or "medium"
            deadline = input("截止日期 (YYYY-MM-DD, 默认7天后): ").strip()
            memory.add_task(title, description, priority, deadline or None)
        
        elif choice == '6':
            memory.show_habits()
        
        elif choice == '7':
            memory.show_tasks()
        
        elif choice == '8':
            print("\n感谢使用记忆系统！数据已保存。")
            break
        
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    print("🧠 欢迎使用个人记忆系统（命令行版）")
    print("此版本无需安装额外依赖，可直接使用")
    main()