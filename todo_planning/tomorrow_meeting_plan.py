"""
机器人研发团队负责人 - 明日会议安排规划系统
"""

import datetime
from typing import List, Dict, Any

class MeetingPlanner:
    """会议规划器"""
    
    def __init__(self):
        self.tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.meetings = []
    
    def add_meeting(self, name: str, time: str, duration: float, participants: List[str],
                   type: str, purpose: str, preparation_needed: bool, key_topics: List[str]):
        """添加会议"""
        meeting = {
            "name": name,
            "time": time,
            "duration": duration,  # 小时
            "participants": participants,
            "type": type,  # 评审会、计划会、技术分享、回顾会等
            "purpose": purpose,
            "preparation_needed": preparation_needed,
            "key_topics": key_topics,
            "priority": self._calculate_priority(type, purpose),
            "status": "scheduled"
        }
        self.meetings.append(meeting)
        return meeting
    
    def _calculate_priority(self, meeting_type: str, purpose: str) -> str:
        """计算会议优先级"""
        if "评审会" in meeting_type or "计划会" in meeting_type:
            return "高"  # 项目进度相关
        elif "技术分享" in purpose or "回顾会" in meeting_type:
            return "中"  # 技术成长相关
        else:
            return "低"
    
    def schedule_tomorrow_meetings(self):
        """安排明天的会议"""
        # 上午会议：商清项目Sprint评审和计划会
        self.add_meeting(
            name="商清项目Sprint评审与计划会",
            time="09:30-10:30",
            duration=1.0,
            participants=["项目负责人", "技术骨干", "产品经理", "测试负责人"],
            type="项目评审会 + 计划会",
            purpose="评审上周完成情况，规划下周工作任务，调整项目优先级",
            preparation_needed=True,
            key_topics=["上周完成情况回顾", "技术问题讨论", "下周任务规划", "风险评估"]
        )
        
        # 下午会议：晨曦项目Sprint评审和计划会
        self.add_meeting(
            name="晨曦项目Sprint评审与计划会",
            time="14:00-15:00",
            duration=1.0,
            participants=["项目负责人", "硬件工程师", "软件工程师", "算法工程师"],
            type="项目评审会 + 计划会",
            purpose="评审机器人底盘控制算法进展，规划下一步技术攻关方向",
            preparation_needed=True,
            key_topics=["底盘控制算法评审", "硬件集成问题", "下一步技术路线", "测试计划"]
        )
        
        # 下班前会议：技术团队回顾会
        self.add_meeting(
            name="技术团队回顾与技术分享会",
            time="17:00-17:30",
            duration=0.5,
            participants=["全体技术人员", "实习生"],
            type="技术回顾会 + 分享会",
            purpose="分析本周技术工作成果，分享技术经验，促进团队技术成长",
            preparation_needed=True,
            key_topics=["本周技术成果总结", "遇到的问题与解决方案", "技术经验分享", "下周技术学习计划"]
        )
    
    def calculate_meeting_time_distribution(self) -> Dict[str, float]:
        """计算会议时间分布"""
        total_meeting_time = sum(m["duration"] for m in self.meetings)
        total_work_time = 8.0  # 假设工作日8小时
        
        return {
            "会议时间": total_meeting_time,
            "可用工作时间": total_work_time - total_meeting_time,
            "会议占比": round((total_meeting_time / total_work_time) * 100, 1),
            "工作占比": round(((total_work_time - total_meeting_time) / total_work_time) * 100, 1)
        }
    
    def get_preparation_requirements(self) -> List[Dict[str, Any]]:
        """获取会议准备要求"""
        preparations = []
        for meeting in self.meetings:
            if meeting["preparation_needed"]:
                prep = {
                    "meeting": meeting["name"],
                    "time": meeting["time"],
                    "prep_items": [],
                    "estimated_prep_time": 0.5 if "技术" in meeting["type"] else 0.3  # 技术会议需要更多准备
                }
                
                # 根据会议类型添加准备项
                if "商清项目" in meeting["name"]:
                    prep["prep_items"] = [
                        "查看上周完成的任务清单",
                        "准备技术问题讨论点",
                        "准备下周任务优先级列表",
                        "风险评估报告"
                    ]
                elif "晨曦项目" in meeting["name"]:
                    prep["prep_items"] = [
                        "底盘控制算法进展报告",
                        "硬件集成问题清单",
                        "技术路线图更新",
                        "测试结果分析"
                    ]
                elif "技术团队" in meeting["name"]:
                    prep["prep_items"] = [
                        "本周技术成果总结",
                        "问题与解决方案整理",
                        "技术分享内容准备",
                        "学习计划建议"
                    ]
                
                preparations.append(prep)
        
        return preparations
    
    def generate_daily_schedule(self) -> Dict[str, List[Dict[str, Any]]]:
        """生成完整的日程安排"""
        # 按时间排序会议
        sorted_meetings = sorted(self.meetings, key=lambda x: x["time"])
        
        # 定义工作时间段
        work_periods = []
        
        # 上午工作时间段（会议前）
        work_periods.append({
            "time": "08:30-09:30",
            "type": "深度工作",
            "task": "处理邮件和紧急事务，为商清项目会议做准备",
            "duration": 1.0
        })
        
        # 会议时间段
        for meeting in sorted_meetings:
            work_periods.append({
                "time": meeting["time"],
                "type": "会议",
                "task": meeting["name"],
                "duration": meeting["duration"],
                "priority": meeting["priority"]
            })
        
        # 会议间的工作时间段
        work_periods.append({
            "time": "10:30-12:00",
            "type": "技术工作",
            "task": "根据商清会议结果调整工作计划，处理技术问题",
            "duration": 1.5
        })
        
        work_periods.append({
            "time": "13:30-14:00",
            "type": "准备会议",
            "task": "为晨曦项目会议做准备，整理技术资料",
            "duration": 0.5
        })
        
        work_periods.append({
            "time": "15:00-17:00",
            "type": "项目管理",
            "task": "处理会议决议，跟进项目进度，协调资源",
            "duration": 2.0
        })
        
        work_periods.append({
            "time": "17:30-18:00",
            "type": "总结规划",
            "task": "总结今日会议成果，规划明日工作，处理遗留事项",
            "duration": 0.5
        })
        
        return {
            "date": self.tomorrow,
            "schedule": work_periods,
            "total_work_hours": sum(p["duration"] for p in work_periods)
        }
    
    def print_meeting_summary(self):
        """打印会议摘要"""
        print(f"\n[明日会议安排] {self.tomorrow}")
        print("="*70)
        
        for i, meeting in enumerate(self.meetings, 1):
            print(f"\n{i}. {meeting['name']}")
            print(f"   时间: {meeting['time']} ({meeting['duration']}小时)")
            print(f"   类型: {meeting['type']}")
            print(f"   优先级: {meeting['priority']}")
            print(f"   参与者: {', '.join(meeting['participants'])}")
            print(f"   关键议题: {', '.join(meeting['key_topics'])}")
    
    def print_daily_schedule(self):
        """打印完整日程"""
        schedule = self.generate_daily_schedule()
        
        print(f"\n[明日完整日程安排] {schedule['date']}")
        print("="*70)
        
        for period in schedule["schedule"]:
            time_display = f"{period['time']} ({period['duration']}小时)"
            task_display = f"[{period['type']}] {period['task']}"
            if 'priority' in period:
                task_display += f" (优先级: {period['priority']})"
            
            print(f"{time_display:25} {task_display}")
    
    def print_preparation_guide(self):
        """打印会议准备指南"""
        preparations = self.get_preparation_requirements()
        
        print(f"\n[会议准备要求]")
        print("="*70)
        
        for prep in preparations:
            print(f"\n会议: {prep['meeting']}")
            print(f"时间: {prep['time']}")
            print(f"预计准备时间: {prep['estimated_prep_time']}小时")
            print("准备事项:")
            for item in prep["prep_items"]:
                print(f"  - {item}")

