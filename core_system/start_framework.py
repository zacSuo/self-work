#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多技能框架启动脚本
提供多种启动方式和配置选项
"""

import os
import sys
import argparse
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills_framework import SkillsFramework
from framework_ui import FrameworkUI


def check_dependencies():
    """检查依赖是否满足"""
    try:
        import flask
        return True
    except ImportError:
        print("⚠️ 警告: Flask未安装，Web界面功能将受限")
        print("   可以运行: pip install flask")
        return False


def load_config():
    """加载配置文件"""
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
    
    # 返回默认配置
    return {
        "framework": {
            "name": "多技能框架系统",
            "version": "1.0.0"
        }
    }


def start_cli_interface():
    """启动命令行界面"""
    print("🚀 启动多技能框架命令行界面...")
    
    # 检查依赖
    check_dependencies()
    
    # 加载配置
    config = load_config()
    
    # 启动UI
    try:
        ui = FrameworkUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n👋 感谢使用多技能框架系统!")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查系统配置后重试")


def start_web_interface():
    """启动Web界面"""
    print("🌐 启动多技能框架Web界面...")
    
    # 检查Flask依赖
    try:
        import flask
    except ImportError:
        print("❌ Flask未安装，无法启动Web界面")
        print("请运行: pip install flask")
        return
    
    # 启动Web服务
    try:
        from web_interface import app
        print("✅ Web服务启动成功!")
        print("📱 请在浏览器中访问: http://localhost:5000")
        print("⏹️  按 Ctrl+C 停止服务")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ 启动Web界面失败: {e}")
        print("💡 可以尝试使用命令行界面: python start_framework.py --cli")


def test_framework():
    """测试框架功能"""
    print("🧪 测试多技能框架功能...")
    
    try:
        framework = SkillsFramework()
        
        # 手动添加技能（如果未自动加载）
        from skills_framework import PrioritySkill
        framework.skills["priority_sorter"] = PrioritySkill()
        
        # 列出技能
        skills = framework.list_skills()
        print(f"✅ 已加载 {len(skills)} 个技能:")
        for skill in skills:
            print(f"   - {skill['name']}: {skill['description']}")
        
        # 测试优先级排序
        test_tasks = [
            {
                "title": "测试任务1",
                "urgency": 8,
                "importance": 7,
                "effort": 3
            },
            {
                "title": "测试任务2", 
                "urgency": 5,
                "importance": 9,
                "effort": 6
            }
        ]
        
        result = framework.execute_skill("priority_sorter", test_tasks)
        if result["success"]:
            print("✅ 优先级排序测试通过!")
            print(f"   排序结果: {len(result['result']['prioritized_tasks'])} 个任务")
        else:
            print(f"❌ 优先级排序测试失败: {result['error']}")
        
        # 保存上下文
        framework.save_context()
        print("✅ 系统数据保存成功!")
        
        print("\n🎉 框架测试完成!")
        
    except Exception as e:
        print(f"❌ 框架测试失败: {e}")


def create_shortcut():
    """创建快捷方式"""
    print("📋 创建快捷方式...")
    
    # 创建Windows批处理文件
    batch_content = """@echo off
echo 启动多技能框架系统...
cd /d "%~dp0"
python start_framework.py --cli
pause
"""
    
    batch_file = "启动框架.bat"
    with open(batch_file, 'w', encoding='gbk') as f:
        f.write(batch_content)
    
    print(f"✅ 已创建快捷方式: {batch_file}")
    print("💡 双击此文件即可启动框架")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='多技能框架系统')
    parser.add_argument('--cli', action='store_true', help='启动命令行界面')
    parser.add_argument('--web', action='store_true', help='启动Web界面')
    parser.add_argument('--test', action='store_true', help='测试框架功能')
    parser.add_argument('--shortcut', action='store_true', help='创建快捷方式')
    
    args = parser.parse_args()
    
    # 显示欢迎信息
    print("\n" + "="*60)
    print("🧠 多技能框架系统 v1.0.0")
    print("="*60)
    
    if args.cli:
        start_cli_interface()
    elif args.web:
        start_web_interface()
    elif args.test:
        test_framework()
    elif args.shortcut:
        create_shortcut()
    else:
        # 默认启动命令行界面
        start_cli_interface()


if __name__ == "__main__":
    main()