#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间分析技能包
分析工作时间模式和效率
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from ..skills_framework import Skill


class TimeAnalyzer(Skill):
    """时间分析技能"""
    
    def __init__(self):
        super().__init__(
            name="time_analyzer",
            description="分析工作时间模式、效率统计和优化建议",
            version="1.0.0"
        )
        
        self.analysis_history = []
        self.efficiency_thresholds = {
            "high": 0.8,    # 80%以上为高效
            "medium": 0.6,  # 60%-80%为中等
            "low": 0.4      # 40%以下为低效
        }
    
    def execute(self, input_data: Any, context: Dict = None) -> Dict:
        """执行时间分析"""
        try:
            # 解析输入数据
            work_data = self._parse_work_data(input_data)
            
            # 分析工作时间模式
            time_patterns = self._analyze_time_patterns(work_data)
            
            # 计算效率统计
            efficiency_stats = self._calculate_efficiency(work_data)
            
            # 生成优化建议
            recommendations = self._generate_recommendations(time_patterns, efficiency_stats)
            
            # 保存分析记录
            self._save_analysis(time_patterns, efficiency_stats)
            
            return {
                "success": True,
                "time_patterns": time_patterns,
                "efficiency_stats": efficiency_stats,
                "recommendations": recommendations,
                "overall_score": self._calculate_overall_score(efficiency_stats)
            }
            
        except Exception as e:
            return {"error": f"执行时间分析时出错: {str(e)}", "success": False}
    
    def _parse_work_data(self, input_data: Any) -> List[Dict]:
        """解析工作数据"""
        if isinstance(input_data, list):
            return input_data
        elif isinstance(input_data, dict) and "work_sessions" in input_data:
            return input_data["work_sessions"]
        elif isinstance(input_data, str):
            # 尝试解析JSON字符串
            try:
                data = json.loads(input_data)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "work_sessions" in data:
                    return data["work_sessions"]
            except:
                pass
        
        # 返回示例数据用于演示
        return self._generate_sample_data()
    
    def _generate_sample_data(self) -> List[Dict]:
        """生成示例工作数据"""
        base_date = datetime.now().date()
        
        return [
            {
                "date": (base_date - timedelta(days=i)).isoformat(),
                "start_time": "09:00",
                "end_time": "18:00",
                "productive_hours": 6.5,
                "tasks_completed": 8,
                "breaks_taken": 3,
                "focus_score": 0.75
            }
            for i in range(7)  # 最近7天数据
        ]
    
    def _analyze_time_patterns(self, work_data: List[Dict]) -> Dict:
        """分析工作时间模式"""
        if not work_data:
            return {}
        
        patterns = {
            "daily_average_hours": 0,
            "most_productive_day": None,
            "peak_productivity_hours": [],
            "consistent_days": 0,
            "weekly_trend": "stable"
        }
        
        # 计算每日平均工作时间
        total_hours = sum(session.get("productive_hours", 0) for session in work_data)
        patterns["daily_average_hours"] = round(total_hours / len(work_data), 1)
        
        # 找出最高效的一天
        if work_data:
            most_productive = max(work_data, key=lambda x: x.get("tasks_completed", 0))
            patterns["most_productive_day"] = most_productive.get("date")
        
        # 分析峰值生产力时段（简化版）
        patterns["peak_productivity_hours"] = ["09:00-11:00", "14:00-16:00"]
        
        return patterns
    
    def _calculate_efficiency(self, work_data: List[Dict]) -> Dict:
        """计算效率统计"""
        if not work_data:
            return {}
        
        stats = {
            "total_days": len(work_data),
            "total_productive_hours": 0,
            "total_tasks_completed": 0,
            "average_efficiency": 0,
            "efficiency_level": "medium"
        }
        
        total_hours = sum(session.get("productive_hours", 0) for session in work_data)
        total_tasks = sum(session.get("tasks_completed", 0) for session in work_data)
        
        stats["total_productive_hours"] = round(total_hours, 1)
        stats["total_tasks_completed"] = total_tasks
        
        # 计算平均效率（任务数/工作时间）
        if total_hours > 0:
            stats["average_efficiency"] = round(total_tasks / total_hours, 2)
        
        # 确定效率等级
        efficiency_ratio = stats["average_efficiency"] / 2.0  # 假设2任务/小时为基准
        if efficiency_ratio >= self.efficiency_thresholds["high"]:
            stats["efficiency_level"] = "high"
        elif efficiency_ratio >= self.efficiency_thresholds["medium"]:
            stats["efficiency_level"] = "medium"
        else:
            stats["efficiency_level"] = "low"
        
        return stats
    
    def _generate_recommendations(self, patterns: Dict, stats: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 基于时间模式的建议
        avg_hours = patterns.get("daily_average_hours", 0)
        if avg_hours > 10:
            recommendations.append("⚠️ 工作时间过长，建议适当休息避免疲劳")
        elif avg_hours < 6:
            recommendations.append("💡 可以考虑增加专注工作时间提高产出")
        
        # 基于效率统计的建议
        efficiency_level = stats.get("efficiency_level", "medium")
        if efficiency_level == "low":
            recommendations.append("🚀 效率有待提升，尝试使用番茄工作法")
        elif efficiency_level == "high":
            recommendations.append("✅ 保持高效工作状态，注意工作生活平衡")
        
        # 通用建议
        recommendations.extend([
            "⏰ 在峰值生产力时段处理重要任务",
            "🔄 定期回顾和调整工作时间安排",
            "📊 使用时间追踪工具优化工作流程"
        ])
        
        return recommendations
    
    def _calculate_overall_score(self, stats: Dict) -> int:
        """计算整体评分（0-100）"""
        efficiency_level = stats.get("efficiency_level", "medium")
        
        if efficiency_level == "high":
            return 85
        elif efficiency_level == "medium":
            return 70
        else:
            return 55
    
    def _save_analysis(self, patterns: Dict, stats: Dict):
        """保存分析记录"""
        analysis_record = {
            "timestamp": datetime.now().isoformat(),
            "patterns": patterns,
            "stats": stats,
            "overall_score": self._calculate_overall_score(stats)
        }
        
        self.analysis_history.append(analysis_record)
        
        # 只保留最近50次记录
        if len(self.analysis_history) > 50:
            self.analysis_history = self.analysis_history[-50:]
    
    def validate_input(self, input_data: Any) -> bool:
        """验证输入数据"""
        return input_data is not None


def main():
    """技能测试"""
    analyzer = TimeAnalyzer()
    
    # 测试数据
    test_data = [
        {
            "date": "2025-03-08",
            "start_time": "09:00",
            "end_time": "17:30",
            "productive_hours": 6.0,
            "tasks_completed": 7,
            "focus_score": 0.8
        },
        {
            "date": "2025-03-09", 
            "start_time": "08:30",
            "end_time": "18:00",
            "productive_hours": 7.5,
            "tasks_completed": 9,
            "focus_score": 0.85
        }
    ]
    
    print("⏰ 时间分析技能测试")
    print("=" * 50)
    
    result = analyzer.execute(test_data)
    
    if result["success"]:
        print("✅ 分析成功!")
        
        patterns = result["time_patterns"]
        stats = result["efficiency_stats"]
        
        print(f"\n📊 时间模式分析:")
        print(f"  日均高效工作时间: {patterns.get('daily_average_hours', 0)}小时")
        print(f"  最高效日期: {patterns.get('most_productive_day', 'N/A')}")
        
        print(f"\n📈 效率统计:")
        print(f"  总任务完成数: {stats.get('total_tasks_completed', 0)}")
        print(f"  平均效率: {stats.get('average_efficiency', 0)} 任务/小时")
        print(f"  效率等级: {stats.get('efficiency_level', 'medium')}")
        
        print(f"\n💡 优化建议:")
        for rec in result["recommendations"]:
            print(f"  - {rec}")
    else:
        print(f"❌ 分析失败: {result['error']}")


if __name__ == "__main__":
    main()