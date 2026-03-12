#!/usr/bin/env python3
"""
机器人团队负责人每日规划启动脚本
每天早上运行此脚本获取当日工作优先级安排
"""

import sys
import os
sys.path.append('.')

from robot_team_priority_system import DailyPlanner, QuickTaskInput, Task, TaskType, PriorityLevel
import datetime

def show_daily_plan():
    """显示今日规划"""
    print("\n" + "="*60)
    print("🤖 机器人研发团队负责人 - 每日工作规划")
    print("="*60)
    
    planner = DailyPlanner()
    report = planner.generate_summary_report()
    print(report)

def quick_add_task():
    """快速添加任务"""
    print("\n📝 快速任务录入 (输入'q'退出)")
    print("-" * 40)
    
    while True:
        task_text = input("请输入任务描述: ").strip()
        if task_text.lower() == 'q':
            break
        
        if not task_text:
            print("任务描述不能为空，请重新输入")
            continue
        
        # 解析自然语言
        task = QuickTaskInput.parse_natural_language(task_text)
        if task:
            planner = DailyPlanner()
            planner.add_task(task)
            print(f"✅ 任务已添加: {task.title}")
            print(f"   类型: {task.task_type.value}")
            print(f"   优先级: {task.priority.value}")
            print(f"   预估时间: {task.estimated_hours}小时")
        else:
            print("❌ 无法解析任务描述，请重试")

def view_task_details():
    """查看任务详情"""
    planner = DailyPlanner()
    
    if not planner.tasks:
        print("暂无任务数据")
        return
    
    print(f"\n📋 任务列表 (共{len(planner.tasks)}个)")
    print("-" * 60)
    
    pending_tasks = [t for t in planner.tasks if t.status != "completed"]
    
    for i, task in enumerate(pending_tasks, 1):
        status_icon = "🟢" if task.status == "completed" else "🟡" if task.status == "in_progress" else "⚪"
        print(f"{i}. {status_icon} [{task.task_type.value}] {task.title}")
        print(f"   优先级: {task.priority.value} | 状态: {task.status} | 进度: {task.progress_percent}%")
        print(f"   预估: {task.estimated_hours}小时 | 难度: {'★' * task.difficulty_level}")
        if task.deadline:
            print(f"   截止: {task.deadline}")
        print()

def update_task_status():
    """更新任务状态"""
    planner = DailyPlanner()
    
    pending_tasks = [t for t in planner.tasks if t.status != "completed"]
    
    if not pending_tasks:
        print("暂无需要更新的任务")
        return
    
    print("\n🔄 更新任务状态")
    print("-" * 40)
    
    for i, task in enumerate(pending_tasks, 1):
        print(f"{i}. {task.title} [{task.status}]")
    
    try:
        choice = int(input("\n选择要更新的任务编号: "))
        if 1 <= choice <= len(pending_tasks):
            task = pending_tasks[choice-1]
            print(f"\n当前任务: {task.title}")
            print(f"当前状态: {task.status}")
            print(f"当前进度: {task.progress_percent}%")
            
            new_status = input("输入新状态 (pending/in_progress/completed/blocked): ").strip().lower()
            if new_status in ["pending", "in_progress", "completed", "blocked"]:
                task.status = new_status
                
                if new_status == "completed":
                    task.progress_percent = 100
                    task.completed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    progress = input("输入进度百分比 (0-100): ").strip()
                    if progress.isdigit():
                        task.progress_percent = min(100, max(0, int(progress)))
                
                planner._save_tasks()
                print("✅ 任务状态已更新")
            else:
                print("❌ 无效的状态")
        else:
            print("❌ 无效的选择")
    except ValueError:
        print("❌ 请输入有效的数字")

def show_weekly_preview():
    """显示周度预览"""
    planner = DailyPlanner()
    
    # 按类型统计
    type_stats = {}
    for task in planner.tasks:
        if task.status != "completed":
            task_type = task.task_type.value
            type_stats[task_type] = type_stats.get(task_type, 0) + 1
    
    print("\n📊 本周任务概览")
    print("-" * 60)
    
    if type_stats:
        for task_type, count in type_stats.items():
            print(f"• {task_type}: {count}个任务")
    else:
        print("暂无待处理任务")
    
    # 即将到期的任务
    today = datetime.datetime.now()
    upcoming_tasks = []
    for task in planner.tasks:
        if task.deadline and task.status != "completed":
            try:
                deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d")
                days_left = (deadline - today).days
                if 0 <= days_left <= 7:
                    upcoming_tasks.append((task, days_left))
            except:
                pass
    
    if upcoming_tasks:
        print("\n⏰ 本周即将到期任务:")
        for task, days_left in sorted(upcoming_tasks, key=lambda x: x[1]):
            status_icon = "🔴" if days_left <= 1 else "🟡" if days_left <= 3 else "🟢"
            print(f"  {status_icon} {task.title} - 还剩{days_left}天")

def main_menu():
    """主菜单"""
    while True:
        print("\n" + "="*60)
        print("🤖 机器人团队负责人工作规划系统")
        print("="*60)
        print("1. 📅 查看今日工作规划")
        print("2. 📝 快速添加任务")
        print("3. 📋 查看任务列表")
        print("4. 🔄 更新任务状态")
        print("5. 📊 本周任务概览")
        print("6. 💾 保存并退出")
        print("0. 🚪 直接退出")
        print("-" * 60)
        
        choice = input("请选择操作 (0-6): ").strip()
        
        if choice == "1":
            show_daily_plan()
        elif choice == "2":
            quick_add_task()
        elif choice == "3":
            view_task_details()
        elif choice == "4":
            update_task_status()
        elif choice == "5":
            show_weekly_preview()
        elif choice == "6":
            print("💾 数据已自动保存")
            print("👋 再见！祝您工作顺利！")
            break
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    # 检查数据文件是否存在，如果不存在创建示例数据
    data_file = "robot_team_tasks.json"
    if not os.path.exists(data_file):
        print("[文件] 初始化系统，创建示例任务...")
        # 导入并运行主函数创建示例数据
        from robot_team_priority_system import main as init_main
        init_main()
    
    print("[启动] 启动机器人团队负责人工作规划系统...")
    main_menu()