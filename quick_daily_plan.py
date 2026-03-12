#!/usr/bin/env python3
"""
机器人研发团队负责人 - 每日工作优先级规划
专为20+人机器人研发团队负责人设计
结合技术攻关（软硬件/算法/结构）与项目管理双重职责
"""

import json
import os
import datetime

def create_sample_data():
    """创建示例任务数据"""
    sample_tasks = [
        {
            "id": "T001",
            "title": "机器人运动控制算法优化",
            "type": "算法研发攻关",
            "priority": "高优先级",
            "description": "优化四足机器人的步态控制算法，提升运动稳定性",
            "estimated_hours": 6.0,
            "difficulty": 4,
            "impact": 4,
            "deadline": "2026-03-15",
            "status": "pending",
            "progress": 0
        },
        {
            "id": "T002",
            "title": "项目第二阶段里程碑评审",
            "type": "项目关键节点",
            "priority": "关键紧急",
            "description": "准备第二阶段交付物，组织客户评审会议",
            "estimated_hours": 4.0,
            "difficulty": 3,
            "impact": 5,
            "deadline": "2026-03-14",
            "status": "pending",
            "progress": 0
        },
        {
            "id": "T003",
            "title": "硬件团队技术瓶颈攻关",
            "type": "硬件技术攻关",
            "priority": "高优先级",
            "description": "解决电机驱动器过热问题，协调硬件团队技术攻关",
            "estimated_hours": 3.0,
            "difficulty": 4,
            "impact": 3,
            "status": "in_progress",
            "progress": 30
        },
        {
            "id": "T004",
            "title": "团队周例会和技术分享",
            "type": "团队管理",
            "priority": "中等优先级",
            "description": "组织团队周例会，安排技术分享内容",
            "estimated_hours": 2.0,
            "difficulty": 2,
            "impact": 3,
            "status": "pending",
            "progress": 0
        },
        {
            "id": "T005",
            "title": "新型传感器技术调研",
            "type": "技术创新探索",
            "priority": "低优先级",
            "description": "调研最新的激光雷达传感器技术，评估可行性",
            "estimated_hours": 5.0,
            "difficulty": 3,
            "impact": 2,
            "status": "pending",
            "progress": 0
        },
        {
            "id": "T006",
            "title": "软件架构重构方案评审",
            "type": "软件技术攻关",
            "priority": "中等优先级",
            "description": "评审软件架构重构方案，确保系统可扩展性",
            "estimated_hours": 3.0,
            "difficulty": 4,
            "impact": 4,
            "status": "pending",
            "progress": 0
        },
        {
            "id": "T007",
            "title": "与供应商技术沟通会议",
            "type": "外部沟通",
            "priority": "中等优先级",
            "description": "与核心部件供应商讨论技术规格和交付时间",
            "estimated_hours": 2.0,
            "difficulty": 2,
            "impact": 3,
            "status": "pending",
            "progress": 0
        }
    ]
    
    return sample_tasks

def calculate_priority_score(task):
    """计算任务优先级分数"""
    # 优先级基础分
    priority_scores = {
        "关键紧急": 90,
        "高优先级": 75,
        "中等优先级": 60,
        "低优先级": 45,
        "待办事项": 30
    }
    
    # 类型调整分
    type_adj = {
        "项目关键节点": 20,
        "风险管控": 18,
        "团队管理": 15,
        "硬件技术攻关": 12,
        "算法研发攻关": 12,
        "软件技术攻关": 10,
        "关键决策": 10,
        "结构设计攻关": 8,
        "外部沟通": 6,
        "技术创新探索": 5
    }
    
    base_score = priority_scores.get(task["priority"], 50)
    type_score = type_adj.get(task["type"], 0)
    
    # 难度调整
    difficulty_adj = task["difficulty"] * 3
    
    # 影响调整
    impact_adj = task["impact"] * 4
    
    # 截止日期调整
    deadline_adj = 0
    if "deadline" in task and task["deadline"]:
        try:
            deadline = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d")
            today = datetime.datetime.now()
            days_left = (deadline - today).days
            
            if days_left < 0:
                deadline_adj = 25
            elif days_left <= 1:
                deadline_adj = 20
            elif days_left <= 3:
                deadline_adj = 15
            elif days_left <= 7:
                deadline_adj = 10
        except:
            pass
    
    # 状态调整
    status_adj = 0
    if task["status"] == "blocked":
        status_adj = 15
    elif task["status"] == "in_progress":
        status_adj = 8
    
    total_score = base_score + type_score + difficulty_adj + impact_adj + deadline_adj + status_adj
    
    return min(100, total_score)

