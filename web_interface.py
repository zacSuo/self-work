#!/usr/bin/env python3
"""
记忆系统Web界面
提供图形化界面来管理记忆系统
"""

import json
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from memory_system import MemorySystem

app = Flask(__name__)
memory_system = MemorySystem()


@app.route('/')
def index():
    """主页 - 显示系统概览"""
    summary = memory_system.generate_summary()
    
    # 获取最近数据
    recent_decisions = memory_system.get_recent_decisions(7)
    pending_tasks = memory_system.get_pending_tasks()
    high_priority_habits = memory_system.get_habits_by_priority(7)
    
    return render_template('index.html', 
                         summary=summary,
                         recent_decisions=recent_decisions,
                         pending_tasks=pending_tasks,
                         high_priority_habits=high_priority_habits)


@app.route('/habits')
def habits_page():
    """习惯管理页面"""
    habits = memory_system.habits
    return render_template('habits.html', habits=habits)


@app.route('/add_habit', methods=['POST'])
def add_habit():
    """添加新习惯"""
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        frequency = request.form.get('frequency')
        priority = int(request.form.get('priority', 5))
        
        if memory_system.add_habit(name, description, frequency, priority):
            return jsonify({'success': True, 'message': '习惯添加成功'})
        else:
            return jsonify({'success': False, 'message': '添加失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'错误: {str(e)}'})


@app.route('/update_habit_practice', methods=['POST'])
def update_habit_practice():
    """更新习惯实践记录"""
    try:
        habit_name = request.form.get('habit_name')
        success = request.form.get('success', 'true').lower() == 'true'
        
        if memory_system.update_habit_practice(habit_name, success):
            return jsonify({'success': True, 'message': '习惯实践记录更新成功'})
        else:
            return jsonify({'success': False, 'message': '更新失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'错误: {str(e)}'})


@app.route('/work_styles')
def work_styles_page():
    """工作方式页面"""
    work_styles = memory_system.work_styles
    return render_template('work_styles.html', work_styles=work_styles)


@app.route('/add_work_style', methods=['POST'])
def add_work_style():
    """添加工作方式"""
    try:
        category = request.form.get('category')
        description = request.form.get('description')
        effectiveness = int(request.form.get('effectiveness', 5))
        preferred_tools = request.form.get('preferred_tools', '').split(',')
        
        # 工作时间
        working_hours = {
            'morning': request.form.get('morning_hours', ''),
            'afternoon': request.form.get('afternoon_hours', ''),
            'evening': request.form.get('evening_hours', '')
        }
        
        if memory_system.add_work_style(category, description, effectiveness, 
                                       preferred_tools, working_hours):
            return jsonify({'success': True, 'message': '工作方式添加成功'})
        else:
            return jsonify({'success': False, 'message': '添加失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'错误: {str(e)}'})


@app.route('/decisions')
def decisions_page():
    """决策记录页面"""
    decisions = memory_system.decisions
    recent_decisions = memory_system.get_recent_decisions(30)
    return render_template('decisions.html', 
                         decisions=decisions,
                         recent_decisions=recent_decisions)


@app.route('/record_decision', methods=['POST'])
def record_decision():
    """记录决策"""
    try:
        decision_type = request.form.get('decision_type')
        description = request.form.get('description')
        factors = request.form.get('factors', '').split(',')
        outcome = request.form.get('outcome')
        confidence = int(request.form.get('confidence', 5))
        lessons = request.form.get('lessons', '')
        
        if memory_system.record_decision(decision_type, description, factors, 
                                        outcome, confidence, lessons):
            return jsonify({'success': True, 'message': '决策记录成功'})
        else:
            return jsonify({'success': False, 'message': '记录失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'错误: {str(e)}'})


@app.route('/tasks')
def tasks_page():
    """任务管理页面"""
    tasks = memory_system.tasks
    pending_tasks = memory_system.get_pending_tasks()
    return render_template('tasks.html', 
                         tasks=tasks,
                         pending_tasks=pending_tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    """添加新任务"""
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        deadline = request.form.get('deadline')
        estimated_hours = float(request.form.get('estimated_hours', 0))
        tags = request.form.get('tags', '').split(',')
        
        if memory_system.add_task(title, description, priority, deadline, 
                                 estimated_hours, tags):
            return jsonify({'success': True, 'message': '任务添加成功'})
        else:
            return jsonify({'success': False, 'message': '添加失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'错误: {str(e)}'})


@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    """更新任务状态"""
    try:
        title = request.form.get('title')
        status = request.form.get('status')
        actual_hours = request.form.get('actual_hours')
        
        if actual_hours:
            actual_hours = float(actual_hours)
        else:
            actual_hours = None
        
        if memory_system.update_task_status(title, status, actual_hours):
            return jsonify({'success': True, 'message': '任务状态更新成功'})
        else:
            return jsonify({'success': False, 'message': '更新失败'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'错误: {str(e)}'})


@app.route('/api/summary')
def api_summary():
    """API接口 - 获取系统摘要"""
    summary = memory_system.generate_summary()
    return jsonify(summary)


@app.route('/api/recent_activity')
def api_recent_activity():
    """API接口 - 获取最近活动"""
    recent_decisions = memory_system.get_recent_decisions(7)
    pending_tasks = memory_system.get_pending_tasks()
    
    # 转换为字典格式
    decisions_data = [
        {
            'type': d.decision_type,
            'description': d.description,
            'outcome': d.outcome,
            'timestamp': d.timestamp
        } for d in recent_decisions
    ]
    
    tasks_data = [
        {
            'title': t.title,
            'priority': t.priority,
            'deadline': t.deadline,
            'status': t.status
        } for t in pending_tasks
    ]
    
    return jsonify({
        'recent_decisions': decisions_data,
        'pending_tasks': tasks_data
    })


if __name__ == '__main__':
    print("启动记忆系统Web界面...")
    print("访问地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)