#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词压缩演示
展示压缩前后的提示词对比
"""

from lightce.prompt.mini_contents import (
    CompressionType, 
    get_compression_prompt,
    CompressionStage
)

def demo_prompt_compression():
    """演示提示词压缩效果"""
    print("=== 提示词压缩演示 ===\n")
    
    # 测试内容
    test_content = "这是一个测试内容"
    
    # 展示每种类型的提示词长度对比
    stages = [
        CompressionStage.PREPROCESS,
        CompressionStage.COMPRESS,
        CompressionStage.OPTIMIZE,
        CompressionStage.POSTPROCESS
    ]
    
    print("各类型提示词长度统计：")
    print("-" * 60)
    
    for compression_type in CompressionType:
        print(f"\n{compression_type.value.upper()}类型:")
        total_length = 0
        
        for stage in stages:
            prompt = get_compression_prompt(
                stage,
                compression_type,
                text=test_content,
                preprocess_result="预处理结果示例",
                compression_ratio=50.0,
                original_length=100,
                compressed_length=50,
                actual_ratio=50.0,
                final_length=50,
                final_ratio=50.0,
                information_retention=85.0,
                original_text=test_content,
                optimized_text=test_content,
                final_text=test_content,
                compressed_text=test_content
            )
            
            stage_name = {
                CompressionStage.PREPROCESS: "预处理",
                CompressionStage.COMPRESS: "压缩",
                CompressionStage.OPTIMIZE: "优化",
                CompressionStage.POSTPROCESS: "后处理"
            }[stage]
            
            print(f"  {stage_name}: {len(prompt)} 字符")
            total_length += len(prompt)
        
        print(f"  总计: {total_length} 字符")
    
    print("\n" + "=" * 60)
    
    # 展示压缩后的提示词示例
    print("\n压缩后的提示词示例（TEXT类型预处理）：")
    print("-" * 60)
    
    prompt = get_compression_prompt(
        CompressionStage.PREPROCESS,
        CompressionType.TEXT,
        text=test_content
    )
    
    print(prompt)
    
    print("\n" + "=" * 60)
    
    # 展示压缩效果
    print("\n压缩效果总结：")
    print("1. 移除了不必要的空行")
    print("2. 压缩了字符串开头的换行")
    print("3. 压缩了字符串结尾的换行")
    print("4. 保持了提示词的结构和可读性")
    print("5. 减少了文件大小，提高了加载效率")

if __name__ == "__main__":
    demo_prompt_compression()
    print("\n=== 演示完成 ===") 