def generate_daily_plan(tasks):
    """生成每日规划"""
    today = datetime.datetime.now()
    
    # 筛选待处理任务
    pending_tasks = [t for t in tasks if t["status"] != "completed"]
    
    # 计算每个任务的优先级分数
    for task in pending_tasks:
        task["priority_score"] = calculate_priority_score(task)
    
    # 按优先级排序
    sorted_tasks = sorted(pending_tasks, key=lambda x: x["priority_score"], reverse=True)
    
    # 确定关键任务（前25%）
    critical_count = max(1, len(sorted_tasks) // 4)
    critical_tasks = sorted_tasks[:critical_count]
    
    # 确定今日可完成的任务（基于8小时工作日）
    daily_capacity = 8
    daily_tasks = []
    time_used = 0
    
    for task in sorted_tasks:
        if time_used + task["estimated_hours"] <= daily_capacity:
            daily_tasks.append(task)
            time_used += task["estimated_hours"]
        else:
            break
    
    # 按类型统计
    type_stats = {}
    tech_tasks = 0
    project_tasks = 0
    team_tasks = 0
    
    for task in pending_tasks:
        task_type = task["type"]
        type_stats[task_type] = type_stats.get(task_type, 0) + 1
        
        # 分类统计
        if task_type in ["硬件技术攻关", "软件技术攻关", "算法研发攻关", "结构设计攻关"]:
            tech_tasks += 1
        elif task_type in ["项目关键节点", "风险管控", "关键决策"]:
            project_tasks += 1
        elif task_type in ["团队管理", "外部沟通", "技术创新探索"]:
            team_tasks += 1
    
    # 计算时间分配比例
    total_categorized = tech_tasks + project_tasks + team_tasks
    if total_categorized > 0:
        tech_ratio = tech_tasks / total_categorized
        project_ratio = project_tasks / total_categorized
        team_ratio = team_tasks / total_categorized
    else:
        tech_ratio = project_ratio = team_ratio = 0.33
    
    return {
        "date": today.strftime("%Y-%m-%d"),
        "pending_count": len(pending_tasks),
        "critical_count": len(critical_tasks),
        "daily_count": len(daily_tasks),
        "estimated_hours": round(time_used, 1),
        "critical_tasks": critical_tasks,
        "daily_tasks": daily_tasks,
        "type_stats": type_stats,
        "focus_ratio": {
            "技术攻关": round(tech_ratio, 2),
            "项目管理": round(project_ratio, 2),
            "团队管理": round(team_ratio, 2)
        }
    }

def print_daily_plan(plan):
    """打印每日规划"""
    print("\n" + "=" * 80)
    print("机器人研发团队负责人 - 每日工作优先级安排")
    print("日期:", plan["date"])
    print("=" * 80)
    
    print(f"\n[概览]")
    print(f"  待处理任务总数: {plan['pending_count']} 个")
    print(f"  关键任务数量: {plan['critical_count']} 个")
    print(f"  今日推荐完成: {plan['daily_count']} 个")
    print(f"  预计工作时间: {plan['estimated_hours']} 小时")
    
    print(f"\n[时间分配建议]")
    print(f"  技术攻关: {plan['focus_ratio']['技术攻关']*100:.0f}%")
    print(f"  项目管理: {plan['focus_ratio']['项目管理']*100:.0f}%")
    print(f"  团队管理: {plan['focus_ratio']['团队管理']*100:.0f}%")
    
    if plan["critical_tasks"]:
        print(f"\n[关键任务 - 必须优先处理]")
        for i, task in enumerate(plan["critical_tasks"], 1):
            status_icon = "[进行中]" if task["status"] == "in_progress" else "[待处理]"
            print(f"  {i}. {status_icon} {task['title']}")
            print(f"     类型: {task['type']} | 优先级: {task['priority']}")
            print(f"     优先级分: {task['priority_score']:.1f} | 预估: {task['estimated_hours']}小时")
            if "deadline" in task and task["deadline"]:
                print(f"     截止: {task['deadline']}")
    
    if plan["daily_tasks"]:
        print(f"\n[今日推荐任务安排]")
        time_slots = [
            "09:00-10:30 (技术攻关)",
            "10:30-12:00 (技术攻关)", 
            "13:30-15:00 (会议协调)",
            "15:00-16:30 (项目管理)",
            "16:30-18:00 (灵活处理)"
        ]
        
        for i, task in enumerate(plan["daily_tasks"]):
            time_slot = time_slots[i] if i < len(time_slots) else "灵活安排"
            print(f"  {i+1}. [{time_slot}] {task['title']}")
            print(f"     类型: {task['type']} | 优先级分: {task['priority_score']:.1f}")
    
    if plan["type_stats"]:
        print(f"\n[任务类型分布]")
        for task_type, count in plan["type_stats"].items():
            print(f"  - {task_type}: {count}个")
    
    print(f"\n[今日工作节奏建议]")
    print("  1. 09:00-10:30: 处理最复杂的技术问题（头脑最清醒时）")
    print("  2. 10:30-12:00: 继续技术攻关或技术评审")
    print("  3. 13:30-15:00: 团队会议、跨部门协调")
    print("  4. 15:00-16:30: 项目进度跟踪、风险管控")
    print("  5. 16:30-18:00: 处理突发问题、规划明日工作")
    
    print(f"\n[特别提醒]")
    print("  * 作为团队负责人，您的30%时间应用于团队赋能")
    print("  * 每天至少预留1小时处理突发技术问题")
    print("  * 复杂技术决策建议在上午进行")
    print("  * 保持与技术团队的日常沟通（站立会/技术同步）")
    
    print("\n" + "=" * 80)
    print("提示：一次只专注于一个关键任务，避免多任务切换")
    print("=" * 80)

def main():
    """主函数"""
    print("[系统] 机器人研发团队负责人每日工作规划系统")
    print("[版本] 1.0 - 专为20+人团队负责人设计")
    print("[特点] 结合技术攻关与项目管理双重职责")
    print("-" * 80)
    
    # 创建示例数据
    tasks = create_sample_data()
    
    # 生成今日规划
    plan = generate_daily_plan(tasks)
    
    # 打印规划
    print_daily_plan(plan)
    
    # 添加快速操作提示
    print("\n[快速操作指南]")
    print("  1. 每天早上查看此规划，明确当日重点")
    print("  2. 根据时间分配建议安排工作节奏")
    print("  3. 优先处理'关键任务'，确保项目节点")
    print("  4. 每天结束前花15分钟更新任务状态")
    print("  5. 每周五下午进行任务复盘和下周规划")
    
    print("\n[文件保存位置]")
    print("  任务数据文件: d:/code/workbuddy/robot_tasks.json")
    print("  每日规划文件: d:/code/workbuddy/daily_plan_{}.txt".format(plan["date"]))

if __name__ == "__main__":
    main()