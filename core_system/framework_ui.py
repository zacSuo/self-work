#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多技能框架用户界面
提供交互式命令行界面来使用各种技能
"""

import os
import sys
import json
from datetime import datetime
from skills_framework import SkillsFramework


class FrameworkUI:
    """框架用户界面"""
    
    def __init__(self):
        self.framework = SkillsFramework()
        self.running = True
        self.user_name = "用户"
        
    def display_welcome(self):
        """显示欢迎界面"""
        print("\n" + "="*60)
        print("🧠 多技能框架系统")
        print("="*60)
        print("欢迎使用智能技能框架!")
        print("本系统集成了多种技能包，帮助您高效处理各种任务")
        print("="*60)
        
    def display_main_menu(self):
        """显示主菜单"""
        print("\n📋 主菜单")
        print("-" * 40)
        print("1. 🎯 工作优先级排序")
        print("2. ⏰ 时间分析")
        print("3. 📊 查看可用技能")
        print("4. ⚙️ 系统设置")
        print("5. ℹ️ 系统信息")
        print("6. 🚪 退出系统")
        print("-" * 40)
        
    def get_user_choice(self) -> str:
        """获取用户选择"""
        while True:
            try:
                choice = input("\n请选择操作 (1-6): ").strip()
                if choice in ["1", "2", "3", "4", "5", "6"]:
                    return choice
                else:
                    print("❌ 请输入有效的选项 (1-6)")
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用，再见!")
                sys.exit(0)
    
    def run_priority_sorter(self):
        """运行优先级排序技能"""
        print("\n🎯 工作优先级排序")
        print("-" * 40)
        print("请输入您的任务列表（支持多种格式）:")
        print("1. 直接输入任务标题（每行一个）")
        print("2. 任务标题 [紧急度/重要性/工作量]")
        print("3. 输入'example'查看示例")
        print("4. 输入'back'返回主菜单")
        print("-" * 40)
        
        tasks_input = []
        print("\n📝 请输入任务（空行结束输入）:")
        
        while True:
            line = input("任务: ").strip()
            
            if not line:
                break
            elif line.lower() == "back":
                return
            elif line.lower() == "example":
                self.show_priority_example()
                continue
            
            tasks_input.append(line)
        
        if not tasks_input:
            print("⚠️ 未输入任何任务")
            return
        
        # 执行优先级排序
        result = self.framework.execute_skill("priority_sorter", tasks_input)
        
        self.display_priority_results(result)
    
    def show_priority_example(self):
        """显示优先级排序示例"""
        print("\n📋 输入示例:")
        print("完成项目报告 [9/8/6]")
        print("回复客户邮件")
        print("学习新技术 [3/8/5]")
        print("团队会议准备 [7/6/3]")
        print("\n💡 格式说明: 任务标题 [紧急度/重要性/工作量]")
        print("   紧急度/重要性/工作量: 1-10分，10为最高")
    
    def display_priority_results(self, result):
        """显示优先级排序结果"""
        if not result["success"]:
            print(f"❌ 排序失败: {result['error']}")
            return
        
        data = result["result"]
        
        print("\n" + "🎯" * 30)
        print("📊 优先级排序结果")
        print("🎯" * 30)
        
        # 显示排序后的任务
        for i, task in enumerate(data["prioritized_tasks"], 1):
            category = task["priority_category"]
            score = task["priority_score"]
            
            # 根据分类显示不同颜色
            if category == "紧急重要":
                color_prefix = "🔴"
            elif category == "重要不紧急":
                color_prefix = "🟡" 
            elif category == "紧急不重要":
                color_prefix = "🟢"
            else:
                color_prefix = "⚪"
            
            print(f"{i:2d}. {color_prefix} [{category}] {task['title']}")
            print(f"     分数: {score:.3f} | 紧急: {task['urgency']} | 重要: {task['importance']} | 工作量: {task['effort']}")
        
        # 显示摘要
        summary = data["summary"]
        print(f"\n📈 任务摘要:")
        print(f"   总任务数: {summary['total_tasks']}")
        print(f"   平均优先级分数: {summary['average_score']:.3f}")
        print(f"   整体紧急度: {summary['urgency_level']}")
        
        # 显示分类分布
        print(f"\n📊 任务分类分布:")
        for category, count in summary["category_distribution"].items():
            print(f"   {category}: {count}个任务")
        
        # 显示建议
        if data["recommendations"]:
            print(f"\n💡 优化建议:")
            for rec in data["recommendations"]:
                print(f"   • {rec}")
        
        # 显示每日计划
        daily_plan = data["daily_plan"]
        print(f"\n📅 今日工作计划 ({daily_plan['date']}):")
        print(f"   可完成任务: {daily_plan['total_tasks']}个")
        print(f"   预计用时: {daily_plan['completion_estimate']}")
    
    def run_time_analyzer(self):
        """运行时间分析技能"""
        print("\n⏰ 时间分析")
        print("-" * 40)
        print("正在分析您的工作时间模式...")
        
        # 使用示例数据进行演示
        example_data = [
            {
                "date": "2025-03-10",
                "start_time": "09:00",
                "end_time": "18:00", 
                "productive_hours": 7.0,
                "tasks_completed": 8,
                "focus_score": 0.82
            },
            {
                "date": "2025-03-11",
                "start_time": "08:30",
                "end_time": "17:30",
                "productive_hours": 6.5,
                "tasks_completed": 7,
                "focus_score": 0.78
            }
        ]
        
        result = self.framework.execute_skill("time_analyzer", example_data)
        self.display_time_analysis_results(result)
    
    def display_time_analysis_results(self, result):
        """显示时间分析结果"""
        if not result["success"]:
            print(f"❌ 分析失败: {result['error']}")
            return
        
        data = result["result"]
        
        print("\n" + "⏰" * 30)
        print("📊 时间分析报告")
        print("⏰" * 30)
        
        patterns = data["time_patterns"]
        stats = data["efficiency_stats"]
        
        print(f"\n📈 时间模式分析:")
        print(f"   日均高效工作时间: {patterns.get('daily_average_hours', 0)}小时")
        print(f"   最高效日期: {patterns.get('most_productive_day', 'N/A')}")
        print(f"   峰值生产力时段: {', '.join(patterns.get('peak_productivity_hours', []))}")
        
        print(f"\n📊 效率统计:")
        print(f"   分析天数: {stats.get('total_days', 0)}")
        print(f"   总高效时间: {stats.get('total_productive_hours', 0)}小时")
        print(f"   总完成任务: {stats.get('total_tasks_completed', 0)}个")
        print(f"   平均效率: {stats.get('average_efficiency', 0)} 任务/小时")
        print(f"   效率等级: {stats.get('efficiency_level', 'medium')}")
        
        # 显示评分
        score = data["overall_score"]
        print(f"\n⭐ 综合评分: {score}/100")
        
        # 进度条显示评分
        bar_length = 20
        filled = int(bar_length * score / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}] {score}%")
        
        # 显示建议
        if data["recommendations"]:
            print(f"\n💡 优化建议:")
            for rec in data["recommendations"]:
                print(f"   • {rec}")
    
    def list_available_skills(self):
        """列出可用技能"""
        print("\n🛠️ 可用技能列表")
        print("-" * 50)
        
        skills = self.framework.list_skills()
        
        if not skills:
            print("❌ 未找到可用技能")
            return
        
        for i, skill in enumerate(skills, 1):
            status = "✅ 启用" if skill["enabled"] else "❌ 禁用"
            print(f"{i}. {skill['name']} ({skill['version']}) - {status}")
            print(f"   描述: {skill['description']}")
            if skill['last_executed']:
                print(f"   最后执行: {skill['last_executed']}")
            print(f"   执行次数: {skill['execution_count']}")
            print()
    
    def show_system_settings(self):
        """显示系统设置"""
        print("\n⚙️ 系统设置")
        print("-" * 40)
        print("1. 查看系统信息")
        print("2. 管理技能状态")
        print("3. 备份系统数据")
        print("4. 恢复系统数据")
        print("5. 返回主菜单")
        
        choice = input("\n请选择设置选项: ").strip()
        
        if choice == "1":
            self.show_system_info()
        elif choice == "2":
            self.manage_skills()
        elif choice == "3":
            self.backup_data()
        elif choice == "4":
            self.restore_data()
    
    def show_system_info(self):
        """显示系统信息"""
        print("\nℹ️ 系统信息")
        print("-" * 40)
        print(f"系统版本: 多技能框架 v1.0")
        print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"技能目录: {self.framework.skills_dir}")
        print(f"已加载技能: {len(self.framework.skills)}个")
        print(f"执行历史记录: {len(self.framework.context.get('execution_history', []))}条")
    
    def manage_skills(self):
        """管理技能状态"""
        print("\n🔧 技能管理")
        skills = self.framework.list_skills()
        
        for i, skill in enumerate(skills, 1):
            status = "启用" if skill["enabled"] else "禁用"
            print(f"{i}. {skill['name']} - {status}")
        
        try:
            choice = int(input("\n选择要管理的技能编号: ")) - 1
            if 0 <= choice < len(skills):
                skill_name = skills[choice]["name"]
                current_status = "启用" if skills[choice]["enabled"] else "禁用"
                
                action = input(f"当前状态: {current_status}，要启用还是禁用? (e/d): ").strip().lower()
                
                if action == "e":
                    self.framework.enable_skill(skill_name)
                    print(f"✅ 已启用技能: {skill_name}")
                elif action == "d":
                    self.framework.disable_skill(skill_name)
                    print(f"✅ 已禁用技能: {skill_name}")
                else:
                    print("❌ 无效操作")
            else:
                print("❌ 无效的选择")
        except ValueError:
            print("❌ 请输入有效数字")
    
    def backup_data(self):
        """备份系统数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"framework_backup_{timestamp}.json"
        
        self.framework.save_context(backup_file)
        print(f"✅ 系统数据已备份到: {backup_file}")
    
    def restore_data(self):
        """恢复系统数据"""
        print("\n⚠️ 恢复系统数据将覆盖当前数据，请谨慎操作!")
        confirm = input("确认恢复? (y/N): ").strip().lower()
        
        if confirm == "y":
            backup_files = [f for f in os.listdir('.') if f.startswith('framework_backup_') and f.endswith('.json')]
            
            if not backup_files:
                print("❌ 未找到备份文件")
                return
            
            print("\n可用的备份文件:")
            for i, file in enumerate(backup_files, 1):
                print(f"{i}. {file}")
            
            try:
                choice = int(input("\n选择要恢复的备份文件: ")) - 1
                if 0 <= choice < len(backup_files):
                    self.framework.load_context(backup_files[choice])
                    print(f"✅ 已从 {backup_files[choice]} 恢复系统数据")
                else:
                    print("❌ 无效的选择")
            except ValueError:
                print("❌ 请输入有效数字")
    
    def show_system_info_menu(self):
        """显示系统信息菜单"""
        self.show_system_info()
        
        # 显示执行历史摘要
        history = self.framework.context.get("execution_history", [])
        if history:
            print(f"\n📋 最近执行记录:")
            recent = history[-5:]  # 显示最近5条
            for record in recent:
                skill_name = record.get("skill_name", "未知")
                timestamp = record.get("timestamp", "")
                print(f"   {skill_name} - {timestamp[:16]}")
    
    def run(self):
        """运行主循环"""
        self.display_welcome()
        
        while self.running:
            self.display_main_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.run_priority_sorter()
            elif choice == "2":
                self.run_time_analyzer()
            elif choice == "3":
                self.list_available_skills()
            elif choice == "4":
                self.show_system_settings()
            elif choice == "5":
                self.show_system_info_menu()
            elif choice == "6":
                self.exit_system()
    
    def exit_system(self):
        """退出系统"""
        print("\n💾 正在保存系统数据...")
        self.framework.save_context()
        print("👋 感谢使用多技能框架系统，再见!")
        self.running = False


def main():
    """主函数"""
    try:
        ui = FrameworkUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用，再见!")
    except Exception as e:
        print(f"\n❌ 系统错误: {e}")
        print("请检查系统配置后重试")


if __name__ == "__main__":
    main()