---
name: radar-agents-agent-orchestrator
description: 使 Claude 能够基于 RadarAgents 框架生成智能体编排代码，遵循框架的"一切皆为 Tools"设计理念和 API 规范，适用于多智能体系统的快速开发。此外，也可以基于原有框架继续改进其内部设计逻辑，完善架构设计。
---

RadarAgents 智能体编排技能

## Instructions

请严格遵循以下规范：

1. 业务场景智能体类型选择：
   - 简单任务使用 SimpleAgent
   - 需要工具调用使用 ReActAgent
   - 需要迭代优化使用 ReflectionAgent
   - 复杂任务分解使用 PlanAndSolveAgent
   - 自定义智能体时，严格遵守相关规范和格式，包括工具注册和代码结构规范

2. 工具注册规范：
   - 所有功能都应通过 ToolRegistry 注册为工具
   - 优先使用内置工具（SearchTool, CalculatorTool）
   - 自定义工具需使用 register_function 或 register_tool

3. 代码结构规范：
   - 使用 PEP 8 命名规范（变量使用 snake_case，类使用 CamelCase）
   - 为所有函数和类添加 docstring
   - 通过 .env 文件管理配置（LLM_MODEL_ID, LLM_API_KEY 等）
   - 避免硬编码值，使用环境变量或配置文件

4. 智能体交互原则：
   - 每个智能体应有明确的 name 和 system_prompt
   - 使用 run() 和 stream_run() 两种方式处理任务
   - 对于需要工具调用的任务，必须使用 tool_registry

5. 向后兼容性：
   - 任何框架改进必须保持现有 API 兼容（不修改已有类/方法签名）
   - 新增功能通过 @deprecated 标记旧方法，提供迁移指南
   - 禁止删除任何现有文件或测试用例
   
6. 模块化设计：
   - 新功能必须封装为独立模块（如 agent_extensions/ 目录）
   - 避免在核心文件（agent.py, orchestrator.py）中添加新逻辑
   - 使用 __init__.py 显式导出模块

## Reference
   - https://github.com/jjyaoao/helloagents
   - https://datawhalechina.github.io/hello-agents/#/
   - https://datawhalechina.github.io/hello-agents/#/./chapter7/%E7%AC%AC%E4%B8%83%E7%AB%A0%20%E6%9E%84%E5%BB%BA%E4%BD%A0%E7%9A%84Agent%E6%A1%86%E6%9E%B6
   - https://datawhalechina.github.io/hello-agents/#/./chapter8/%E7%AC%AC%E5%85%AB%E7%AB%A0%20%E8%AE%B0%E5%BF%86%E4%B8%8E%E6%A3%80%E7%B4%A2
   - https://datawhalechina.github.io/hello-agents/#/./chapter9/%E7%AC%AC%E4%B9%9D%E7%AB%A0%20%E4%B8%8A%E4%B8%8B%E6%96%87%E5%B7%A5%E7%A8%8B
   - https://datawhalechina.github.io/hello-agents/#/./chapter10/%E7%AC%AC%E5%8D%81%E7%AB%A0%20%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%9A%E4%BF%A1%E5%8D%8F%E8%AE%AE
   - https://datawhalechina.github.io/hello-agents/#/./chapter12/%E7%AC%AC%E5%8D%81%E4%BA%8C%E7%AB%A0%20%E6%99%BA%E8%83%BD%E4%BD%93%E6%80%A7%E8%83%BD%E8%AF%84%E4%BC%B0

## Examples

### Example1

from hello_agents import SimpleAgent, HelloAgentsLLM

初始化 LLM（框架会自动检测 provider）
llm = HelloAgentsLLM()

创建基础智能体
researcher = SimpleAgent(
    name="研究助手",
    llm=llm,
    system_prompt="你是一个专注于科技新闻研究的AI助手"
)

执行任务
response = researcher.run("请介绍最新的大模型发展趋势")
print(response)

### Example2:使用 ReActAgent 和工具

from radar_agents import ReActAgent, ToolRegistry, SearchTool
from radar_agents import HelloAgentsLLM

llm = RadarAgentsLLM()
tool_registry = ToolRegistry()

tool_registry.register_tool(SearchTool())

research_agent = ReActAgent(
    name="研究专家",
    llm=llm,
    tool_registry=tool_registry,
    max_steps=5
)

result = research_agent.run(
    "搜索最新的GPT-4.5发展情况，并计算其参数量相比GPT-4的增长百分比"
)
print(result)

### Example3:多智能体协同工作

from radar_agents import ReActAgent, PlanAndSolveAgent, ToolRegistry
from radar_agents import HelloAgentsLLM

llm = RadarAgentsLLM()

tool_registry = ToolRegistry()
tool_registry.register_tool(SearchTool())

planner = PlanAndSolveAgent(
    name="规划专家",
    llm=llm
)

researcher = ReActAgent(
    name="研究助手",
    llm=llm,
    tool_registry=tool_registry
)

def multi_agent_workflow():
    # 1. 规划任务
    plan = planner.run(
        "请规划一个关于AI模型发展的研究项目，包括研究方向、需要的数据和预期成果"
    )
    
    # 2. 执行研究
    research_result = researcher.run(
        f"基于规划: {plan}，进行详细研究并收集最新数据"
    )
    
    # 3. 生成报告
    report = planner.run(
        f"基于研究结果: {research_result}，撰写一份完整的研究报告"
    )
    
    return report

report = multi_agent_workflow()
print("最终研究报告:", report)

### Example4：流式响应与错误处理

from radar_agents import SimpleAgent, HelloAgentsLLM
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_system")

llm = RadarAgentsLLM()

support_agent = SimpleAgent(
    name="技术支持",
    llm=llm,
    system_prompt="你是一个专业的AI技术支持助手，能解决用户的技术问题"
)

try:
    # 流式响应
    print("支持助手: ", end="", flush=True)
    for chunk in support_agent.stream_run("如何解决HelloAgents框架中的API密钥错误？"):
        print(chunk, end="", flush=True)
    print()
    
except Exception as e:
    logger.error(f"智能体处理失败: {str(e)}")
    raise ValueError("智能体处理过程中发生错误") from e