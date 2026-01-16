---
name: mcp-tool-pattern
description: Standard pattern for creating MCP tools that AI agents can call. Use when implementing task management tools (add, list, complete, delete, update).
---

# MCP Tool Pattern

## Instructions

Create MCP tools with these features:

1. **Tool Structure**
   - Use `@mcp_server.tool()` decorator
   - Accept `user_id` as first parameter (for data isolation)
   - Return standardized dict: `{"status": "success|error", "data": {}, "message": ""}`

2. **Error Handling**
   - Wrap in try-except blocks
   - Return error status with clear message
   - Never raise exceptions to agent

3. **Database Integration**
   - Reuse Phase 2 database models (Task, User)
   - Use existing SQLModel queries
   - Keep tools stateless (no global state)

4. **Validation**
   - Check user_id is provided
   - Validate required parameters
   - Return error if validation fails

## Example Tool
```python
from mcp.server import MCPServer

mcp_server = MCPServer("todo-tools")

@mcp_server.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task for the user."""
    try:
        if not user_id or not title:
            return {"status": "error", "message": "user_id and title required"}
        
        # Use Phase 2 database code
        task = create_task_in_db(user_id, title, description)
        
        return {
            "status": "success",
            "data": {"task_id": task.id, "title": task.title},
            "message": f"Task '{task.title}' created"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Response Format

Success:
```python
{"status": "success", "data": {...}, "message": "Task created"}
```

Error:
```python
{"status": "error", "message": "Task not found"}
```

## Required Tools
1. add_task - Create task
2. list_tasks - Get tasks (filter by status)
3. complete_task - Mark complete
4. delete_task - Remove task
5. update_task - Modify task
```

---
