import sys
import pkgutil
import langchain
import langchain.agents
import langgraph
import langgraph.prebuilt

print(f"LangChain version: {langchain.__version__}")
# print(f"LangGraph version: {langgraph.__version__}")

print("\nChecking langchain.agents for 'create_tool_calling_agent'...")
if hasattr(langchain.agents, 'create_tool_calling_agent'):
    print("Found create_tool_calling_agent in langchain.agents")
else:
    print("NOT FOUND create_tool_calling_agent in langchain.agents")

print("\nChecking langchain.agents for 'AgentExecutor'...")
if hasattr(langchain.agents, 'AgentExecutor'):
    print("Found AgentExecutor in langchain.agents")
else:
    print("NOT FOUND AgentExecutor in langchain.agents")

print("\nChecking langgraph.prebuilt for 'create_react_agent'...")
if hasattr(langgraph.prebuilt, 'create_react_agent'):
    print("Found create_react_agent in langgraph.prebuilt")
else:
    print("NOT FOUND create_react_agent in langgraph.prebuilt")

print("\nSearching for AgentExecutor in langchain package...")
# Simple recursive search (limited depth)
def search_module(module, name, depth=0):
    if depth > 2: return
    if hasattr(module, name):
        print(f"Found {name} in {module.__name__}")
        return
    
    if hasattr(module, "__path__"):
        for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
            try:
                submod = importer.find_module(modname).load_module(modname)
                if hasattr(submod, name):
                    print(f"Found {name} in {module.__name__}.{modname}")
            except:
                pass

search_module(langchain, "AgentExecutor")