def main():
    """主函数"""
    planner = MeetingPlanner()
    
    print("机器人研发团队负责人 - 明日会议规划系统")
    print("="*60)
    
    # 安排会议
    planner.schedule_tomorrow_meetings()
    
    # 打印会议摘要
    planner.print_meeting_summary()
    
    # 计算时间分布
    time_dist = planner.calculate_meeting_time_distribution()
    print(f"\n[时间分布分析]")
    print(f"总会议时间: {time_dist['会议时间']}小时")
    print(f"可用工作时间: {time_dist['可用工作时间']}小时")
    print(f"会议占比: {time_dist['会议占比']}%")
    print(f"工作占比: {time_dist['工作占比']}%")
    
    # 打印会议准备指南
    planner.print_preparation_guide()
    
    # 打印完整日程
    planner.print_daily_schedule()
    
    # 提供执行建议
    print(f"\n[执行建议]")
    print("="*70)
    print("1. 上午深度工作时段非常重要，请确保无打扰")
    print("2. 每个会议前预留15-30分钟准备时间")
    print("3. 会议间的工作时段要高效利用，处理会议决议")
    print("4. 技术团队回顾会前收集团队成员的技术收获")
    print("5. 下班前半小时用于总结和明日规划")
    
    print(f"\n[重点关注]")
    print("1. 商清项目：关注技术问题解决进度")
    print("2. 晨曦项目：底盘控制算法是关键")
    print("3. 技术团队：促进技术经验传承")
    
    print(f"\n[风险提醒]")
    print("1. 会议时间占比较高(31.3%)，需确保会议效率")
    print("2. 多个项目并行，注意资源协调")
    print("3. 技术分享需要提前收集内容")
    
    print(f"\n" + "="*60)
    print("明日会议规划完成。建议今晚完成必要准备，确保明日高效执行。")

if __name__ == "__main__":
    main()