#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态信息提取工具演示
展示如何使用UniversalAgent和静态信息提取提示词进行静态信息提取
"""

import json
from lightce.tools.static_information import (
    StaticInformationAgent, StaticInformationConfig,
    create_static_information_agent, extract_static_information_with_agent,
    StaticInformationTool
)
from lightce.prompt.static_information import InformationLevel, InformationType

def demo_basic_extraction():
    """演示基础级别静态信息提取"""
    print("=" * 60)
    print("基础级别静态信息提取演示")
    print("=" * 60)
    
    test_text = """
    张三，男，28岁，软件工程师，毕业于清华大学计算机系。
    联系方式：zhangsan@example.com，电话：138-1234-5678。
    工作地址：北京市海淀区中关村软件园，月薪15000元。
    入职时间：2020年3月15日，技术栈：Python、Java、React。
    """
    
    # 创建基础级别的静态信息提取代理
    agent = create_static_information_agent("basic")
    
    # 执行提取
    result = agent.extract_information(test_text)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"提取级别: {result.information_level}")
    print(f"提取类型: {result.information_types}")
    print(f"成功状态: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"验证通过: {result.validation_passed}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取结果:")
        for information_type, information_result in result.results.items():
            print(f"\n--- {information_type.upper()} ---")
            if "error" in information_result:
                print(f"错误: {information_result['error']}")
            else:
                content = information_result['extracted_content']
                print(f"内容: {content[:300]}{'...' if len(content) > 300 else ''}")

def demo_intermediate_extraction():
    """演示中级级别静态信息提取"""
    print("\n" + "=" * 60)
    print("中级级别静态信息提取演示")
    print("=" * 60)
    
    test_text = """
    李四，女，32岁，产品经理，毕业于北京大学工商管理系。
    邮箱：lisi@company.com，手机：139-8765-4321。
    公司：腾讯科技有限公司，地址：深圳市南山区腾讯大厦。
    入职时间：2018年6月1日，年薪：25万元，部门：微信事业群。
    负责产品：微信小程序、企业微信，团队规模：15人。
    """
    
    # 创建中级级别的静态信息提取代理
    agent = create_static_information_agent("intermediate")
    
    # 执行提取
    result = agent.extract_information(test_text)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"提取级别: {result.information_level}")
    print(f"提取类型: {result.information_types}")
    print(f"成功状态: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"验证通过: {result.validation_passed}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        print("\n提取结果:")
        for information_type, information_result in result.results.items():
            print(f"\n--- {information_type.upper()} ---")
            if "error" in information_result:
                print(f"错误: {information_result['error']}")
            else:
                content = information_result['extracted_content']
                print(f"内容: {content[:300]}{'...' if len(content) > 300 else ''}")

def demo_specific_information_types():
    """演示特定类型的静态信息提取"""
    print("\n" + "=" * 60)
    print("特定类型静态信息提取演示")
    print("=" * 60)
    
    test_text = """
    王五，男，35岁，架构师，毕业于上海交通大学计算机系。
    联系方式：wangwu@tech.com，电话：186-1111-2222。
    公司：阿里巴巴集团，地址：杭州市余杭区文一西路969号。
    入职时间：2016年9月1日，年薪：35万元，股票期权：1000股。
    技术栈：Java、Spring、MySQL、Redis、Docker、Kubernetes。
    项目经验：双11大促系统架构、支付宝核心支付系统。
    """
    
    # 创建代理
    agent = create_static_information_agent("basic")
    
    # 指定特定类型进行提取
    specific_types = [InformationType.CONTACT, InformationType.PERSONAL, InformationType.FINANCIAL]
    
    result = agent.extract_information(test_text, specific_types)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"指定提取类型: {[t.value for t in specific_types]}")
    print(f"成功状态: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"验证通过: {result.validation_passed}")
    
    if result.success:
        print("\n提取结果:")
        for information_type, information_result in result.results.items():
            print(f"\n--- {information_type.upper()} ---")
            if "error" in information_result:
                print(f"错误: {information_result['error']}")
            else:
                content = information_result['extracted_content']
                print(f"内容: {content}")

def demo_batch_extraction():
    """演示批量静态信息提取"""
    print("\n" + "=" * 60)
    print("批量静态信息提取演示")
    print("=" * 60)
    
    texts = [
        "赵六，男，30岁，数据分析师，邮箱：zhaoliu@data.com，电话：187-3333-4444。",
        "钱七，女，27岁，UI设计师，公司：字节跳动，地址：北京市海淀区中关村。",
        "孙八，男，33岁，运维工程师，技术栈：Linux、Python、Shell，年薪：20万。"
    ]
    
    # 创建代理
    agent = create_static_information_agent("basic")
    
    # 批量提取
    results = agent.batch_extract(texts)
    
    print(f"批量处理 {len(texts)} 个文本")
    
    for i, result in enumerate(results):
        print(f"\n--- 文本 {i+1} ---")
        print(f"成功: {result.success}")
        print(f"质量评分: {result.quality_score:.2f}")
        print(f"验证通过: {result.validation_passed}")
        print(f"处理时间: {result.processing_time:.2f}秒")
        
        if result.success:
            for information_type, information_result in result.results.items():
                if "error" not in information_result:
                    content = information_result['extracted_content']
                    print(f"  {information_type}: {content[:100]}{'...' if len(content) > 100 else ''}")

def demo_langchain_tool():
    """演示LangChain工具包装器"""
    print("\n" + "=" * 60)
    print("LangChain工具包装器演示")
    print("=" * 60)
    
    test_text = """
    周九，女，29岁，前端工程师，毕业于华中科技大学。
    邮箱：zhoujiu@web.com，电话：188-5555-6666。
    公司：美团点评，地址：北京市朝阳区望京东路4号。
    入职时间：2019年3月1日，月薪：18K，技术栈：Vue、React、TypeScript。
    """
    
    # 创建静态信息提取代理
    agent = create_static_information_agent("basic")
    
    # 创建LangChain工具
    tool = StaticInformationTool(agent)
    
    # 使用工具进行提取
    result = tool._run(
        text=test_text,
        information_level="basic",
        information_types=["contact", "personal", "financial"]
    )
    
    print(f"输入文本: {test_text.strip()}")
    print(f"工具名称: {tool.name}")
    print(f"工具描述: {tool.description}")
    print(f"执行结果: {result['success']}")
    
    if result['success']:
        print(f"提取级别: {result['information_level']}")
        print(f"提取类型: {result['information_types']}")
        print(f"质量评分: {result['quality_score']:.2f}")
        print(f"验证通过: {result['validation_passed']}")
        print(f"处理时间: {result['processing_time']:.2f}秒")
        
        print("\n提取结果:")
        for information_type, information_result in result['results'].items():
            print(f"\n--- {information_type.upper()} ---")
            if "error" in information_result:
                print(f"错误: {information_result['error']}")
            else:
                content = information_result['extracted_content']
                print(f"内容: {content[:200]}{'...' if len(content) > 200 else ''}")

def demo_statistics():
    """演示统计信息"""
    print("\n" + "=" * 60)
    print("统计信息演示")
    print("=" * 60)
    
    # 创建代理
    agent = create_static_information_agent("basic")
    
    # 执行多次提取
    texts = [
        "吴十，男，31岁，后端工程师，邮箱：wushi@backend.com。",
        "郑十一，女，26岁，产品助理，公司：滴滴出行。",
        "王十二，男，34岁，技术总监，年薪：50万元。"
    ]
    
    for text in texts:
        agent.extract_information(text)
    
    # 获取统计信息
    stats = agent.get_statistics()
    
    print("提取统计信息:")
    print(f"总提取次数: {stats['total_extractions']}")
    print(f"成功提取次数: {stats['successful_extractions']}")
    print(f"成功率: {stats['success_rate']:.2%}")
    print(f"平均质量评分: {stats['average_quality']:.2f}")
    print(f"平均处理时间: {stats['average_processing_time']:.2f}秒")
    print(f"验证通过次数: {stats['validation_passed']}")
    print(f"验证通过率: {stats['validation_rate']:.2%}")
    
    print("\n级别统计:")
    for level, level_stats in stats['level_statistics'].items():
        print(f"  {level}: {level_stats['count']}次, 平均质量: {level_stats['avg_quality']:.2f}, 验证率: {level_stats['validation_rate']:.2%}")

def demo_advanced_configuration():
    """演示高级配置"""
    print("\n" + "=" * 60)
    print("高级配置演示")
    print("=" * 60)
    
    test_text = """
    刘十三，男，36岁，CTO，毕业于斯坦福大学计算机系。
    邮箱：liushisan@startup.com，电话：189-7777-8888。
    公司：某知名科技创业公司，地址：上海市浦东新区张江高科技园区。
    入职时间：2021年1月1日，年薪：80万元，股权：5%。
    技术栈：全栈开发、云原生架构、AI/ML、区块链。
    管理团队：50人研发团队，负责技术战略和产品架构。
    """
    
    # 创建自定义配置
    from lightce.agent.system import ModelConfig
    
    model_config = ModelConfig(
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=2000,
        provider="openai"
    )
    
    config = StaticInformationConfig(
        information_level=InformationLevel.ADVANCED,
        information_types=[InformationType.PERSONAL, InformationType.FINANCIAL, InformationType.TECHNICAL],
        model_config=model_config,
        enable_validation=True,
        quality_threshold=0.8,
        enable_format_check=True
    )
    
    # 创建代理
    agent = StaticInformationAgent(config)
    
    # 执行提取
    result = agent.extract_information(test_text)
    
    print(f"配置信息:")
    print(f"  提取级别: {config.information_level.value}")
    print(f"  提取类型: {[t.value for t in config.information_types]}")
    print(f"  模型配置: {config.model_config.dict()}")
    print(f"  质量阈值: {config.quality_threshold}")
    print(f"  启用验证: {config.enable_validation}")
    print(f"  启用格式检查: {config.enable_format_check}")
    
    print(f"\n提取结果:")
    print(f"成功: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"验证通过: {result.validation_passed}")
    print(f"处理时间: {result.processing_time:.2f}秒")
    
    if result.success:
        for information_type, information_result in result.results.items():
            print(f"\n--- {information_type.upper()} ---")
            if "error" not in information_result:
                content = information_result['extracted_content']
                print(f"内容: {content[:300]}{'...' if len(content) > 300 else ''}")

def demo_format_validation():
    """演示格式验证功能"""
    print("\n" + "=" * 60)
    print("格式验证功能演示")
    print("=" * 60)
    
    test_text = """
    陈十四，男，25岁，实习生，邮箱：chenshisi@intern.com，电话：190-9999-0000。
    公司：某互联网公司，地址：广州市天河区珠江新城。
    实习时间：2023年7月1日-2023年9月30日，实习工资：3000元/月。
    技术栈：JavaScript、HTML、CSS、Vue.js。
    """
    
    # 创建代理
    agent = create_static_information_agent("basic")
    
    # 执行提取
    result = agent.extract_information(test_text)
    
    print(f"输入文本: {test_text.strip()}")
    print(f"成功: {result.success}")
    print(f"质量评分: {result.quality_score:.2f}")
    print(f"验证通过: {result.validation_passed}")
    
    if result.success:
        print("\n格式验证结果:")
        for information_type, information_result in result.results.items():
            print(f"\n--- {information_type.upper()} ---")
            if "error" not in information_result:
                content = information_result['extracted_content']
                raw_content = information_result.get('raw_content', '')
                
                print(f"原始内容: {raw_content[:150]}...")
                print(f"格式化后: {content[:150]}...")
                
                # 检查格式改进
                if len(content) > len(raw_content):
                    print("✓ 格式检查已改进内容结构")
                else:
                    print("✓ 内容格式已符合要求")

def main():
    """主演示函数"""
    print("静态信息提取工具演示")
    print("=" * 60)
    
    while True:
        print("\n请选择演示功能:")
        print("1. 基础级别静态信息提取")
        print("2. 中级级别静态信息提取")
        print("3. 特定类型提取")
        print("4. 批量提取")
        print("5. LangChain工具包装器")
        print("6. 统计信息")
        print("7. 高级配置")
        print("8. 格式验证功能")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-8): ").strip()
        
        if choice == "0":
            print("感谢使用静态信息提取工具演示！")
            break
        elif choice == "1":
            demo_basic_extraction()
        elif choice == "2":
            demo_intermediate_extraction()
        elif choice == "3":
            demo_specific_information_types()
        elif choice == "4":
            demo_batch_extraction()
        elif choice == "5":
            demo_langchain_tool()
        elif choice == "6":
            demo_statistics()
        elif choice == "7":
            demo_advanced_configuration()
        elif choice == "8":
            demo_format_validation()
        else:
            print("无效的选择，请重新输入")

if __name__ == "__main__":
    main() 