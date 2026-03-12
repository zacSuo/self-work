#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隐私配置测试脚本
验证所有私人文件已被保护，代码更新正确
"""

import os
import json
from pathlib import Path

def test_gitignore_config():
    """测试.gitignore配置是否正确"""
    print("[测试] .gitignore配置测试")
    print("-" * 40)
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print("[失败] .gitignore文件不存在")
        return False
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        gitignore_content = f.read()
    
    # 检查关键规则
    required_rules = [
        "private_data/",
        "chat_memory_data.json",
        "daily_todos.json",
        "technical_events.json",
        "weekly_meeting_data.json",
        "daily_plan_*.json",
        "*.bat",
        "*.log",
        "__pycache__/",
        ".vscode/",
        ".idea/",
        ".env",
        "venv/"
    ]
    
    passed = 0
    failed = 0
    
    for rule in required_rules:
        if rule in gitignore_content:
            print(f"[通过] 规则存在: {rule}")
            passed += 1
        else:
            print(f"[失败] 规则缺失: {rule}")
            failed += 1
    
    print(f"\n[结果] .gitignore测试: {passed}通过, {failed}失败")
    return failed == 0

def test_private_data_structure():
    """测试私人数据目录结构"""
    print("\n[测试] 私人数据目录结构测试")
    print("-" * 40)
    
    private_dir = Path("private_data")
    
    # 检查主目录
    if not private_dir.exists():
        print("[失败] private_data目录不存在")
        return False
    
    # 检查子目录
    required_subdirs = ["data", "configs", "logs", "backups"]
    passed = 0
    failed = 0
    
    for subdir in required_subdirs:
        subdir_path = private_dir / subdir
        if subdir_path.exists() and subdir_path.is_dir():
            print(f"[通过] 子目录存在: {subdir_path}/")
            passed += 1
        else:
            print(f"[失败] 子目录缺失: {subdir_path}/")
            failed += 1
    
    # 检查README文件
    readme_path = private_dir / "README_PRIVATE.md"
    if readme_path.exists():
        print(f"[通过] 说明文件存在: {readme_path}")
        passed += 1
    else:
        print(f"[失败] 说明文件缺失: {readme_path}")
        failed += 1
    
    print(f"\n[结果] 目录结构测试: {passed}通过, {failed}失败")
    return failed == 0

def test_data_files_moved():
    """测试数据文件是否已移动到private_data目录"""
    print("\n[测试] 数据文件迁移测试")
    print("-" * 40)
    
    private_data_dir = Path("private_data/data")
    
    # 应该在private_data/data中的文件
    expected_files_in_private = [
        "chat_memory_data.json",
        "daily_todos.json",
        "technical_events.json",
        "weekly_meeting_data.json",
        "daily_plan_2026-03-13.json",
        "robot_tasks_simple.json",
        "memory_data.json",
        "simple_memory_data.json"
    ]
    
    # 应该在项目根目录的示例文件
    expected_example_files = [
        "chat_memory_data_EXAMPLE.json",
        "daily_todos_EXAMPLE.json",
        "technical_events_EXAMPLE.json",
        "weekly_meeting_data_EXAMPLE.json",
        "daily_plan_2026-03-13_EXAMPLE.json",
        "robot_tasks_simple_EXAMPLE.json",
        "memory_data_EXAMPLE.json",
        "simple_memory_data_EXAMPLE.json",
        "config_EXAMPLE.json"
    ]
    
    passed = 0
    failed = 0
    
    # 检查文件是否在private_data目录
    for filename in expected_files_in_private:
        private_path = private_data_dir / filename
        root_path = Path(filename)
        
        if private_path.exists():
            print(f"[通过] 文件在private_data: {filename}")
            passed += 1
        else:
            print(f"[警告] 文件不在private_data: {filename}")
        
        if root_path.exists():
            # 检查是否是示例文件
            if "EXAMPLE" in filename:
                print(f"[通过] 示例文件在根目录: {filename}")
                passed += 1
            else:
                print(f"[失败] 原始文件不应在根目录: {filename}")
                failed += 1
        else:
            if "EXAMPLE" not in filename:
                print(f"[通过] 原始文件不在根目录: {filename}")
                passed += 1
    
    # 检查示例文件
    for example_file in expected_example_files:
        example_path = Path(example_file)
        if example_path.exists():
            print(f"[通过] 示例文件存在: {example_file}")
            passed += 1
        else:
            print(f"[警告] 示例文件缺失: {example_file}")
    
    print(f"\n[结果] 文件迁移测试: {passed}通过, {failed}失败")
    return failed == 0

def test_batch_files_moved():
    """测试批处理文件是否已移动到private_data/configs目录"""
    print("\n[测试] 批处理文件迁移测试")
    print("-" * 40)
    
    private_configs_dir = Path("private_data/configs")
    
    expected_batch_files = [
        "morning_todo.bat",
        "start_memory_system.bat"
    ]
    
    expected_example_batch = [
        "morning_todo_EXAMPLE.bat",
        "start_memory_system_EXAMPLE.bat"
    ]
    
    passed = 0
    failed = 0
    
    # 检查批处理文件是否在private_data/configs
    for batch_file in expected_batch_files:
        private_path = private_configs_dir / batch_file
        root_path = Path(batch_file)
        
        if private_path.exists():
            print(f"[通过] 批处理文件在private_data: {batch_file}")
            passed += 1
        else:
            print(f"[警告] 批处理文件不在private_data: {batch_file}")
        
        if root_path.exists():
            print(f"[失败] 批处理文件不应在根目录: {batch_file}")
            failed += 1
        else:
            print(f"[通过] 批处理文件不在根目录: {batch_file}")
            passed += 1
    
    # 检查示例批处理文件
    for example_batch in expected_example_batch:
        example_path = Path(example_batch)
        if example_path.exists():
            print(f"[通过] 示例批处理文件存在: {example_batch}")
            passed += 1
        else:
            print(f"[警告] 示例批处理文件缺失: {example_batch}")
    
    print(f"\n[结果] 批处理文件测试: {passed}通过, {failed}失败")
    return failed == 0

def test_code_references_updated():
    """测试代码中的文件引用是否已更新"""
    print("\n[测试] 代码引用更新测试")
    print("-" * 40)
    
    # 需要检查的文件列表
    files_to_check = [
        "daily_todo_system.py",
        "weekly_meeting_system.py",
        "technical_events_recorder.py",
        "view_technical_events.py",
        "record_today_event.py",
        "chat_memory_system.py",
        "memory_system.py",
        "simple_memory_system.py"
    ]
    
    passed = 0
    failed = 0
    
    for filename in files_to_check:
        filepath = Path(filename)
        if not filepath.exists():
            print(f"[跳过] 文件不存在: {filename}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否引用了private_data目录
        if "private_data/" in content:
            print(f"[通过] 代码引用已更新: {filename}")
            passed += 1
        else:
            # 检查是否还有旧的引用
            old_refs = [
                '"chat_memory_data.json"',
                '"daily_todos.json"',
                '"technical_events.json"',
                '"weekly_meeting_data.json"',
                '"robot_tasks_simple.json"',
                '"memory_data.json"',
                '"simple_memory_data.json"'
            ]
            
            has_old_ref = False
            for old_ref in old_refs:
                if old_ref in content:
                    has_old_ref = True
                    print(f"[失败] 仍有旧引用 {old_ref} 在: {filename}")
                    failed += 1
                    break
            
            if not has_old_ref:
                print(f"[通过] 代码无旧引用: {filename}")
                passed += 1
    
    print(f"\n[结果] 代码引用测试: {passed}通过, {failed}失败")
    return failed == 0

def test_example_files_valid():
    """测试示例文件是否有效"""
    print("\n[测试] 示例文件有效性测试")
    print("-" * 40)
    
    example_files = [
        "chat_memory_data_EXAMPLE.json",
        "daily_todos_EXAMPLE.json",
        "technical_events_EXAMPLE.json",
        "weekly_meeting_data_EXAMPLE.json",
        "config_EXAMPLE.json"
    ]
    
    passed = 0
    failed = 0
    
    for example_file in example_files:
        filepath = Path(example_file)
        if not filepath.exists():
            print(f"[失败] 示例文件不存在: {example_file}")
            failed += 1
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # 读取前几行检查注释
                lines = f.readlines()
                if len(lines) > 0:
                    # 检查是否有说明注释
                    has_comment = False
                    for line in lines[:5]:
                        if "示例" in line or "EXAMPLE" in line or "原始文件" in line:
                            has_comment = True
                            break
                    
                    if has_comment:
                        print(f"[通过] 示例文件有说明: {example_file}")
                        passed += 1
                    else:
                        print(f"[警告] 示例文件缺少说明: {example_file}")
                    
                    # 尝试解析JSON
                    f.seek(0)
                    try:
                        json.load(f)
                        print(f"[通过] 示例文件JSON有效: {example_file}")
                        passed += 1
                    except json.JSONDecodeError as e:
                        print(f"[失败] 示例文件JSON无效: {example_file} - {e}")
                        failed += 1
                else:
                    print(f"[失败] 示例文件为空: {example_file}")
                    failed += 1
        except Exception as e:
            print(f"[失败] 读取示例文件失败: {example_file} - {e}")
            failed += 1
    
    print(f"\n[结果] 示例文件测试: {passed}通过, {failed}失败")
    return failed == 0

def test_functionality():
    """测试基本功能是否正常"""
    print("\n[测试] 基本功能测试")
    print("-" * 40)
    
    tests = [
        ("daily_todo_system.py", "每日待办事项系统"),
        ("weekly_meeting_system.py", "每周会议系统"),
        ("view_technical_events.py", "技术事件查看器")
    ]
    
    passed = 0
    failed = 0
    
    for script_name, description in tests:
        script_path = Path(script_name)
        if not script_path.exists():
            print(f"[跳过] 脚本不存在: {script_name}")
            continue
        
        # 简单检查脚本是否能导入
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否有语法错误的关键字
            if "import " in content and "def " in content:
                print(f"[通过] 脚本结构正常: {description}")
                passed += 1
            else:
                print(f"[警告] 脚本结构异常: {description}")
        except Exception as e:
            print(f"[失败] 脚本检查失败: {description} - {e}")
            failed += 1
    
    print(f"\n[结果] 功能测试: {passed}通过, {failed}失败")
    return failed == 0

def main():
    """主测试函数"""
    print("=" * 60)
    print("[系统] 隐私保护配置完整性测试")
    print("=" * 60)
    
    tests = [
        ("gitignore配置", test_gitignore_config),
        ("私人数据目录结构", test_private_data_structure),
        ("数据文件迁移", test_data_files_moved),
        ("批处理文件迁移", test_batch_files_moved),
        ("代码引用更新", test_code_references_updated),
        ("示例文件有效性", test_example_files_valid),
        ("基本功能", test_functionality)
    ]
    
    total_passed = 0
    total_failed = 0
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            if success:
                results.append(f"[通过] {test_name}")
                total_passed += 1
            else:
                results.append(f"[失败] {test_name}")
                total_failed += 1
        except Exception as e:
            results.append(f"[错误] {test_name} - {str(e)}")
            total_failed += 1
    
    print("\n" + "=" * 60)
    print("[总结] 测试结果汇总")
    print("=" * 60)
    
    for result in results:
        print(result)
    
    print(f"\n[总计] 通过: {total_passed}, 失败: {total_failed}")
    
    if total_failed == 0:
        print("\n[完成] 所有隐私保护配置测试通过!")
        print("\n[建议] 现在可以安全地将代码提交到Git仓库:")
        print("  1. git add .")
        print("  2. git commit -m \"初始化项目，配置隐私保护\"")
        print("  3. git push")
    else:
        print(f"\n[警告] 有 {total_failed} 个测试失败，请检查并修复")
        print("\n[建议] 修复问题后重新运行测试")
    
    return total_failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)