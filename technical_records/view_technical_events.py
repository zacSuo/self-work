"""
查看技术事件记录
"""

import json
import datetime
import os

def load_events():
    """加载事件数据"""
    data_file = "private_data/data/private_data/data/technical_events.json"
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def display_event_summary(event):
    """显示事件摘要"""
    print(f"\n[{event['date']}] {event['title']}")
    print(f"  类型: {event['type']} | 重要性: {event['importance']}")
    print(f"  ID: {event['id']}")
    print(f"  标签: {', '.join(event['tags'])}")
    
    # 显示问题摘要
    problem_lines = event['problem'].split('\n')
    if problem_lines:
        first_line = problem_lines[0]
        if len(first_line) > 80:
            print(f"  问题: {first_line[:80]}...")
        else:
            print(f"  问题: {first_line}")
    
    print("-" * 60)

def display_event_details(event):
    """显示事件详细信息"""
    print("\n" + "="*80)
    print(f"技术事件详情: {event['title']}")
    print("="*80)
    print(f"事件ID: {event['id']}")
    print(f"记录时间: {event['timestamp']}")
    print(f"事件类型: {event['type']}")
    print(f"重要性级别: {event['importance']}")
    print(f"参与者: {', '.join(event['participants'])}")
    print(f"标签: {', '.join(event['tags'])}")
    
    print("\n[问题描述]:")
    for line in event['problem'].split('\n'):
        print(f"  {line}")
    
    print("\n[解决方案]:")
    for line in event['solution'].split('\n'):
        print(f"  {line}")
    
    print("\n[影响和意义]:")
    for line in event['impact'].split('\n'):
        print(f"  {line}")
    
    if event['attachments']:
        print(f"\n[相关附件]: {', '.join(event['attachments'])}")
    
    print("\n" + "="*80)

def main():
    """主函数"""
    print("机器人研发技术事件查看器")
    print("="*50)
    
    events = load_events()
    
    if not events:
        print("暂无技术事件记录")
        return
    
    print(f"\n共记录 {len(events)} 个技术事件")
    
    # 按日期排序，最新的在前
    sorted_events = sorted(events, key=lambda x: x['timestamp'], reverse=True)
    
    # 显示最近的事件
    recent_days = 7
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=recent_days)).strftime("%Y-%m-%d")
    recent_events = [e for e in sorted_events if e['date'] >= cutoff_date]
    
    print(f"\n最近{recent_days}天内的事件 ({len(recent_events)} 个):")
    print("-" * 60)
    
    for event in recent_events:
        display_event_summary(event)
    
    # 显示今日事件
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_events = [e for e in sorted_events if e['date'] == today]
    
    if today_events:
        print(f"\n今日事件 ({len(today_events)} 个):")
        print("="*60)
        
        for i, event in enumerate(today_events, 1):
            print(f"\n{i}. {event['title']}")
            display_event_details(event)
    
    # 统计信息
    print(f"\n统计信息:")
    print(f"- 总事件数: {len(events)}")
    print(f"- 本周事件: {len(recent_events)}")
    print(f"- 今日事件: {len(today_events)}")
    
    # 类型分布
    type_counts = {}
    for event in events:
        event_type = event['type']
        type_counts[event_type] = type_counts.get(event_type, 0) + 1
    
    print(f"\n事件类型分布:")
    for event_type, count in type_counts.items():
        print(f"  - {event_type}: {count}个")

if __name__ == "__main__":
    main()