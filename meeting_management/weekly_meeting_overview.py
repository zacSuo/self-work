"""
每周会议概览 - 简洁版本
"""

def print_weekly_overview():
    """打印每周会议概览"""
    
    print("机器人研发团队负责人 - 每周固定会议概览")
    print("="*70)
    
    # 每周会议安排
    weekly_schedule = {
        "Monday": [
            "09:10-09:20 晨曦项目每日站会 (10分钟)",
            "09:20-09:30 商清项目每日站会 (10分钟)",
            "09:30-09:50 管理层每日站会 (20分钟)",
            "09:30-11:00 公司管理层周例会 (1.5小时)",
            "11:00-12:00 机器人讨论会 (1小时)"
        ],
        "Tuesday": [
            "09:10-09:20 晨曦项目每日站会 (10分钟)",
            "09:20-09:30 商清项目每日站会 (10分钟)",
            "09:30-09:50 管理层每日站会 (20分钟)"
        ],
        "Wednesday": [
            "09:10-09:20 晨曦项目每日站会 (10分钟)",
            "09:20-09:30 商清项目每日站会 (10分钟)",
            "09:30-09:50 管理层每日站会 (20分钟)",
            "09:30-10:30 品质周例会 (1小时)"
        ],
        "Thursday": [
            "09:10-09:20 晨曦项目每日站会 (10分钟)",
            "09:20-09:30 商清项目每日站会 (10分钟)",
            "09:30-09:50 管理层每日站会 (20分钟)"
        ],
        "Friday": [
            "09:10-09:20 晨曦项目每日站会 (10分钟)",
            "09:20-09:30 商清项目每日站会 (10分钟)",
            "09:30-09:50 管理层每日站会 (20分钟)",
            "11:00-12:00 商清项目Sprint评审与计划会 (1小时)",
            "16:30-17:30 晨曦项目Sprint评审与计划会 (1小时)",
            "17:30-18:00 技术团队回顾与技术分享会 (30分钟)"
        ]
    }
    
    # 打印每天的安排
    for day, meetings in weekly_schedule.items():
        print(f"\n[{day}]")
        print("-"*40)
        for meeting in meetings:
            print(f"  {meeting}")
    
    # 统计信息
    print(f"\n[每周统计]")
    print("-"*40)
    
    total_meetings = sum(len(meetings) for meetings in weekly_schedule.values())
    print(f"总会议数: {total_meetings}个")
    
    # 计算总时长
    total_hours = 0
    for meetings in weekly_schedule.values():
        for meeting in meetings:
            if "10分钟" in meeting:
                total_hours += 10/60
            elif "20分钟" in meeting:
                total_hours += 20/60
            elif "30分钟" in meeting:
                total_hours += 30/60
            elif "1小时" in meeting:
                total_hours += 1.0
            elif "1.5小时" in meeting:
                total_hours += 1.5
    
    print(f"总会议时间: {total_hours:.1f}小时")
    print(f"平均每天会议: {total_hours/5:.1f}小时")
    
    # 最繁忙的天
    busiest_day = max(weekly_schedule.items(), key=lambda x: len(x[1]))
    print(f"最繁忙的一天: {busiest_day[0]} ({len(busiest_day[1])}个会议)")
    
    # 会议类型分布
    print(f"\n[会议类型分布]")
    print("-"*40)
    print("每日站会: 每天3个，共15个")
    print("管理层会议: 周一1个 + 每天1个，共6个")
    print("技术会议: 周一1个 + 周五1个，共2个")
    print("品质会议: 周三1个")
    print("项目评审会: 周五2个")
    
    # 时间管理建议
    print(f"\n[时间管理建议]")
    print("-"*40)
    print("1. 周一: 上午会议密集，需提前准备")
    print("2. 周二/周四: 会议较少，适合深度技术工作")
    print("3. 周三: 上午有品质会议，安排技术审查")
    print("4. 周五: 会议最多，需提前规划全天安排")
    print("5. 每日: 保护08:30-09:10深度工作时间")
    
    # 使用指南
    print(f"\n[系统使用指南]")
    print("-"*40)
    print("早上查看: python daily_meeting_viewer.py")
    print("每周概览: python weekly_meeting_overview.py")
    print("详细分析: python weekly_meeting_system.py")
    print("明日计划: python integrated_daily_plan.py")
    
    print(f"\n" + "="*70)
    print("系统已就绪，帮助您高效管理每周会议安排。")

def main():
    """主函数"""
    print_weekly_overview()

if __name__ == "__main__":
    main()