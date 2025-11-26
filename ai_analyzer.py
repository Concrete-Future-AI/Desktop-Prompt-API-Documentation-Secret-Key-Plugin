#!/usr/bin/env python3
"""
AI Prompt 分析器 - 豆包版本
使用豆包 (Doubao) API 自动分析 Prompt 并生成名称、分类、标签
"""
import os
import requests
import json
import re


class AIAnalyzerDoubao:
    """AI 分析器（豆包版本）"""
    
    def __init__(self, api_key=None, use_key_pool=False):
        """
        初始化豆包API分析器
        api_key: 可以通过参数传入，或通过环境变量 DOUBAO_API_KEY 设置
        """
        # 豆包API配置
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        # 优先使用传入的 api_key，其次使用环境变量
        self.api_key = api_key or os.environ.get("DOUBAO_API_KEY", "")
        self.model = "doubao-seed-1-6-thinking-250715"
        
        if not self.api_key:
            print("⚠️ 警告: 未设置豆包 API 密钥")
            print("   请设置环境变量 DOUBAO_API_KEY 或在初始化时传入 api_key 参数")
        else:
            print(f"✓ 豆包 API 初始化完成")
            print(f"   模型: {self.model}")
    
    def analyze_prompt(self, prompt_content, max_retries=3):
        """
        分析 Prompt 内容
        返回: {"name": "名称", "category": "分类", "tags": ["标签1", "标签2"]}
        """
        if not self.api_key:
            print("✗ API 密钥未设置，无法进行分析")
            return None
            
        print(f"\n{'='*60}")
        print(f"🤖 开始 AI 分析（豆包）")
        print(f"   Prompt 长度: {len(prompt_content)} 字符")
        print(f"   最大重试: {max_retries} 次")
        print(f"{'='*60}\n")
        
        # 构建分析请求
        analysis_prompt = f"""请分析以下 Prompt 内容，并返回 JSON 格式的结果。

要求：
1. name: 简短的名称（5-15个字）
2. category: 单个分类（如：编程、写作、分析、产品、教育等）
3. tags: 3-5个关键标签（用于快速识别）

请直接返回 JSON，不要有其他说明文字。格式如下：
{{
  "name": "具体名称",
  "category": "分类",
  "tags": ["标签1", "标签2", "标签3"]
}}

Prompt 内容：
{prompt_content}
"""
        
        # 重试逻辑
        for attempt in range(max_retries):
            try:
                print(f"→ 尝试 {attempt + 1}/{max_retries}")
                
                # 构建请求
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": analysis_prompt
                        }
                    ]
                }
                
                # 发送请求
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 提取生成的文本
                    if 'choices' in result and len(result['choices']) > 0:
                        message = result['choices'][0].get('message', {})
                        text = message.get('content', '')
                        
                        if not text:
                            print(f"✗ 响应内容为空")
                            if attempt < max_retries - 1:
                                print(f"   继续重试...")
                                continue
                            else:
                                return None
                        
                        # 清理文本（移除代码块标记）
                        text = text.strip()
                        # 移除 ```json 或 ``` 开头
                        if text.startswith('```json'):
                            text = text[7:].strip()
                        elif text.startswith('```'):
                            text = text[3:].strip()
                        # 移除 ``` 结尾
                        if text.endswith('```'):
                            text = text[:-3].strip()
                        
                        # 解析 JSON
                        try:
                            data = json.loads(text)
                        except json.JSONDecodeError as je:
                            print(f"✗ JSON解析失败")
                            print(f"   原始文本: {text[:200]}")
                            print(f"   错误: {je}")
                            if attempt < max_retries - 1:
                                print(f"   继续重试...")
                                continue
                            else:
                                return None
                        
                        # 验证数据
                        if 'name' in data and 'category' in data and 'tags' in data:
                            if isinstance(data['tags'], list):
                                result_data = {
                                    'name': data['name'][:50],
                                    'category': data['category'][:30],
                                    'tags': [tag[:20] for tag in data['tags'][:5]]
                                }
                                print(f"✓ 分析成功！")
                                print(f"   名称: {result_data['name']}")
                                print(f"   分类: {result_data['category']}")
                                print(f"   标签: {', '.join(result_data['tags'])}")
                                return result_data
                        
                        # 数据验证失败
                        print("✗ 响应格式错误（数据验证失败或字段缺失）")
                        print(f"   响应内容: {str(data)[:300]}")
                        if attempt < max_retries - 1:
                            print(f"   继续重试...")
                            continue
                        else:
                            return None
                    
                    # 响应格式不符合预期
                    print("✗ 响应格式错误")
                    print(f"   响应内容: {str(result)[:300]}")
                    if attempt < max_retries - 1:
                        print(f"   继续重试...")
                        continue
                    else:
                        return None
                
                else:
                    # API错误
                    print(f"✗ API 错误 ({response.status_code})")
                    try:
                        error_data = response.json()
                        print(f"   错误详情: {error_data}")
                    except:
                        print(f"   响应文本: {response.text[:200]}")
                    
                    if attempt < max_retries - 1:
                        print(f"   继续重试...")
                        continue
                    else:
                        return None
            
            except requests.exceptions.Timeout:
                print(f"✗ 请求超时（尝试 {attempt + 1}/{max_retries}）")
                if attempt < max_retries - 1:
                    print(f"   继续重试...")
                    continue
                else:
                    return None
            
            except requests.exceptions.ConnectionError as e:
                print(f"✗ 连接错误（尝试 {attempt + 1}/{max_retries}）")
                print(f"   错误: {str(e)[:200]}")
                if attempt < max_retries - 1:
                    print(f"   继续重试...")
                    continue
                else:
                    return None
            
            except Exception as e:
                print(f"✗ 未知错误: {e}")
                import traceback
                traceback.print_exc()
                
                if attempt < max_retries - 1:
                    print(f"   继续重试...")
                    continue
                else:
                    return None
        
        print(f"\n✗ 所有重试失败，分析终止")
        return None
    
    def test_connection(self):
        """测试 API 连接"""
        if not self.api_key:
            return False, "✗ API 密钥未设置"
            
        try:
            print(f"测试豆包 API 连接...")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return True, "✓ 连接成功"
            else:
                return False, f"✗ API 错误: {response.status_code}"
        
        except requests.exceptions.Timeout:
            return False, "✗ 连接超时"
        
        except requests.exceptions.ConnectionError:
            return False, "✗ 连接错误"
        
        except Exception as e:
            return False, f"✗ 错误: {e}"


# 保持向后兼容
AIAnalyzer = AIAnalyzerDoubao
