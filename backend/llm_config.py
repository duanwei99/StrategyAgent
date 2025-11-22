"""
LLM 模型配置管理模块
支持 OpenAI、Claude 和豆包（火山引擎）等多种模型提供商的统一配置和切换
"""
import os
from typing import Literal, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 模型类型定义
ModelType = Literal["code_generator", "tool_caller", "optimizer"]
ProviderType = Literal["openai", "claude", "doubao"]


class LLMConfig:
    """LLM 模型配置类，统一管理不同用途的模型"""
    
    def __init__(self):
        # 从环境变量读取配置
        self.provider: ProviderType = os.getenv("LLM_PROVIDER", "doubao")
        
        # OpenAI 配置
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.openai_code_model = os.getenv("OPENAI_CODE_MODEL", "gpt-4-turbo")
        self.openai_tool_model = os.getenv("OPENAI_TOOL_MODEL", "gpt-4-turbo")
        self.openai_optimizer_model = os.getenv("OPENAI_OPTIMIZER_MODEL", "gpt-4-turbo")
        
        # Claude 配置
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", "")
        self.claude_code_model = os.getenv("CLAUDE_CODE_MODEL", "claude-3-5-sonnet-20241022")
        self.claude_tool_model = os.getenv("CLAUDE_TOOL_MODEL", "claude-3-5-sonnet-20241022")
        self.claude_optimizer_model = os.getenv("CLAUDE_OPTIMIZER_MODEL", "claude-3-5-sonnet-20241022")
        
        # 豆包（火山引擎）配置
        self.doubao_api_key = os.getenv("DOUBAO_API_KEY", "")
        self.doubao_base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        self.doubao_code_model = os.getenv("DOUBAO_CODE_MODEL", "doubao-seed-code")
        self.doubao_tool_model = os.getenv("DOUBAO_TOOL_MODEL", "kimi-k2")
        self.doubao_optimizer_model = os.getenv("DOUBAO_OPTIMIZER_MODEL", "doubao-seed-1.6-thinking")
        
        # 温度参数配置
        self.code_temperature = float(os.getenv("CODE_TEMPERATURE", "0.2"))
        self.tool_temperature = float(os.getenv("TOOL_TEMPERATURE", "0.1"))
        self.optimizer_temperature = float(os.getenv("OPTIMIZER_TEMPERATURE", "0.3"))
    
    def get_llm(self, model_type: ModelType):
        """
        根据模型类型和配置的提供商返回对应的 LLM 实例
        
        Args:
            model_type: 模型类型 ("code_generator", "tool_caller", "optimizer")
            
        Returns:
            相应的 LLM 实例
        """
        if self.provider == "openai":
            return self._get_openai_llm(model_type)
        elif self.provider == "claude":
            return self._get_claude_llm(model_type)
        elif self.provider == "doubao":
            return self._get_doubao_llm(model_type)
        else:
            raise ValueError(f"不支持的 LLM 提供商: {self.provider}")
    
    def _get_openai_llm(self, model_type: ModelType):
        """获取 OpenAI 模型实例"""
        model_map = {
            "code_generator": self.openai_code_model,
            "tool_caller": self.openai_tool_model,
            "optimizer": self.openai_optimizer_model
        }
        
        temperature_map = {
            "code_generator": self.code_temperature,
            "tool_caller": self.tool_temperature,
            "optimizer": self.optimizer_temperature
        }
        
        return ChatOpenAI(
            model=model_map[model_type],
            temperature=temperature_map[model_type],
            api_key=self.openai_api_key,
            base_url=self.openai_base_url
        )
    
    def _get_claude_llm(self, model_type: ModelType):
        """获取 Claude 模型实例"""
        model_map = {
            "code_generator": self.claude_code_model,
            "tool_caller": self.claude_tool_model,
            "optimizer": self.claude_optimizer_model
        }
        
        temperature_map = {
            "code_generator": self.code_temperature,
            "tool_caller": self.tool_temperature,
            "optimizer": self.optimizer_temperature
        }
        
        return ChatAnthropic(
            model=model_map[model_type],
            temperature=temperature_map[model_type],
            api_key=self.claude_api_key
        )
    
    def _get_doubao_llm(self, model_type: ModelType):
        """
        获取豆包（火山引擎）模型实例
        豆包的 API 兼容 OpenAI 格式，使用 ChatOpenAI 并指定 base_url
        """
        model_map = {
            "code_generator": self.doubao_code_model,
            "tool_caller": self.doubao_tool_model,
            "optimizer": self.doubao_optimizer_model
        }
        
        temperature_map = {
            "code_generator": self.code_temperature,
            "tool_caller": self.tool_temperature,
            "optimizer": self.optimizer_temperature
        }
        
        return ChatOpenAI(
            model=model_map[model_type],
            temperature=temperature_map[model_type],
            api_key=self.doubao_api_key,
            base_url=self.doubao_base_url
        )
    
    def get_code_generator_llm(self):
        """获取代码生成模型（写策略代码）"""
        return self.get_llm("code_generator")
    
    def get_tool_caller_llm(self):
        """获取工具调用模型（Agent 决策）"""
        return self.get_llm("tool_caller")
    
    def get_optimizer_llm(self):
        """获取策略优化模型"""
        return self.get_llm("optimizer")
    
    def print_config(self):
        """打印当前配置信息（用于调试）"""
        print(f"当前 LLM 提供商: {self.provider}")
        if self.provider == "openai":
            print(f"  代码生成模型: {self.openai_code_model}")
            print(f"  工具调用模型: {self.openai_tool_model}")
            print(f"  策略优化模型: {self.openai_optimizer_model}")
        elif self.provider == "claude":
            print(f"  代码生成模型: {self.claude_code_model}")
            print(f"  工具调用模型: {self.claude_tool_model}")
            print(f"  策略优化模型: {self.claude_optimizer_model}")
        elif self.provider == "doubao":
            print(f"  代码生成模型: {self.doubao_code_model}")
            print(f"  工具调用模型: {self.doubao_tool_model}")
            print(f"  策略优化模型: {self.doubao_optimizer_model}")


# 创建全局配置实例
llm_config = LLMConfig()

