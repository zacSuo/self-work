#!/usr/bin/env python3
"""
私人数据规则检查器

这个脚本确保所有创建的文件遵循私人数据存储规则：
1. 所有包含私人信息的文件必须保存到 private_data/ 目录
2. 代码中不能直接引用私人文件（应引用示例文件）
3. .gitignore 必须包含所有私人文件类型
"""

import os
import json
import re
import sys
from datetime import datetime

class PrivateDataRuleChecker:
    """私人数据规则检查器"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.private_dir = os.path.join(self.project_root, "private_data")
        self.gitignore_path = os.path.join(self.project_root, ".gitignore")
        
        # 私人信息关键词（扩展定义）
        self.private_keywords = [
            # 个人信息
            "name", "姓名", "张三", "李四", "wangwu", "lisi", 
            "email", "邮箱", "phone", "电话", "mobile", "手机",
            "address", "地址", "birthday", "生日",
            
            # 工作信息
            "work", "工作", "job", "职位", "company", "公司",
            "project", "项目", "task", "任务", "todo", "待办",
            "meeting", "会议", "schedule", "日程", "plan", "计划",
            "team", "团队", "colleague", "同事",
            
            # 具体内容
            "content", "内容", "details", "细节", "description", "描述",
            "notes", "笔记", "thoughts", "想法",
            
            # 时间信息
            "time", "时间", "date", "日期", "hour", "小时",
            "duration", "时长", "start", "开始", "end", "结束",
            
            # 本地信息
            "localhost", "127.0.0.1", "192.168", "10.0", "C:/",
            "D:/", "Users", "AppData", "Roaming", "IWITH",
            "workspace", "工作区", "project_root", "项目根目录"
        ]
        
        # 私人文件类型后缀
        self.private_suffixes = [
            ".personal.json", ".work.json", ".meeting.json", 
            ".schedule.json", ".plan.json", ".todo.json", 
            ".task.json", ".event.json", ".record.json", 
            ".memory.json", ".history.json", ".local.json",
            ".user.json"
        ]
        
        # 必须排除的文件类型
        self.must_exclude = [
            ".bat", ".log", ".backup"
        ]
    
    def check_new_file(self, file_path, content):
        """
        检查新创建的文件是否包含私人信息
        
        Args:
            file_path: 文件路径
            content: 文件内容
            
        Returns:
            tuple: (is_private, suggested_path, reason)
        """
        file_name = os.path.basename(file_path)
        
        # 检查文件后缀
        for suffix in self.private_suffixes:
            if file_name.endswith(suffix):
                return (True, self.get_suggested_path(file_path), 
                        f"文件后缀 {suffix} 表示这是私人文件")
        
        # 检查内容中的私人信息关键词
        if isinstance(content, str):
            for keyword in self.private_keywords:
                if keyword.lower() in content.lower():
                    return (True, self.get_suggested_path(file_path),
                            f"内容包含私人信息关键词: {keyword}")
        
        # 检查批处理文件
        if file_name.endswith(".bat"):
            return (True, self.get_suggested_path(file_path),
                    "批处理文件包含本地路径信息")
        
        # 检查是否是个人配置文件
        if file_name in ["config.json", "settings.json", "preferences.json"]:
            return (True, self.get_suggested_path(file_path),
                    "配置文件可能包含个人设置")
        
        # 如果是JSON文件，检查内容
        if file_name.endswith(".json"):
            try:
                data = json.loads(content)
                # 检查JSON中的私人信息字段
                if isinstance(data, dict):
                    for key in data.keys():
                        for keyword in self.private_keywords:
                            if keyword.lower() in key.lower():
                                return (True, self.get_suggested_path(file_path),
                                        f"JSON字段名包含私人信息: {key}")
            except json.JSONDecodeError:
                pass
        
        return (False, file_path, "文件不包含私人信息")
    
    def get_suggested_path(self, original_path):
        """
        根据文件类型和内容，建议保存到 private_data/ 的哪个子目录
        
        Args:
            original_path: 原始文件路径
            
        Returns:
            str: 建议的路径
        """
        file_name = os.path.basename(original_path)
        
        # 根据文件后缀确定目录
        if file_name.endswith(".json"):
            if any(suffix in file_name for suffix in ["personal", "work", "meeting", "todo"]):
                return os.path.join(self.private_dir, "data", file_name)
            elif any(suffix in file_name for suffix in ["local", "user"]):
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
            if "PRIVATE" in file_name or "NOTE" in file_name:
                return os.path.join(self.private_dir, "notes", file_name)
        
        # 默认保存到 data 目录
        return os.path.join(self.private_dir, "data", file_name)
    
    def check_code_references(self):
        """
        检查代码中的文件引用，确保不直接引用私人文件
        
        Returns:
            list: 发现的问题列表
        """
        problems = []
        
        # 检查所有Python文件
        for file in os.listdir(self.project_root):
            if file.endswith(".py"):
                file_path = os.path.join(self.project_root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 查找直接引用私人文件的代码
                    patterns = [
                        r'open\("([^"]+\.json)"\)',
                        r'open\("([^"]+\.bat)"\)',
                        r'open\("([^"]+\.log)"\)',
                        r'with open\("([^"]+\.json)"\)',
                        r'with open\("([^"]+\.bat)"\)',
                        r'with open\("([^"]+\.log)"\)',
                        r'load_daily_todos\("([^"]+\.json)"\)',
                        r'save_to_file\("([^"]+\.json)"\)',
                        r'read_file\("([^"]+\.json)"\)',
                        r'write_file\("([^"]+\.json)"\)'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # 检查是否是私人文件引用
                            if match and not match.startswith("private_data/") and not match.endswith("_EXAMPLE"):
                                problems.append({
                                    "file": file,
                                    "line": self.find_line_number(content, match),
                                    "reference": match,
                                    "suggestion": f"private_data/data/{match}"
                                })
                except Exception as e:
                    pass
        
        return problems
    
    def find_line_number(self, content, search_text):
        """
        查找文本在内容中的行号
        
        Args:
            content: 文件内容
            search_text: 要查找的文本
            
        Returns:
            int: 行号
        """
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if search_text in line:
                return i + 1
        return 0
    
    def check_gitignore(self):
        """
        检查.gitignore文件是否包含必要的排除规则
        
        Returns:
            list: 缺失的规则列表
        """
        missing_rules = []
        
        try:
            with open(self.gitignore_path, 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
            
            # 检查必须排除的文件类型
            for suffix in self.must_exclude:
                if f"*{suffix}" not in gitignore_content:
                    missing_rules.append(f"*.{suffix}")
            
            # 检查私人文件后缀
            for suffix in self.private_suffixes:
                if f"*{suffix}" not in gitignore_content:
                    missing_rules.append(f"*.{suffix}")
            
            # 检查private_data目录
            if "private_data/" not in gitignore_content:
                missing_rules.append("private_data/")
            
        except FileNotFoundError:
            missing_rules = [".gitignore文件不存在"]
        
        return missing_rules
    
    def enforce_rule(self, file_path):
        """
        强制执行规则：如果文件包含私人信息，移动到private_data目录
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否成功移动
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            is_private, suggested_path, reason = self.check_new_file(file_path, content)
            
            if is_private:
                # 创建目标目录
                target_dir = os.path.dirname(suggested_path)
                os.makedirs(target_dir, exist_ok=True)
                
                # 移动文件
                os.rename(file_path, suggested_path)
                
                # 创建示例文件
                example_path = f"{os.path.basename(file_path)}_EXAMPLE"
                example_path = os.path.join(self.project_root, example_path)
                
                # 创建示例文件内容（去除私人信息）
                example_content = self.create_example_content(content)
                with open(example_path, 'w', encoding='utf-8') as f:
                    f.write(example_content)
                
                # 更新.gitignore
                self.update_gitignore(file_path)
                
                print(f"[强制] 文件 {file_path} 包含私人信息 ({reason})")
                print(f"[强制] 已移动到: {suggested_path}")
                print(f"[强制] 示例文件已创建: {example_path}")
                
                return True
            else:
                print(f"[安全] 文件 {file_path} 不包含私人信息")
                return False
                
        except Exception as e:
            print(f"[错误] 处理文件 {file_path} 时出错: {e}")
            return False
    
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
            
            # 替换私人信息字段
            example_data = {}
            for key, value in data.items():
                # 如果是个人信息字段，替换为示例值
                if isinstance(key, str):
                    for keyword in self.private_keywords:
                        if keyword.lower() in key.lower():
                            example_data[key] = f"示例_{keyword}"
                        else:
                            example_data[key] = value
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
    
    def update_gitignore(self, file_path):
        """
        更新.gitignore文件，添加对应的排除规则
        
        Args:
            file_path: 文件路径
        """
        file_name = os.path.basename(file_path)
        
        try:
            with open(self.gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加文件名的排除规则
            if file_name not in content:
                # 添加到文件类型排除区域
                if file_name.endswith(".json"):
                    # 找到合适的区域添加
                    if "# 个人隐私数据和配置文件 - 扩展定义" in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith("# 个人隐私数据和配置文件 - 扩展定义"):
                                # 在下一行添加排除规则
                                lines.insert(i + 2, file_name)
                                content = '\n'.join(lines)
                                break
                
                elif file_name.endswith(".bat"):
                    if "# 批处理文件（包含本地路径）" in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith("# 批处理文件（包含本地路径）"):
                                lines.insert(i + 2, file_name)
                                content = '\n'.join(lines)
                                break
            
            # 写入更新后的内容
            with open(self.gitignore_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"[更新] .gitignore 已更新，排除 {file_name}")
            
        except Exception as e:
            print(f"[错误] 更新.gitignore时出错: {e}")
    
    def run_comprehensive_check(self):
        """
        运行全面的隐私保护检查
        
        Returns:
            dict: 检查结果
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "code_references": [],
            "gitignore_missing": [],
            "private_files_in_root": [],
            "total_files_checked": 0
        }
        
        print("=" * 60)
        print("[系统] 隐私保护全面检查")
        print("=" * 60)
        
        # 检查代码引用
        print("\n[检查] 检查代码中的文件引用...")
        code_problems = self.check_code_references()
        results["code_references"] = code_problems
        
        if code_problems:
            print(f"[警告] 发现 {len(code_problems)} 个代码引用问题:")
            for problem in code_problems:
                print(f"  - {problem['file']}: 行 {problem['line']} 引用 {problem['reference']}")
                print(f"    建议改为: {problem['suggestion']}")
        else:
            print("[通过] 代码引用检查通过")
        
        # 检查.gitignore
        print("\n[检查] 检查.gitignore配置...")
        gitignore_missing = self.check_gitignore()
        results["gitignore_missing"] = gitignore_missing
        
        if gitignore_missing:
            print(f"[警告] .gitignore缺少 {len(gitignore_missing)} 个规则:")
            for rule in gitignore_missing:
                print(f"  - {rule}")
        else:
            print("[通过] .gitignore检查通过")
        
        # 检查根目录中的私人文件
        print("\n[检查] 检查根目录中的私人文件...")
        root_files = os.listdir(self.project_root)
        private_files = []
        
        for file_name in root_files:
            if file_name not in ["private_data", ".gitignore", "PRIVATE_DATA_RULE.md"]:
                file_path = os.path.join(self.project_root, file_name)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        is_private, _, reason = self.check_new_file(file_path, content)
                        if is_private:
                            private_files.append({
                                "file": file_name,
                                "reason": reason
                            })
                    except Exception:
                        pass
        
        results["private_files_in_root"] = private_files
        
        if private_files:
            print(f"[警告] 根目录中发现 {len(private_files)} 个私人文件:")
            for file_info in private_files:
                print(f"  - {file_info['file']}: {file_info['reason']}")
        else:
            print("[通过] 根目录中无私人文件")
        
        results["total_files_checked"] = len(root_files)
        
        # 总结
        print("\n" + "=" * 60)
        print("[总结] 隐私保护检查结果")
        print("=" * 60)
        
        total_issues = len(code_problems) + len(gitignore_missing) + len(private_files)
        
        if total_issues == 0:
            print("[完美] 所有检查通过！您的隐私保护配置完整")
            print("[建议] 可以安全地将代码提交到Git仓库")
        else:
            print(f"[问题] 发现 {total_issues} 个隐私保护问题")
            print("[建议] 请先解决这些问题再提交代码")
        
        return results
    
def main():
    """主函数"""
    checker = PrivateDataRuleChecker()
    
    # 运行全面检查
    results = checker.run_comprehensive_check()
    
    # 保存检查结果
    results_file = os.path.join(checker.private_dir, "logs", "privacy_check.json")
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n[保存] 检查结果已保存到: {results_file}")
    
    # 提供修复建议
    if results["code_references"]:
        print("\n[修复] 代码引用问题修复建议:")
        print("1. 修改代码中的文件路径引用")
        print("2. 使用示例文件作为默认值")
        print("3. 动态检查 private_data/ 目录是否存在私人文件")
    
    if results["gitignore_missing"]:
        print("\n[修复] .gitignore问题修复建议:")
        print("1. 添加缺失的排除规则到 .gitignore")
        print("2. 确保所有私人文件类型都被排除")
    
    if results["private_files_in_root"]:
        print("\n[修复] 根目录私人文件修复建议:")
        print("1. 使用 move_private_files.py 工具移动文件")
        print("2. 创建对应的示例文件")
        print("3. 更新代码引用")
    
if __name__ == "__main__":
    main()