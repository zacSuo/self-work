#!/usr/bin/env python3
"""
自动隐私保护强制执行器

这个脚本在每次创建新文件时自动检查文件内容，
如果包含私人信息，自动保存到 private_data/ 目录，
并创建相应的示例文件。

工作原理：
1. 检查新文件内容中的私人信息关键词
2. 自动创建对应的示例文件（不含私人信息）
3. 自动更新.gitignore文件
4. 提供使用示例
"""

import os
import json
import re
import sys
import time
from datetime import datetime

class AutoPrivacyEnforcer:
    """自动隐私保护强制执行器"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.private_dir = os.path.join(self.project_root, "private_data")
        self.gitignore_path = os.path.join(self.project_root, ".gitignore")
        self.rule_path = os.path.join(self.project_root, "docs", "PRIVATE_DATA_RULE.md")
        
        # 私人信息关键词（扩展定义）
        self.private_keywords = [
            # 个人信息
            "张三", "李四", "王五", "赵六", "陈七", "刘八",
            "IWITH", "workbuddy", "d:/code/workbuddy",
            "C:/Users/IWITH", "AppData", "Roaming", "WindowsPowerShell",
            
            # 工作信息
            "项目", "任务", "会议", "日程", "计划", "待办",
            "技术", "算法", "优化", "测试", "团队", "同事",
            
            # 具体内容
            "优化机器人底盘控制算法", "处理传感器数据",
            "完成本周工作总结", "准备下周计划",
            "晨会", "站会", "评审会", "周会",
            
            # 时间信息
            "9:00-12:00", "13:30-18:00", "周一至周四",
            "周五晚上", "周六日", "休息",
            
            # 通用敏感词
            "password", "secret", "private", "confidential",
            "personal", "company", "team", "project"
        ]
        
        # 私人文件类型
        self.private_file_types = [
            ".personal.json", ".work.json", ".meeting.json",
            ".schedule.json", ".plan.json", ".todo.json",
            ".task.json", ".event.json", ".record.json",
            ".memory.json", ".history.json", ".log.json"
        ]
        
        # 个人配置文件
        self.config_file_types = [
            "config.json", "settings.json", "preferences.json",
            ".local.json", ".user.json"
        ]
    
    def check_file(self, file_path):
        """
        检查文件是否包含私人信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            dict: 检查结果
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_name = os.path.basename(file_path)
            
            # 检查文件后缀
            for suffix in self.private_file_types:
                if file_name.endswith(suffix):
                    return {
                        "is_private": True,
                        "reason": f"文件后缀 {suffix} 表示私人文件",
                        "content": content,
                        "suggested_path": os.path.join(self.private_dir, "data", file_name)
                    }
            
            # 检查配置文件
            for config_type in self.config_file_types:
                if file_name == config_type or file_name.endswith(config_type):
                    return {
                        "is_private": True,
                        "reason": f"配置文件 {file_name} 可能包含个人设置",
                        "content": content,
                        "suggested_path": os.path.join(self.private_dir, "configs", file_name)
                    }
            
            # 检查内容中的私人信息关键词
            private_keywords_found = []
            for keyword in self.private_keywords:
                if keyword.lower() in content.lower():
                    private_keywords_found.append(keyword)
            
            if private_keywords_found:
                return {
                    "is_private": True,
                    "reason": f"内容包含私人信息关键词: {', '.join(private_keywords_found)}",
                    "content": content,
                    "suggested_path": self.get_suggested_path(file_name, content)
                }
            
            # 检查JSON格式中的字段名
            if file_name.endswith(".json"):
                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        sensitive_fields = []
                        for key in data.keys():
                            if any(kw.lower() in key.lower() for kw in self.private_keywords):
                                sensitive_fields.append(key)
                        
                        if sensitive_fields:
                            return {
                                "is_private": True,
                                "reason": f"JSON字段名包含私人信息: {', '.join(sensitive_fields)}",
                                "content": content,
                                "suggested_path": os.path.join(self.private_dir, "data", file_name)
                            }
                except json.JSONDecodeError:
                    pass
            
            return {
                "is_private": False,
                "reason": "文件不包含私人信息",
                "content": content,
                "suggested_path": file_path
            }
            
        except Exception as e:
            return {
                "is_private": False,
                "reason": f"检查文件时出错: {e}",
                "content": "",
                "suggested_path": file_path
            }
    
    def get_suggested_path(self, file_name, content):
        """
        根据文件内容和类型建议保存路径
        
        Args:
            file_name: 文件名
            content: 文件内容
            
        Returns:
            str: 建议的保存路径
        """
        # 根据文件后缀确定目录
        if file_name.endswith(".json"):
            # 检查内容关键词决定目录
            if any(keyword in content for keyword in ["个人", "姓名", "工作", "任务"]):
                return os.path.join(self.private_dir, "data", file_name)
            elif any(keyword in content for keyword in ["配置", "设置", "路径"]):
                return os.path.join(self.private_dir, "configs", file_name)
            else:
                return os.path.join(self.private_dir, "data", file_name)
        
        elif file_name.endswith(".bat"):
            return os.path.join(self.private_dir, "configs", file_name)
        
        elif file_name.endswith(".log"):
            return os.path.join(self.private_dir, "logs", file_name)
        
        elif file_name.endswith(".backup"):
            return os.path.join(self.private_dir, "backups", file_name)
        
        elif file_name.endswith(".md"):
            if "PRIVATE" in file_name or "NOTE" in file_name or "日志" in file_name:
                return os.path.join(self.private_dir, "notes", file_name)
        
        # 默认保存到 data 目录
        return os.path.join(self.private_dir, "data", file_name)
    
    def enforce_privacy(self, file_path):
        """
        强制执行隐私保护规则
        
        Args:
            file_path: 文件路径
            
        Returns:
            dict: 执行结果
        """
        result = self.check_file(file_path)
        
        if not result["is_private"]:
            return {
                "action": "none",
                "message": "文件不包含私人信息，无需特殊处理",
                "file": file_path
            }
        
        # 创建目标目录
        target_dir = os.path.dirname(result["suggested_path"])
        os.makedirs(target_dir, exist_ok=True)
        
        # 移动文件到 private_data
        os.rename(file_path, result["suggested_path"])
        
        # 创建示例文件
        example_file_name = f"{os.path.basename(file_path)}_EXAMPLE"
        example_path = os.path.join(self.project_root, "examples", example_file_name)
        os.makedirs(os.path.dirname(example_path), exist_ok=True)
        
        example_content = self.create_example_content(result["content"])
        with open(example_path, 'w', encoding='utf-8') as f:
            f.write(example_content)
        
        # 更新.gitignore
        self.update_gitignore(os.path.basename(file_path))
        
        # 更新PRIVATE_DATA_RULE.md
        self.update_rule_file(file_path, result["suggested_path"])
        
        return {
            "action": "moved",
            "message": f"文件包含私人信息 ({result['reason']})，已移动到 {result['suggested_path']}",
            "original_path": file_path,
            "new_path": result["suggested_path"],
            "example_path": example_path
        }
    
    def create_example_content(self, original_content):
        """
        创建示例文件内容（去除私人信息）
        
        Args:
            original_content: 原始内容
            
        Returns:
            str: 示例内容
        """
        # 如果是JSON文件，替换私人信息
        try:
            data = json.loads(original_content)
            
            # 创建示例数据
            example_data = {}
            for key, value in data.items():
                # 如果是字符串值，检查是否包含私人信息
                if isinstance(value, str):
                    # 替换私人信息关键词
                    example_value = value
                    for keyword in self.private_keywords:
                        if keyword in example_value:
                            example_value = example_value.replace(keyword, f"示例_{keyword}")
                    
                    # 如果是姓名、ID等个人信息
                    if key.lower() in ["name", "姓名", "username", "user"]:
                        example_value = "示例用户"
                    elif key.lower() in ["email", "邮箱", "phone", "电话"]:
                        example_value = "示例联系方式"
                    elif key.lower() in ["address", "地址", "location", "位置"]:
                        example_value = "示例地址"
                    elif key.lower() in ["password", "密码", "secret", "密钥"]:
                        example_value = "示例密码"
                    
                    example_data[key] = example_value
                else:
                    example_data[key] = value
            
            return json.dumps(example_data, indent=2)
        
        except json.JSONDecodeError:
            # 不是JSON文件，返回原始内容（稍作修改）
            example_content = original_content
            
            # 替换可能的私人信息
            for keyword in self.private_keywords:
                example_content = example_content.replace(keyword, f"示例_{keyword}")
            
            return example_content
    
    def update_gitignore(self, file_name):
        """
        更新.gitignore文件，添加对应的排除规则
        
        Args:
            file_name: 文件名
        """
        try:
            with open(self.gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加文件名的排除规则
            if file_name not in content:
                # 添加到文件类型排除区域
                if "# 个人隐私数据和配置文件 - 扩展定义" in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("# 个人隐私数据和配置文件 - 扩展定义"):
                            # 在下一行添加排除规则
                            lines.insert(i + 2, file_name)
                            break
                    
                    # 写入更新后的内容
                    content = '\n'.join(lines)
                    
            with open(self.gitignore_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"[更新] .gitignore 已更新，排除 {file_name}")
            
        except Exception as e:
            print(f"[错误] 更新.gitignore时出错: {e}")
    
    def update_rule_file(self, original_file, new_path):
        """
        更新PRIVATE_DATA_RULE.md文件，记录新的私人文件
        
        Args:
            original_file: 原始文件路径
            new_path: 新的文件路径
        """
        try:
            with open(self.rule_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加新的记录
            file_name = os.path.basename(original_file)
            new_entry = f"\n### 文件: {file_name}\n"
            new_entry += f"- **原始路径**: {original_file}\n"
            new_entry += f"- **新的路径**: {new_path}\n"
            new_entry += f"- **移动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            new_entry += f"- **示例文件**: examples/{file_name}_EXAMPLE\n"
            
            # 找到合适的位置添加
            if "## 示例" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("## 示例"):
                        lines.insert(i + 1, new_entry)
                        content = '\n'.join(lines)
                        break
            
            with open(self.rule_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[更新] PRIVATE_DATA_RULE.md 已更新，添加了 {file_name}")
            
        except Exception as e:
            print(f"[错误] 更新规则文件时出错: {e}")
    
    def check_all_existing_files(self):
        """
        检查所有已存在的文件，强制执行隐私规则
        
        Returns:
            list: 处理结果列表
        """
        results = []
        
        print("=" * 60)
        print("[系统] 检查所有已存在的文件")
        print("=" * 60)
        
        # 检查根目录中的所有文件
        for file_name in os.listdir(self.project_root):
            if file_name not in ["private_data", ".gitignore", "directory_organizer.py", "auto_privacy_enforcer.py"]:
                file_path = os.path.join(self.project_root, file_name)
                
                if os.path.isfile(file_path):
                    print(f"[检查] 检查文件: {file_name}")
                    
                    result = self.enforce_privacy(file_path)
                    if result["action"] == "moved":
                        results.append(result)
                        print(f"[移动] {result['message']}")
                    else:
                        print(f"[安全] {result['message']}")
        
        # 总结
        print("\n" + "=" * 60)
        print("[总结] 文件检查结果")
        print("=" * 60)
        
        moved_count = len(results)
        print(f"[统计] 移动了 {moved_count} 个私人文件")
        
        for result in results:
            print(f"  - {os.path.basename(result['original_path'])} → {result['new_path']}")
        
        print("\n[建议] 后续创建新文件时:")
        print("1. 使用此脚本自动检查文件内容")
        print("2. 遵循PRIVATE_DATA_RULE.md中的规则")
        print("3. 定期运行隐私检查器")
        
        return results
    
    def monitor_new_files(self, check_interval=60):
        """
        监控新创建的文件，自动强制执行隐私规则
        
        Args:
            check_interval: 检查间隔（秒）
        """
        print("=" * 60)
        print("[系统] 新文件监控器启动")
        print("=" * 60)
        
        print("[说明] 这个工具会监控新创建的文件")
        print("[说明] 如果文件包含私人信息，会自动移动到 private_data/")
        print("[说明] 同时创建示例文件在 examples/ 目录")
        
        # 初始文件列表
        existing_files = set(os.listdir(self.project_root))
        
        while True:
            # 检查新文件
            current_files = set(os.listdir(self.project_root))
            new_files = current_files - existing_files
            
            for file_name in new_files:
                if file_name not in ["private_data", ".gitignore", "directory_organizer.py", "auto_privacy_enforcer.py"]:
                    file_path = os.path.join(self.project_root, file_name)
                    
                    if os.path.isfile(file_path):
                        print(f"[发现] 新文件: {file_name}")
                        result = self.enforce_privacy(file_path)
                        
                        if result["action"] == "moved":
                            print(f"[处理] {result['message']}")
                        else:
                            print(f"[安全] {result['message']}")
            
            # 更新文件列表
            existing_files = current_files
            
            # 等待下一次检查
            time.sleep(check_interval)
    
def main():
    """主函数"""
    enforcer = AutoPrivacyEnforcer()
    
    print("=" * 60)
    print("[系统] 自动隐私保护强制执行器")
    print("=" * 60)
    
    print("\n[选项] 选择操作:")
    print("1. 检查所有已存在的文件")
    print("2. 监控新创建的文件")
    print("3. 测试单个文件")
    print("4. 查看帮助")
    
    choice = input("\n请输入选择 (1-4): ")
    
    if choice == "1":
        # 检查所有已存在的文件
        results = enforcer.check_all_existing_files()
        
        # 保存检查结果
        result_file = os.path.join(enforcer.private_dir, "logs", "enforcement_results.json")
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[保存] 检查结果已保存到: {result_file}")
    
    elif choice == "2":
        # 监控新创建的文件
        print("\n[监控] 开始监控新文件创建")
        print("[提示] 监控器将每60秒检查一次新文件")
        print("[提示] 按Ctrl+C停止监控")
        
        enforcer.monitor_new_files()
    
    elif choice == "3":
        # 测试单个文件
        file_path = input("请输入文件路径: ")
        
        if os.path.exists(file_path):
            result = enforcer.enforce_privacy(file_path)
            print(f"\n[结果] {result['message']}")
            
            if result["action"] == "moved":
                print(f"[示例] 示例文件创建在: {result['example_path']}")
        else:
            print(f"[错误] 文件不存在: {file_path}")
    
    elif choice == "4":
        # 查看帮助
        print("\n[帮助] 自动隐私保护强制执行器使用指南")
        print("===========================================")
        print("1. 每次创建新文件时，此工具会自动检查")
        print("2. 如果文件包含私人信息，会被移动到 private_data/")
        print("3. 同时创建示例文件在 examples/ 目录")
        print("4. 更新.gitignore文件，排除私人文件")
        print("5. 更新PRIVATE_DATA_RULE.md，记录处理过程")
        print("\n[规则] 什么是私人信息:")
        print("- 个人信息：姓名、联系方式、地址")
        print("- 工作信息：项目、任务、会议内容")
        print("- 时间信息：工作时间、会议时间")
        print("- 具体内容：具体工作描述、技术细节")
        print("\n[目录] 私人数据存储位置:")
        print("- private_data/data/ - 个人数据文件")
        print("- private_data/configs/ - 配置文件")
        print("- private_data/logs/ - 日志文件")
        print("- private_data/backups/ - 备份文件")
        print("- private_data/notes/ - 个人笔记")
        print("\n[示例] 示例文件位置:")
        print("- examples/ - 所有示例文件")
        
        # 创建使用示例
        print("\n[示例] 使用示例:")
        print("```python")
        print("# 创建新文件")
        print("new_data = {'name': '张三', 'task': '优化算法'}")
        print("with open('personal_task.json', 'w') as f:")
        print("    json.dump(new_data, f)")
        print("")
        print("# 自动隐私保护强制执行器将:")
        print("# 1. 检查文件内容")
        print("# 2. 发现包含私人信息")
        print("# 3. 移动到 private_data/data/personal_task.json")
        print("# 4. 创建 examples/personal_task_EXAMPLE.json")
        print("# 5. 更新.gitignore和规则文件")
        print("```")
    
    else:
        print("[错误] 无效的选择")

if __name__ == "__main__":
    main()