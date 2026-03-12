"""
集成式每日工作计划系统 - 结合技术工作、会议安排和项目管理
"""

import datetime
import json
import os

def load_technical_events():
    """加载技术事件"""
    data_file = "technical_events.json"
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        # 获取最近的技术里程碑
        recent_events = []
        for event in events:
            event_date = datetime.datetime.fromisoformat(event['timestamp']).date()
            today_date = datetime.datetime.now().date()
            
            # 最近7天的事件
            if (today_date - event_date).days <= 7:
                recent_events.append(event)
        
        return recent_events
    return []

def create_tomorrow_plan():
    """创建明日综合计划"""
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 加载最近的技术事件
    recent_events = load_technical_events()
    
    # 明日会议安排
    meetings = [
        {
            "name": "商清项目Sprint评审与计划会",
            "time": "09:30-10:30",
            "duration": 1.0,
            "priority": "高",
            "key_topics": ["上周完成情况", "技术问题", "下周规划", "风险评估"],
            "preparation": ["任务清单", "技术问题点", "优先级列表", "风险报告"]
        },
        {
            "name": "晨曦项目Sprint评审与计划会",
            "time": "14:00-15:00",
            "duration": 1.0,
            "priority": "高",
            "key_topics": ["底盘控制算法", "硬件集成", "技术路线", "测试计划"],
            "preparation": ["算法进展报告", "硬件问题清单", "路线图更新", "测试分析"]
        },
        {
            "name": "技术团队回顾与技术分享会",
            "time": "17:00-17:30",
            "duration": 0.5,
            "priority": "中",
            "key_topics": ["技术成果总结", "问题与方案", "经验分享", "学习计划"],
            "preparation": ["成果总结", "问题整理", "分享内容", "学习建议"]
        }
    ]
    
    # 基于技术事件的工作重点
    work_focus = []
    for event in recent_events:
        if "底盘积尘" in event["title"] or "底盘" in event["title"]:
            work_focus.append({
                "priority": "高",
                "topic": "底盘积尘解决方案跟进",
                "actions": [
                    "检查方案实施进展",
                    "安排测试验证计划",
                    "整理技术文档",
                    "团队内部分享"
                ]
            })
    
    # 如果无技术事件，添加默认工作重点
    if not work_focus:
        work_focus = [
            {
                "priority": "高",
                "topic": "机器人软件架构优化",
                "actions": ["架构评审", "性能优化", "代码重构", "文档更新"]
            },
            {
                "priority": "中",
                "topic": "技术团队能力建设",
                "actions": ["培训计划", "知识分享", "代码审查", "技术调研"]
            }
        ]
    
    # 综合计划
    plan = {
        "date": tomorrow,
        "total_meeting_hours": sum(m["duration"] for m in meetings),
        "meetings": meetings,
        "work_focus": work_focus,
        "time_blocks": [
            {"time": "08:30-09:30", "type": "深度工作", "task": "邮件处理和会议准备"},
            {"time": "09:30-10:30", "type": "会议", "task": "商清项目Sprint会"},
            {"time": "10:30-12:00", "type": "技术工作", "task": "会议决议跟进和技术问题处理"},
            {"time": "13:30-14:00", "type": "会议准备", "task": "晨曦项目会议资料准备"},
            {"time": "14:00-15:00", "type": "会议", "task": "晨曦项目Sprint会"},
            {"time": "15:00-17:00", "type": "项目管理", "task": "项目进度跟进和资源协调"},
            {"time": "17:00-17:30", "type": "会议", "task": "技术团队回顾会"},
            {"time": "17:30-18:00", "type": "总结规划", "task": "今日总结和明日规划"}
        ]
    }
    
    return plan

def print_comprehensive_plan():
    """打印综合计划"""
    plan = create_tomorrow_plan()
    
    print("机器人研发团队负责人 - 明日综合工作计划")
    print("="*70)
    print(f"日期: {plan['date']}")
    print(f"总会议时间: {plan['total_meeting_hours']}小时")
    print(f"可用工作时间: {8.0 - plan['total_meeting_hours']}小时")
    
    print(f"\n[会议安排]")
    print("-"*70)
    for meeting in plan["meetings"]:
        print(f"1. {meeting['name']}")
        print(f"   时间: {meeting['time']} | 优先级: {meeting['priority']}")
        print(f"   关键议题: {', '.join(meeting['key_topics'])}")
        print(f"   准备事项: {', '.join(meeting['preparation'])}")
        print()
    
    print(f"\n[工作重点]")
    print("-"*70)
    for i, focus in enumerate(plan["work_focus"], 1):
        print(f"{i}. {focus['topic']} (优先级: {focus['priority']})")
        for action in focus["actions"]:
            print(f"   - {action}")
        print()
    
    print(f"\n[时间安排]")
    print("-"*70)
    for block in plan["time_blocks"]:
        print(f"{block['time']:15} [{block['type']:10}] {block['task']}")
    
    print(f"\n[执行建议]")
    print("-"*70)
    print("1. 上午深度工作时段至关重要，确保无打扰")
    print("2. 每个会议前预留准备时间，提高会议效率")
    print("3. 关注技术事件跟进，特别是底盘积尘方案")
    print("4. 下班前完成总结，为次日做好准备")
    print("5. 保持工作节奏，避免会议过度占用工作时间")
    
    print(f"\n[风险提示]")
    print("-"*70)
    print("1. 会议时间占比31.2%，需确保会议高效")
    print("2. 多个项目并行，注意资源分配平衡")
    print("3. 技术分享需要提前收集和整理内容")
    print("4. 深度工作时间有限，需合理安排技术攻关")
    
    print(f"\n" + "="*70)
    print("明日计划已生成。建议今晚完成必要准备，确保明日高效执行。")

def save_plan_to_file():
    """保存计划到文件"""
    plan = create_tomorrow_plan()
    plan_file = f"daily_plan_{plan['date']}.json"
    
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"[信息] 计划已保存到: {plan_file}")
    return plan_file

def main():
    """主函数"""
    print_comprehensive_plan()
    plan_file = save_plan_to_file()
    
    # 显示技术事件摘要
    events = load_technical_events()
    if events:
        print(f"\n[近期技术事件参考]")
        print("-"*70)
        for i, event in enumerate(events[:2], 1):  # 显示最近2个事件
            print(f"{i}. {event['title']}")
            print(f"   日期: {event['date']} | 类型: {event['type']}")
            print(f"   简要: {event['description'][:60]}...")

if __name__ == "__main__":
    main()