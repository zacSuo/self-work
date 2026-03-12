"""
机器人研发技术事件记录系统
记录技术里程碑、问题解决、创新方案等重要事件
"""

import json
import datetime
import os
from typing import Dict, List, Any

class TechnicalEventRecorder:
    """技术事件记录器"""
    
    def __init__(self, data_file="technical_events.json"):
        self.data_file = data_file
        self.events = self.load_events()
    
    def load_events(self) -> List[Dict[str, Any]]:
        """加载历史事件"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_events(self):
        """保存事件到文件"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)
    
    def record_event(self, 
                    event_type: str,
                    title: str,
                    description: str,
                    problem: str,
                    solution: str,
                    impact: str,
                    participants: List[str] = None,
                    tags: List[str] = None,
                    attachments: List[str] = None):
        """记录一个技术事件"""
        
        event_id = f"EVENT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        event = {
            "id": event_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.datetime.now().isoformat(),
            "type": event_type,  # 里程碑、问题解决、创新、优化等
            "title": title,
            "description": description,
            "problem": problem,  # 遇到的问题
            "solution": solution,  # 解决方案
            "impact": impact,  # 影响和意义
            "participants": participants or ["团队负责人"],
            "tags": tags or [],
            "attachments": attachments or [],
            "status": "completed",
            "importance": "medium"  # low, medium, high, critical
        }
        
        self.events.append(event)
        self.save_events()
        return event
    
    def get_today_events(self) -> List[Dict[str, Any]]:
        """获取今天的事件"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return [event for event in self.events if event["date"] == today]
    
    def get_recent_events(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取最近N天的事件"""
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        return [event for event in self.events if event["date"] >= cutoff_date]
    
    def search_events(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索事件"""
        keyword_lower = keyword.lower()
        results = []
        for event in self.events:
            if (keyword_lower in event["title"].lower() or 
                keyword_lower in event["description"].lower() or
                keyword_lower in event["problem"].lower() or
                keyword_lower in event["solution"].lower() or
                any(keyword_lower in tag.lower() for tag in event["tags"])):
                results.append(event)
        return results
    
    def print_event(self, event: Dict[str, Any]):
        """格式化打印事件"""
        print("\n" + "="*80)
        print(f"技术事件记录: {event['title']}")
        print("="*80)
        print(f"事件ID: {event['id']}")
        print(f"日期: {event['date']}")
        print(f"类型: {event['type']}")
        print(f"重要性: {event['importance']}")
        print(f"参与者: {', '.join(event['participants'])}")
        print(f"标签: {', '.join(event['tags'])}")
        
        print("\n[问题描述]:")
        print(event['problem'])
        
        print("\n[解决方案]:")
        print(event['solution'])
        
        print("\n[影响和意义]:")
        print(event['impact'])
        
        print("\n" + "-"*40)

def record_robot_chassis_dust_problem():
    """记录J30S机器人底盘积尘问题解决事件"""
    
    recorder = TechnicalEventRecorder()
    
    event = recorder.record_event(
        event_type="技术里程碑",
        title="J30S机器人底盘积尘问题解决方案",
        description="识别并解决机器人底盘履带卷入灰尘的问题，提出使用刷子和硅胶进行前后覆盖履带的优化方案",
        
        problem="J30S机器人长时间运行后，底盘底部会积尘严重。之前遗漏的履带卷入灰尘问题是主要原因。履带在运行时会将地面灰尘卷入底盘内部，导致：\n"
                "1. 灰尘在底盘内部积累，影响机械结构\n"
                "2. 可能影响传感器正常工作\n"
                "3. 增加维护频率和成本\n"
                "4. 在特定环境（如实验室、洁净环境）下产生问题",
        
        solution="提出使用刷子和硅胶材料进行前后覆盖履带的创新方案：\n"
                "1. 在履带前方安装柔性刷子组件，主动清扫履带前方的灰尘\n"
                "2. 在履带后方使用硅胶材料覆盖，防止灰尘进入底盘内部\n"
                "3. 优化底盘封闭结构，提高整体密封性\n"
                "4. 建立标准化维护检查流程\n"
                "\n技术要点：\n"
                "- 刷子材料选择：耐磨、柔性的尼龙刷毛\n"
                "- 硅胶密封：食品级硅胶，耐磨损、易清洁\n"
                "- 安装方式：模块化设计，便于维护更换\n"
                "- 测试验证：在实际环境中进行长期运行测试",
        
        impact="此次解决方案是一个重要的技术里程碑：\n"
              "1. 从根本上解决了底盘积尘问题，提升机器人长期可靠性\n"
              "2. 明确了底盘封闭的关键技术路线\n"
              "3. 为后续机器人设计提供了重要的设计参考\n"
              "4. 提高了机器人在复杂环境下的适应性\n"
              "5. 降低了维护成本和频率",
        
        participants=["团队负责人"],
        tags=["机器人", "底盘设计", "防尘方案", "履带优化", "J30S", "技术里程碑"],
        attachments=["底盘设计图纸", "测试报告", "材料清单"]
    )
    
    return event, recorder

def view_today_events():
    """查看今日事件"""
    recorder = TechnicalEventRecorder()
    today_events = recorder.get_today_events()
    
    print(f"\n今日技术事件 ({len(today_events)} 个)")
    print("="*60)
    
    for event in today_events:
        print(f"\n[{event['date']}] {event['title']}")
        print(f"  类型: {event['type']} | 重要性: {event['importance']}")
        print(f"  简要: {event['description'][:100]}...")
    
    return today_events

def record_today_chassis_event():
    """记录今天的底盘积尘解决方案事件"""
    print("机器人研发技术事件记录系统")
    print("="*50)
    
    # 检查是否已经记录过
    recorder = TechnicalEventRecorder()
    today_events = recorder.get_today_events()
    
    # 查找是否有类似的底盘事件
    chassis_events = [e for e in today_events if "底盘积尘" in e["title"] or "底盘" in e["title"]]
    
    if chassis_events:
        print(f"\n[注意] 今天已经记录了 {len(chassis_events)} 个相关事件")
        print("是否要添加新记录？(这将创建新的事件记录)")
        # 这里简化处理，直接记录新事件
        print("[继续] 创建新的技术里程碑记录...")
    
    # 记录今天的底盘积尘解决方案
    print("\n[记录] 开始记录今日技术里程碑事件...")
    event, recorder = record_robot_chassis_dust_problem()
    
    print(f"\n[完成] 成功记录技术事件: {event['title']}")
    print(f"  事件ID: {event['id']}")
    print(f"  已保存到: {recorder.data_file}")
    
    # 显示今日事件
    today_events = recorder.get_today_events()
    
    if today_events:
        print(f"\n今日总共记录 {len(today_events)} 个事件")
        print("="*60)
        
        for i, ev in enumerate(today_events, 1):
            print(f"\n{i}. {ev['title']}")
            print(f"   类型: {ev['type']} | 时间: {ev['timestamp'][11:19]}")
    
    print("\n" + "="*50)
    print("技术事件记录完成。这个里程碑已永久保存，可供未来参考。")
    print("使用 view_technical_events.py 查看完整记录。")

def main():
    """主函数 - 直接记录今日事件"""
    record_today_chassis_event()

if __name__ == "__main__":
    main()