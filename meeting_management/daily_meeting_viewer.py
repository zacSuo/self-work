"""
每日会议查看器 - 简洁实用版本
"""

import datetime

def get_daily_meetings():
    """获取每日固定会议安排"""
    
    # 今天的日期和星期
    today = datetime.datetime.now()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = day_names[today.weekday()]
    date_str = today.strftime("%Y-%m-%d")
    
    # 每日固定会议
    daily_meetings = [
        {"time": "09:10-09:20", "name": "晨曦项目每日站会", "duration": "10分钟", "priority": "高"},
        {"time": "09:20-09:30", "name": "商清项目每日站会", "duration": "10分钟", "priority": "高"},
        {"time": "09:30-09:50", "name": "管理层每日站会", "duration": "20分钟", "priority": "高"}
    ]
    
    # 周一的特殊会议
    monday_meetings = [
        {"time": "09:30-11:00", "name": "公司管理层周例会", "duration": "1.5小时", "priority": "最高"},
        {"time": "11:00-12:00", "name": "机器人讨论会", "duration": "1小时", "priority": "高"}
    ]
    
    # 周三的特殊会议
    wednesday_meetings = [
        {"time": "09:30-10:30", "name": "品质周例会", "duration": "1小时", "priority": "中"}
    ]
    
    # 周五的特殊会议
    friday_meetings = [
        {"time": "11:00-12:00", "name": "商清项目Sprint评审与计划会", "duration": "1小时", "priority": "高"},
        {"time": "16:30-17:30", "name": "晨曦项目Sprint评审与计划会", "duration": "1小时", "priority": "高"},
        {"time": "17:30-18:00", "name": "技术团队回顾与技术分享会", "duration": "30分钟", "priority": "中"}
    ]
    
    # 构建今天的会议列表
    today_meetings = daily_meetings.copy()
    
    if day_name == "Monday":
        today_meetings.extend(monday_meetings)
    elif day_name == "Wednesday":
        today_meetings.extend(wednesday_meetings)
    elif day_name == "Friday":
        today_meetings.extend(friday_meetings)
    
    return {
        "date": date_str,
        "day": day_name,
        "meetings": today_meetings,
        "total_count": len(today_meetings),
        "total_hours": sum(duration_to_hours(m["duration"]) for m in today_meetings)
    }

def duration_to_hours(duration_str):
    """将时长字符串转换为小时数"""
    if "分钟" in duration_str:
        minutes = int(duration_str.replace("分钟", ""))
        return minutes / 60
    elif "小时" in duration_str:
        hours = float(duration_str.replace("小时", ""))
        return hours
    return 0

def get_tomorrow_meetings():
    """获取明天的会议安排"""
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = day_names[tomorrow.weekday()]
    date_str = tomorrow.strftime("%Y-%m-%d")
    
    # 返回同样的格式，但显示明天
    return get_daily_meetings()  # 这只是一个简化的版本

def print_daily_summary():
    """打印每日会议摘要"""
    today_data = get_daily_meetings()
    
    print("机器人研发团队负责人 - 每日会议安排")
    print("="*60)
    print(f"日期: {today_data['date']} ({today_data['day']})")
    print(f"总会议数: {today_data['total_count']}个")
    print(f"总会议时间: {today_data['total_hours']:.1f}小时")
    
    print(f"\n[今日会议安排]")
    print("-"*60)
    
    for i, meeting in enumerate(today_data["meetings"], 1):
        print(f"{i}. {meeting['time']} {meeting['name']}")
        print(f"   时长: {meeting['duration']} | 优先级: {meeting['priority']}")
    
    # 时间分布分析
    work_hours = 8.0  # 工作日8小时
    meeting_hours = today_data["total_hours"]
    work_hours_left = work_hours - meeting_hours
    
    meeting_percent = (meeting_hours / work_hours) * 100
    work_percent = (work_hours_left / work_hours) * 100
    
    print(f"\n[时间分布分析]")
    print("-"*60)
    print(f"会议时间: {meeting_hours:.1f}小时 ({meeting_percent:.1f}%)")
    print(f"工作时间: {work_hours_left:.1f}小时 ({work_percent:.1f}%)")
    
    # 提供建议
    print(f"\n[今日工作建议]")
    print("-"*60)
    
    if today_data["day"] == "Monday":
        print("1. 上午深度工作时间有限，高效处理紧急事务")
        print("2. 管理层周例会是关键，提前准备汇报材料")
        print("3. 机器人讨论会前整理好技术问题")
        print("4. 下午重点跟进会议决议事项")
    elif today_data["day"] == "Friday":
        print("1. 上午准备两个Sprint会议材料")
        print("2. Sprint会议是关键，确保高效产出")
        print("3. 技术分享会前收集团队技术收获")
        print("4. 下班前完成本周总结")
    else:
        print("1. 充分利用上午深度工作时间（08:30-09:10）")
        print("2. 站会要高效，控制在预定时间内")
        print("3. 下午时间可用于深度技术工作")
        print("4. 下班前完成项目跟进和明日规划")
    
    # 显示明天预告
    tomorrow_data = get_tomorrow_meetings()
    print(f"\n[明日预告] {tomorrow_data['date']} ({tomorrow_data['day']})")
    print("-"*60)
    if tomorrow_data["meetings"]:
        for meeting in tomorrow_data["meetings"][:3]:  # 只显示前3个
            print(f"- {meeting['time']} {meeting['name']}")
        if len(tomorrow_data["meetings"]) > 3:
            print(f"  ... 还有{len(tomorrow_data['meetings'])-3}个会议")
    else:
        print("明日无固定会议安排")
    
    print(f"\n" + "="*60)
    print("建议每天早上运行此程序查看当日会议安排。")

def main():
    """主函数"""
    print_daily_summary()

if __name__ == "__main__":
    main()