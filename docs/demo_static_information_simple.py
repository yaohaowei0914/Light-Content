#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态信息提取提示系统简单演示
"""

from lightce.prompt.static_information import (
    InformationLevel, InformationType,
    get_information_prompt, get_all_information_prompts,
    get_information_workflow, get_level_description
)

def main():
    """主演示函数"""
    print("静态信息提取提示系统演示")
    print("=" * 60)
    
    # 测试文本
    test_text = """
    张三，男，1985年3月15日出生，身份证号：110101198503151234，
    联系电话：13812345678，邮箱：zhangsan@example.com，
    地址：北京市朝阳区建国路88号，邮编：100020，
    现任ABC公司技术部经理，月薪15000元。
    """
    
    print(f"测试文本: {test_text.strip()}")
    print(f"文本长度: {len(test_text)} 字符")
    
    # 演示不同级别
    for level in InformationLevel:
        print(f"\n{'='*20} {level.value.upper()} 级别 {'='*20}")
        
        # 获取级别描述
        description = get_level_description(level)
        print(f"描述: {description}")
        
        # 获取工作流
        workflow = get_information_workflow(level, test_text)
        print(f"工作流步骤数: {len(workflow['workflow_steps'])}")
        print("工作流步骤:")
        for step in workflow['workflow_steps']:
            print(f"  {step}")
        
        # 获取提示词
        prompts = get_all_information_prompts(level, text=test_text)
        print(f"提示词数量: {len(prompts)}")
        print("支持的提取类型:")
        for information_type in prompts.keys():
            print(f"  - {information_type}")
        
        # 显示一个示例提示词
        if prompts:
            first_type = list(prompts.keys())[0]
            first_prompt = prompts[first_type]
            print(f"\n{first_type} 示例提示词:")
            print("-" * 40)
            print(first_prompt[:300] + "..." if len(first_prompt) > 300 else first_prompt)
    
    # 演示特定类型的提取
    print(f"\n{'='*20} 特定类型提取演示 {'='*20}")
    
    # 联系信息提取演示
    print("\n联系信息提取演示:")
    try:
        contact_prompt = get_information_prompt(
            InformationLevel.BASIC, 
            InformationType.CONTACT, 
            text=test_text
        )
        print("联系信息提取提示词:")
        print("-" * 40)
        print(contact_prompt[:400] + "..." if len(contact_prompt) > 400 else contact_prompt)
    except ValueError as e:
        print(f"联系信息提取失败: {e}")
    
    # 个人信息提取演示
    print(f"\n{'='*20} 个人信息提取演示 {'='*20}")
    try:
        personal_prompt = get_information_prompt(
            InformationLevel.INTERMEDIATE, 
            InformationType.PERSONAL, 
            text=test_text
        )
        print("个人信息提取提示词:")
        print("-" * 40)
        print(personal_prompt[:400] + "..." if len(personal_prompt) > 400 else personal_prompt)
    except ValueError as e:
        print(f"个人信息提取失败: {e}")
    
    # 数字信息提取演示
    print(f"\n{'='*20} 数字信息提取演示 {'='*20}")
    try:
        numeric_prompt = get_information_prompt(
            InformationLevel.INTERMEDIATE, 
            InformationType.NUMERIC, 
            text=test_text
        )
        print("数字信息提取提示词:")
        print("-" * 40)
        print(numeric_prompt[:400] + "..." if len(numeric_prompt) > 400 else numeric_prompt)
    except ValueError as e:
        print(f"数字信息提取失败: {e}")
    
    print(f"\n{'='*20} 演示完成 {'='*20}")
    print("静态信息提取提示系统已成功创建！")
    print("系统支持4个级别、8种类型的静态信息提取功能。")

if __name__ == "__main__":
    main() 