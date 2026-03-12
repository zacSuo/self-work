"""
机器人研发团队负责人 - 每周固定会议管理系统
"""

import datetime
from typing import List, Dict, Any
from enum import Enum

class WeekDay(Enum):
    """星期枚举"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class MeetingCategory(Enum):
    """会议分类"""
    DAILY_STANDUP = "每日站会"
    PROJECT_REVIEW = "项目评审会"
    MANAGEMENT = "管理层会议"
    TECHNICAL = "技术会议"
    QUALITY = "品质会议"
    PLANNING = "计划会议"

class WeeklyMeetingManager:
    """每周会议管理器"""
    
    def __init__(self):
        self.meetings = self._initialize_weekly_meetings()
    
    def _initialize_weekly_meetings(self) -> Dict[str, List[Dict[str, Any]]]:
        """初始化每周固定会议"""
        
        meetings_by_day = {
            "Monday": [],    # 周一
            "Tuesday": [],   # 周二
            "Wednesday": [], # 周三
            "Thursday": [],  # 周四
            "Friday": [],    # 周五
            "Saturday": [],  # 周六
            "Sunday": []     # 周日
        }
        
        # ========== 每日固定会议 ==========
        daily_meetings = [
            {
                "name": "晨曦项目每日站会",
                "time": "09:10-09:20",
                "duration": 0.17,  # 10分钟
                "day": "All",  # 每天
                "category": MeetingCategory.DAILY_STANDUP.value,
                "participants": ["项目负责人", "硬件工程师", "软件工程师", "算法工程师"],
                "purpose": "快速同步项目进展，识别阻塞问题",
                "key_topics": ["昨日完成", "今日计划", "阻塞问题"],
                "priority": "高",
                "recurring": True
            },
            {
                "name": "商清项目每日站会",
                "time": "09:20-09:30",
                "duration": 0.17,  # 10分钟
                "day": "All",  # 每天
                "category": MeetingCategory.DAILY_STANDUP.value,
                "participants": ["项目负责人", "技术骨干", "产品经理", "测试负责人"],
                "purpose": "快速同步项目进展，协调资源",
                "key_topics": ["进展同步", "问题协调", "资源分配"],
                "priority": "高",
                "recurring": True
            },
            {
                "name": "管理层每日站会",
                "time": "09:30-09:50",
                "duration": 0.33,  # 20分钟
                "day": "All",  # 每天
                "category": MeetingCategory.MANAGEMENT.value,
                "participants": ["团队负责人", "项目经理", "技术主管"],
                "purpose": "管理层快速同步，决策协调",
                "key_topics": ["战略协调", "资源决策", "风险管控"],
                "priority": "高",
                "recurring": True
            }
        ]
        
        # 将每日会议添加到所有工作日（周一到周五）
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            meetings_by_day[day].extend(daily_meetings)
        
        # ========== 周一会议 ==========
        monday_meetings = [
            {
                "name": "公司管理层周例会",
                "time": "09:30-11:00",
                "duration": 1.5,  # 1.5小时
                "day": "Monday",
                "category": MeetingCategory.MANAGEMENT.value,
                "participants": ["公司管理层", "各部门负责人"],
                "purpose": "公司层面战略协调和决策",
                "key_topics": ["公司战略", "跨部门协调", "资源分配", "重大决策"],
                "priority": "最高",
                "recurring": True
            },
            {
                "name": "机器人讨论会",
                "time": "11:00-12:00",
                "duration": 1.0,  # 1小时
                "day": "Monday",
                "category": MeetingCategory.TECHNICAL.value,
                "participants": ["机器人团队全体", "相关专家"],
                "purpose": "机器人技术深度讨论和创新研讨",
                "key_topics": ["技术难题", "创新方案", "技术路线", "研究进展"],
                "priority": "高",
                "recurring": True
            }
        ]
        meetings_by_day["Monday"].extend(monday_meetings)
        
        # ========== 周三会议 ==========
        wednesday_meetings = [
            {
                "name": "品质周例会",
                "time": "09:30-10:30",
                "duration": 1.0,  # 1小时
                "day": "Wednesday",
                "category": MeetingCategory.QUALITY.value,
                "participants": ["质量负责人", "测试团队", "开发代表"],
                "purpose": "质量问题和改进措施讨论",
                "key_topics": ["质量问题", "改进措施", "测试计划", "质量目标"],
                "priority": "中",
                "recurring": True
            }
        ]
        meetings_by_day["Wednesday"].extend(wednesday_meetings)
        
        # ========== 周五会议 ==========
        friday_meetings = [
            {
                "name": "商清项目Sprint评审与计划会",
                "time": "11:00-12:00",
                "duration": 1.0,  # 1小时
                "day": "Friday",
                "category": MeetingCategory.PROJECT_REVIEW.value,
                "participants": ["项目负责人", "技术骨干", "产品经理", "测试负责人"],
                "purpose": "评审Sprint完成情况，规划下一阶段工作",
                "key_topics": ["Sprint评审", "下周计划", "技术问题", "风险评估"],
                "priority": "高",
                "recurring": True
            },
            {
                "name": "晨曦项目Sprint评审与计划会",
                "time": "16:30-17:30",
                "duration": 1.0,  # 1小时
                "day": "Friday",
                "category": MeetingCategory.PROJECT_REVIEW.value,
                "participants": ["项目负责人", "硬件工程师", "软件工程师", "算法工程师"],
                "purpose": "评审机器人项目进展，规划技术攻关方向",
                "key_topics": ["技术进展", "硬件集成", "算法优化", "测试计划"],
                "priority": "高",
                "recurring": True
            },
            {
                "name": "技术团队回顾与技术分享会",
                "time": "17:30-18:00",
                "duration": 0.5,  # 0.5小时
                "day": "Friday",
                "category": MeetingCategory.TECHNICAL.value,
                "participants": ["全体技术人员", "实习生"],
                "purpose": "技术总结和经验分享，促进团队成长",
                "key_topics": ["技术总结", "经验分享", "问题复盘", "学习计划"],
                "priority": "中",
                "recurring": True
            }
        ]
        meetings_by_day["Friday"].extend(friday_meetings)
        
        # 按时间排序每天会议
        for day in meetings_by_day:
            meetings_by_day[day] = sorted(meetings_by_day[day], key=lambda x: x["time"])
        
        return meetings_by_day
    
    def get_today_meetings(self, today_date=None) -> List[Dict[str, Any]]:
        """获取今天的会议安排"""
        if today_date is None:
            today_date = datetime.datetime.now()
        
        # 获取星期几
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today_name = day_names[today_date.weekday()]
        
        return self.meetings.get(today_name, [])
    
    def get_tomorrow_meetings(self) -> List[Dict[str, Any]]:
        """获取明天的会议安排"""
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
        return self.get_today_meetings(tomorrow_date)
    
    def get_weekly_summary(self) -> Dict[str, Any]:
        """获取每周会议摘要"""
        weekly_summary = {
            "total_meetings": 0,
            "total_hours": 0,
            "by_category": {},
            "by_day": {}
        }
        
        # 只计算工作日（周一至周五）
        work_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        for day in work_days:
            day_meetings = self.meetings[day]
            weekly_summary["by_day"][day] = {
                "meeting_count": len(day_meetings),
                "total_hours": sum(m["duration"] for m in day_meetings)
            }
            
            # 分类统计
            for meeting in day_meetings:
                category = meeting["category"]
                if category not in weekly_summary["by_category"]:
                    weekly_summary["by_category"][category] = {
                        "count": 0,
                        "hours": 0
                    }
                
                weekly_summary["by_category"][category]["count"] += 1
                weekly_summary["by_category"][category]["hours"] += meeting["duration"]
                
                weekly_summary["total_meetings"] += 1
                weekly_summary["total_hours"] += meeting["duration"]
        
        return weekly_summary
    
    def get_busiest_day(self) -> Dict[str, Any]:
        """获取最繁忙的一天"""
        max_hours = 0
        busiest_day = None
        
        work_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        for day in work_days:
            day_hours = sum(m["duration"] for m in self.meetings[day])
            if day_hours > max_hours:
                max_hours = day_hours
                busiest_day = day
        
        return {
            "day": busiest_day,
            "total_hours": max_hours,
            "meetings": self.meetings[busiest_day] if busiest_day else []
        }
    
    def calculate_daily_work_time_distribution(self, day_name: str) -> Dict[str, float]:
        """计算某一天的工作时间分布"""
        if day_name not in self.meetings:
            return {}
        
        day_meetings = self.meetings[day_name]
        total_meeting_hours = sum(m["duration"] for m in day_meetings)
        
        # 假设工作日8小时
        total_work_hours = 8.0
        available_work_hours = total_work_hours - total_meeting_hours
        
        return {
            "meeting_hours": round(total_meeting_hours, 2),
            "work_hours": round(available_work_hours, 2),
            "meeting_percentage": round((total_meeting_hours / total_work_hours) * 100, 1),
            "work_percentage": round((available_work_hours / total_work_hours) * 100, 1)
        }
    
    def print_daily_schedule(self, day_name: str):
        """打印某一天的详细安排"""
        if day_name not in self.meetings:
            print(f"无{day_name}的会议安排")
            return
        
        day_meetings = self.meetings[day_name]
        time_dist = self.calculate_daily_work_time_distribution(day_name)
        
        print(f"\n{day_name} 详细安排")
        print("="*80)
        print(f"会议时间: {time_dist['meeting_hours']}小时 ({time_dist['meeting_percentage']}%)")
        print(f"工作时间: {time_dist['work_hours']}小时 ({time_dist['work_percentage']}%)")
        print("-"*80)
        
        # 创建时间块安排
        time_blocks = []
        
        # 上午工作时段
        time_blocks.append({"time": "08:30-09:10", "type": "深度工作", "task": "处理邮件和紧急事务"})
        
        # 添加会议
        for meeting in day_meetings:
            time_blocks.append({
                "time": meeting["time"],
                "type": "会议",
                "task": meeting["name"],
                "priority": meeting["priority"]
            })
        
        # 添加会议间的工作时段
        if day_name == "Monday":
            time_blocks.append({"time": "12:00-13:30", "type": "午餐休息", "task": "午餐和短暂休息"})
            time_blocks.append({"time": "13:30-15:00", "type": "技术工作", "task": "处理机器人讨论会决议"})
            time_blocks.append({"time": "15:00-17:30", "type": "项目管理", "task": "跟进项目进度和资源协调"})
        elif day_name == "Friday":
            time_blocks.append({"time": "09:50-11:00", "type": "会议准备", "task": "准备商清项目Sprint会材料"})
            time_blocks.append({"time": "12:00-13:30", "type": "午餐休息", "task": "午餐和短暂休息"})
            time_blocks.append({"time": "13:30-16:30", "type": "技术工作", "task": "处理技术问题和项目跟进"})
            time_blocks.append({"time": "16:30-17:30", "type": "会议", "task": "晨曦项目Sprint会"})
            time_blocks.append({"time": "17:30-18:00", "type": "会议", "task": "技术团队回顾会"})
        else:
            time_blocks.append({"time": "09:50-12:00", "type": "技术工作", "task": "处理技术问题和项目跟进"})
            time_blocks.append({"time": "13:30-17:30", "type": "项目管理", "task": "项目进度跟进和资源协调"})
        
        # 下班前时段
        time_blocks.append({"time": "17:30-18:00", "type": "总结规划", "task": "今日总结和明日规划"})
        
        # 打印时间安排
        for block in time_blocks:
            time_display = f"{block['time']}"
            task_display = f"[{block['type']}] {block['task']}"
            if 'priority' in block:
                task_display += f" (优先级: {block['priority']})"
            
            print(f"{time_display:20} {task_display}")

def main():
    """主函数"""
    manager = WeeklyMeetingManager()
    
    print("机器人研发团队负责人 - 每周固定会议管理系统")
    print("="*70)
    
    # 获取今天和明天的会议
    today = datetime.datetime.now()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today_name = day_names[today.weekday()]
    
    today_meetings = manager.get_today_meetings()
    tomorrow_meetings = manager.get_tomorrow_meetings()
    
    print(f"\n[今日会议] {today.strftime('%Y-%m-%d')} ({today_name})")
    print("-"*70)
    
    if today_meetings:
        for meeting in today_meetings:
            print(f"- {meeting['time']} {meeting['name']} ({meeting['duration']}小时)")
    else:
        print("今日无固定会议安排")
    
    print(f"\n[明日会议] {(today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')}")
    print("-"*70)
    
    if tomorrow_meetings:
        for meeting in tomorrow_meetings:
            print(f"- {meeting['time']} {meeting['name']} ({meeting['duration']}小时)")
    else:
        print("明日无固定会议安排")
    
    # 每周摘要
    weekly_summary = manager.get_weekly_summary()
    
    print(f"\n[每周会议摘要] (周一至周五)")
    print("-"*70)
    print(f"总会议数: {weekly_summary['total_meetings']}个")
    print(f"总会议时间: {weekly_summary['total_hours']:.1f}小时")
    print(f"平均每天会议: {weekly_summary['total_hours']/5:.1f}小时")
    
    print(f"\n[按类别分布]")
    for category, data in weekly_summary['by_category'].items():
        print(f"  {category}: {data['count']}个会议, {data['hours']:.1f}小时")
    
    print(f"\n[按天分布]")
    for day, data in weekly_summary['by_day'].items():
        time_dist = manager.calculate_daily_work_time_distribution(day)
        print(f"  {day}: {data['meeting_count']}个会议, {data['total_hours']:.1f}小时")
        print(f"     会议占比: {time_dist['meeting_percentage']}%, 工作占比: {time_dist['work_percentage']}%")
    
    # 最繁忙的一天
    busiest = manager.get_busiest_day()
    print(f"\n[最繁忙的一天] {busiest['day']}")
    print(f"  会议时间: {busiest['total_hours']:.1f}小时")
    
    # 打印今天详细安排
    if today_meetings:
        manager.print_daily_schedule(today_name)
    
    print(f"\n[系统使用建议]")
    print("-"*70)
    print("1. 每天早上查看今日会议安排，提前准备")
    print("2. 保护上午深度工作时间（08:30-09:10）")
    print("3. 周五是最繁忙的一天，需提前规划")
    print("4. 利用会议间隙高效处理工作")
    print("5. 下班前完成总结，为次日做好准备")
    
    print(f"\n" + "="*70)
    print("每周会议管理系统已就绪。系统会智能规划您的时间安排。")

if __name__ == "__main__":
    main()