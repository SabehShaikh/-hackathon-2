"""
GROQ AI Agent for Task Management using OpenAI Agents SDK.

This module integrates with GROQ API via LiteLLM to provide
natural language understanding for task management operations.

Features:
- Retry logic with exponential backoff for reliability
- Multi-task operation support (sequential tool calls)
- Off-topic guardrails (task management focus)
- Flexible natural language understanding
- Comprehensive error handling with specific messages
"""

import os
import asyncio
import logging
from typing import List, Tuple, Optional
from sqlmodel import Session

from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

from database import settings
from models import Message, ToolCallResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set LiteLLM API key for GROQ
os.environ["GROQ_API_KEY"] = settings.groq_api_key

# Retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0  # seconds
MAX_BACKOFF = 10.0  # seconds

# Enhanced system instructions with guardrails, multi-task support, and NLP flexibility
SYSTEM_INSTRUCTIONS = """You are a focused task management assistant. Your ONLY purpose is to help users manage their tasks.

## CRITICAL BOUNDARIES
You ONLY help with task management. For ANY off-topic requests (weather, jokes, general questions, coding help, etc.), respond:
"I'm a task management assistant. I can help you add, list, complete, update, or delete tasks. What would you like to do with your tasks?"

## YOUR TOOLS
- add_task: Create a new task (requires title, optional description)
- list_tasks: Show tasks (filter: "all", "pending", or "completed")
- complete_task: Mark a task as done (requires task_id)
- delete_task: Remove a task (requires task_id)
- update_task: Change task title or description (requires task_id)

## MULTI-TASK OPERATIONS
Users may request MULTIPLE operations in one message. You MUST:
1. Identify ALL operations requested
2. Execute each tool call in sequence
3. Report results for EACH operation

Examples of multi-task requests:
- "add task X and add task Y" -> Call add_task twice
- "complete task 1 and task 2" -> Call complete_task twice
- "add buy milk, then show my tasks" -> Call add_task, then list_tasks
- "delete task 3 and 4" -> Call delete_task twice

## NATURAL LANGUAGE UNDERSTANDING
Recognize these intent patterns:

ADD TASK (create new tasks):
- "add [task]" / "add task [task]"
- "create [task]" / "create a task to [task]"
- "new task [task]"
- "remind me to [task]" / "remember to [task]"
- "I need to [task]" / "I have to [task]"
- "don't let me forget to [task]"
- "put [task] on my list"

LIST TASKS (show tasks):
- "show my tasks" / "show tasks" / "list tasks"
- "what are my tasks?" / "what do I need to do?"
- "what's on my list?" / "my todo list"
- "show pending/completed tasks"
- "what haven't I done yet?"

COMPLETE TASK (mark done):
- "complete task [id]" / "done with task [id]"
- "mark task [id] as done/complete/finished"
- "finished task [id]" / "task [id] is done"
- "mark first/last/second task as done"
- "complete the [task name] task"
- "I did [task name]" / "I finished [task name]"

DELETE TASK (remove):
- "delete task [id]" / "remove task [id]"
- "cancel task [id]" / "get rid of task [id]"
- "delete the first/last task"
- "remove the [task name] task"
- "I don't need [task name] anymore"

UPDATE TASK (modify):
- "update task [id] to [new title]"
- "change task [id] to [new title]"
- "rename task [id] to [new title]"
- "edit task [id]"

## TASK REFERENCES
Users may reference tasks by:
1. ID number: "task 3", "task #3", "#3"
2. Position: "first task", "last task", "second task", "third task"
3. Name: "the groceries task", "buy milk task"

When referencing by position or name, first call list_tasks to find the correct ID, then perform the operation.

## RESPONSE STYLE
- Use checkmark emoji (check) for successful operations
- Use wastebasket emoji for deletions
- Be concise but friendly
- If a task is not found, suggest: "Use 'show my tasks' to see available task IDs"
- Confirm each action completed in multi-task operations
- If intent is truly unclear (not off-topic), ask ONE clarifying question

## EXAMPLES
User: "add buy groceries and pick up dry cleaning"
-> Call add_task(title="Buy groceries"), then add_task(title="Pick up dry cleaning")
-> "Done! I've added both tasks: 'Buy groceries' and 'Pick up dry cleaning'"

User: "what's the weather?"
-> "I'm a task management assistant. I can help you add, list, complete, update, or delete tasks. What would you like to do with your tasks?"

User: "mark the first task as done"
-> First call list_tasks, identify task with lowest ID, then call complete_task
-> "Done! Marked '[task name]' as completed"

User: "remind me to call mom tomorrow"
-> Call add_task(title="Call mom tomorrow")
-> "Done! Added task: 'Call mom tomorrow'"
"""

# Global context for current request (set per-request)
_current_user_id: str = ""
_current_session: Session = None


def set_request_context(user_id: str, session: Session):
    """Set the current request context for tool execution."""
    global _current_user_id, _current_session
    _current_user_id = user_id
    _current_session = session


# ============================================================================
# MCP Tools as function_tools for Agents SDK
# ============================================================================

@function_tool
def add_task(title: str, description: str = "") -> dict:
    """
    Create a new task for the user.

    Args:
        title: The title of the task (required, cannot be empty)
        description: Optional description for the task

    Returns:
        dict with status, data (task_id, title), and message
    """
    from models import Task
    from datetime import datetime

    try:
        if not _current_user_id:
            return {"status": "error", "data": {}, "message": "Not authenticated"}

        if not title or not title.strip():
            return {"status": "error", "data": {}, "message": "Please provide a task name"}

        new_task = Task(
            user_id=_current_user_id,
            title=title.strip(),
            description=description.strip() if description else None
        )

        _current_session.add(new_task)
        _current_session.commit()
        _current_session.refresh(new_task)

        logger.info(f"Task created: {new_task.id} - {new_task.title}")

        return {
            "status": "success",
            "data": {"task_id": new_task.id, "title": new_task.title},
            "message": f"Task '{new_task.title}' created successfully"
        }
    except Exception as e:
        logger.error(f"add_task error: {e}")
        return {"status": "error", "data": {}, "message": f"Failed to create task: {str(e)}"}


@function_tool
def list_tasks(status: str = "all") -> dict:
    """
    List tasks for the user.

    Args:
        status: Filter by status - "all", "pending", or "completed"

    Returns:
        dict with status, data (list of tasks), and message
    """
    from models import Task
    from sqlmodel import select

    try:
        if not _current_user_id:
            return {"status": "error", "data": [], "message": "Not authenticated"}

        statement = select(Task).where(Task.user_id == _current_user_id)

        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)

        statement = statement.order_by(Task.created_at.asc())  # Oldest first for consistent ordering
        tasks = _current_session.exec(statement).all()

        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "position": idx + 1  # 1-indexed position
            }
            for idx, task in enumerate(tasks)
        ]

        status_text = status if status != "all" else "total"
        return {
            "status": "success",
            "data": task_list,
            "message": f"Found {len(task_list)} {status_text} task(s)"
        }
    except Exception as e:
        logger.error(f"list_tasks error: {e}")
        return {"status": "error", "data": [], "message": f"Failed to list tasks: {str(e)}"}


@function_tool
def complete_task(task_id: int) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: The ID of the task to complete

    Returns:
        dict with status, data, and message
    """
    from models import Task
    from datetime import datetime

    try:
        if not _current_user_id:
            return {"status": "error", "data": {}, "message": "Not authenticated"}

        task = _current_session.get(Task, task_id)

        if not task or task.user_id != _current_user_id:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found. Use 'show my tasks' to see available task IDs."
            }

        if task.completed:
            return {
                "status": "success",
                "data": {"task_id": task.id, "title": task.title},
                "message": f"Task '{task.title}' is already completed"
            }

        task.completed = True
        task.updated_at = datetime.utcnow()
        _current_session.add(task)
        _current_session.commit()

        logger.info(f"Task completed: {task.id} - {task.title}")

        return {
            "status": "success",
            "data": {"task_id": task.id, "title": task.title},
            "message": f"Task '{task.title}' marked as completed"
        }
    except Exception as e:
        logger.error(f"complete_task error: {e}")
        return {"status": "error", "data": {}, "message": f"Failed to complete task: {str(e)}"}


@function_tool
def delete_task(task_id: int) -> dict:
    """
    Delete a task.

    Args:
        task_id: The ID of the task to delete

    Returns:
        dict with status, data, and message
    """
    from models import Task

    try:
        if not _current_user_id:
            return {"status": "error", "data": {}, "message": "Not authenticated"}

        task = _current_session.get(Task, task_id)

        if not task or task.user_id != _current_user_id:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found. Use 'show my tasks' to see available task IDs."
            }

        title = task.title
        _current_session.delete(task)
        _current_session.commit()

        logger.info(f"Task deleted: {task_id} - {title}")

        return {
            "status": "success",
            "data": {"task_id": task_id, "title": title},
            "message": f"Task '{title}' deleted successfully"
        }
    except Exception as e:
        logger.error(f"delete_task error: {e}")
        return {"status": "error", "data": {}, "message": f"Failed to delete task: {str(e)}"}


@function_tool
def update_task(task_id: int, title: str = None, description: str = None) -> dict:
    """
    Update a task's title or description.

    Args:
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        dict with status, data, and message
    """
    from models import Task
    from datetime import datetime

    try:
        if not _current_user_id:
            return {"status": "error", "data": {}, "message": "Not authenticated"}

        task = _current_session.get(Task, task_id)

        if not task or task.user_id != _current_user_id:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found. Use 'show my tasks' to see available task IDs."
            }

        if title is not None:
            if not title.strip():
                return {"status": "error", "data": {}, "message": "Task title cannot be empty"}
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None

        task.updated_at = datetime.utcnow()
        _current_session.add(task)
        _current_session.commit()
        _current_session.refresh(task)

        logger.info(f"Task updated: {task.id} - {task.title}")

        return {
            "status": "success",
            "data": {"task_id": task.id, "title": task.title},
            "message": f"Task updated successfully"
        }
    except Exception as e:
        logger.error(f"update_task error: {e}")
        return {"status": "error", "data": {}, "message": f"Failed to update task: {str(e)}"}


# ============================================================================
# Agent Configuration with Retry Logic
# ============================================================================

def create_agent() -> Optional[Agent]:
    """Create the task management agent."""
    if not settings.groq_api_key:
        return None

    model = LitellmModel(
        model="groq/llama-3.3-70b-versatile",
        api_key=settings.groq_api_key
    )

    agent = Agent(
        name="TaskAssistant",
        instructions=SYSTEM_INSTRUCTIONS,
        model=model,
        tools=[add_task, list_tasks, complete_task, delete_task, update_task]
    )

    return agent


# Initialize agent at module load
_agent = None
try:
    _agent = create_agent()
    if _agent:
        logger.info("GROQ Agent initialized with Agents SDK")
    else:
        logger.warning("GROQ_API_KEY not set - AI features disabled")
except Exception as e:
    logger.error(f"Could not initialize agent: {e}")


async def run_agent_with_retry(
    agent: Agent,
    input_messages: List[dict],
    max_retries: int = MAX_RETRIES
) -> Tuple[str, List[ToolCallResult], Optional[str]]:
    """
    Run agent with exponential backoff retry logic.

    Args:
        agent: The Agent instance
        input_messages: List of conversation messages
        max_retries: Maximum number of retry attempts

    Returns:
        Tuple of (response_text, tool_calls, error_message)
    """
    last_error = None
    backoff = INITIAL_BACKOFF

    for attempt in range(max_retries):
        try:
            result = await Runner.run(agent, input=input_messages)

            # Extract response
            response_text = result.final_output or ""

            # Track tool calls
            tool_calls_made = []
            if hasattr(result, 'new_items'):
                for item in result.new_items:
                    if hasattr(item, 'raw_item') and hasattr(item.raw_item, 'type'):
                        if item.raw_item.type == 'function_call':
                            tool_name = getattr(item.raw_item, 'name', 'unknown')
                            tool_calls_made.append(ToolCallResult(
                                tool=tool_name,
                                parameters={},
                                result={"status": "executed"}
                            ))

            logger.info(f"Agent completed successfully on attempt {attempt + 1}")
            return response_text, tool_calls_made, None

        except Exception as e:
            last_error = str(e)
            logger.warning(f"Agent attempt {attempt + 1} failed: {last_error}")

            # Check for specific error types
            error_lower = last_error.lower()

            # Rate limit errors - wait longer
            if "rate" in error_lower or "429" in last_error or "quota" in error_lower:
                backoff = min(backoff * 2, MAX_BACKOFF)
                logger.info(f"Rate limit detected, backing off for {backoff}s")

            # Auth errors - don't retry
            if "401" in last_error or "403" in last_error or "invalid api key" in error_lower:
                logger.error("Authentication error - not retrying")
                break

            # Network/timeout errors - retry with backoff
            if attempt < max_retries - 1:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, MAX_BACKOFF)

    return "", [], last_error


# ============================================================================
# Message Processing
# ============================================================================

async def process_message(
    user_id: str,
    message: str,
    history: List[Message],
    session: Session
) -> Tuple[str, List[ToolCallResult]]:
    """
    Process a user message with the AI agent.

    Args:
        user_id: User ID for authorization
        message: User's input message
        history: Previous conversation messages
        session: Database session

    Returns:
        Tuple of (response_text, list of tool calls)
    """
    # Set request context for tools
    set_request_context(user_id, session)

    # If no agent, use fallback logic
    if not _agent:
        logger.info("No agent available, using fallback processing")
        return await fallback_process(user_id, message, session)

    try:
        # Build input messages for agent
        input_messages = []

        # Add conversation history (last 10 messages for context, balanced for performance)
        for msg in history[-10:]:
            input_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add current message
        input_messages.append({"role": "user", "content": message})

        # Run agent with retry logic
        response_text, tool_calls, error = await run_agent_with_retry(_agent, input_messages)

        if error:
            logger.error(f"Agent failed after retries: {error}")

            # Provide specific error messages
            error_lower = error.lower()

            if "rate" in error_lower or "429" in error or "quota" in error_lower:
                return (
                    "I'm currently experiencing high demand. Please wait a moment and try again.",
                    []
                )
            elif "401" in error or "403" in error or "invalid api key" in error_lower:
                # Fall back to basic processing
                logger.info("Auth error, falling back to basic processing")
                return await fallback_process(user_id, message, session)
            elif "timeout" in error_lower or "timed out" in error_lower:
                return (
                    "The request took too long. Please try a simpler request or try again.",
                    []
                )
            else:
                # Generic error - try fallback
                logger.info(f"Generic error, falling back: {error}")
                return await fallback_process(user_id, message, session)

        return response_text, tool_calls

    except Exception as e:
        logger.error(f"Unexpected error in process_message: {e}")
        # Fallback to basic processing on unexpected error
        return await fallback_process(user_id, message, session)


async def fallback_process(
    user_id: str,
    message: str,
    session: Session
) -> Tuple[str, List[ToolCallResult]]:
    """
    Fallback processing when GROQ API is unavailable.

    Uses enhanced keyword matching with support for:
    - Multiple operations
    - Flexible natural language
    - Off-topic detection
    - Position-based task references
    """
    import re

    # Set context for tools
    set_request_context(user_id, session)

    msg_lower = message.lower()
    tool_calls_made = []
    responses = []

    # Off-topic detection (check first)
    off_topic_patterns = [
        r'\b(weather|temperature|forecast)\b',
        r'\b(joke|funny|laugh)\b',
        r'\b(who are you|what are you)\b',
        r'\b(calculate|math|compute)\b',
        r'\b(news|headlines)\b',
        r'\b(recipe|cook|food)\b',
        r'\b(translate|language)\b',
        r'\b(code|program|script|debug)\b',
        r'\b(tell me about|explain|define)\b(?!.*task)',
    ]

    # Check if this is an off-topic request
    is_off_topic = any(re.search(pattern, msg_lower) for pattern in off_topic_patterns)

    # But not if it also contains task-related words
    task_indicators = ['task', 'todo', 'remind', 'add', 'create', 'complete', 'done', 'delete', 'remove', 'list', 'show', 'update', 'change']
    has_task_context = any(word in msg_lower for word in task_indicators)

    if is_off_topic and not has_task_context:
        return (
            "I'm a task management assistant. I can help you add, list, complete, update, or delete tasks. What would you like to do with your tasks?",
            []
        )

    # Helper function to get task by position
    def get_task_by_position(position: str) -> Optional[int]:
        result = list_tasks(status="all")
        if result["status"] != "success" or not result["data"]:
            return None

        tasks = result["data"]
        position_lower = position.lower()

        if "first" in position_lower or position_lower == "1":
            return tasks[0]["id"]
        elif "last" in position_lower:
            return tasks[-1]["id"]
        elif "second" in position_lower or position_lower == "2":
            return tasks[1]["id"] if len(tasks) > 1 else None
        elif "third" in position_lower or position_lower == "3":
            return tasks[2]["id"] if len(tasks) > 2 else None

        return None

    # Split message into potential multiple commands
    # Split on: "and", "then", ",", "also"
    commands = re.split(r'\s+and\s+|\s+then\s+|\s*,\s*|\s+also\s+', message, flags=re.IGNORECASE)
    commands = [cmd.strip() for cmd in commands if cmd.strip()]

    for cmd in commands:
        cmd_lower = cmd.lower()

        # ADD TASK intent
        add_patterns = [
            r'^add\s+(?:task\s+)?(.+)$',
            r'^create\s+(?:a\s+)?(?:task\s+)?(?:to\s+)?(.+)$',
            r'^new\s+task\s+(.+)$',
            r'^remind\s+(?:me\s+)?(?:to\s+)?(.+)$',
            r'^remember\s+(?:to\s+)?(.+)$',
            r'^i\s+need\s+to\s+(.+)$',
            r'^i\s+have\s+to\s+(.+)$',
            r"^don'?t\s+(?:let\s+me\s+)?forget\s+(?:to\s+)?(.+)$",
            r'^put\s+(.+)\s+on\s+(?:my\s+)?(?:list|todo)$',
        ]

        for pattern in add_patterns:
            match = re.match(pattern, cmd_lower)
            if match:
                title = match.group(1).strip().capitalize()
                if title:
                    result = add_task(title=title)
                    tool_calls_made.append(ToolCallResult(
                        tool="add_task",
                        parameters={"title": title},
                        result=result
                    ))
                    if result["status"] == "success":
                        responses.append(f"Added '{result['data']['title']}'")
                    else:
                        responses.append(result["message"])
                break
        else:
            # LIST TASKS intent
            if any(word in cmd_lower for word in ["show", "list", "what", "see", "my task", "tasks", "todo"]):
                status = "all"
                if "pending" in cmd_lower or "incomplete" in cmd_lower or "haven't" in cmd_lower:
                    status = "pending"
                elif "completed" in cmd_lower or "done" in cmd_lower or "finished" in cmd_lower:
                    status = "completed"

                result = list_tasks(status=status)
                tool_calls_made.append(ToolCallResult(
                    tool="list_tasks",
                    parameters={"status": status},
                    result=result
                ))

                if result["status"] == "success":
                    tasks = result["data"]
                    if not tasks:
                        responses.append("You don't have any tasks yet. Try 'add [task name]' to create one!")
                    else:
                        lines = [result["message"] + ":"]
                        for task in tasks:
                            status_emoji = "v" if task["completed"] else "[ ]"
                            lines.append(f"  {status_emoji} {task['id']}. {task['title']}")
                        responses.append("\n".join(lines))
                else:
                    responses.append(result["message"])

            # COMPLETE TASK intent
            elif any(word in cmd_lower for word in ["done", "complete", "finish", "mark"]):
                # Try to find task ID
                numbers = re.findall(r'\d+', cmd)
                task_id = None

                if numbers:
                    task_id = int(numbers[0])
                else:
                    # Check for position reference
                    for pos in ["first", "last", "second", "third"]:
                        if pos in cmd_lower:
                            task_id = get_task_by_position(pos)
                            break

                if task_id:
                    result = complete_task(task_id=task_id)
                    tool_calls_made.append(ToolCallResult(
                        tool="complete_task",
                        parameters={"task_id": task_id},
                        result=result
                    ))
                    if result["status"] == "success":
                        responses.append(f"Completed '{result['data']['title']}'")
                    else:
                        responses.append(result["message"])
                else:
                    responses.append("Which task? Please specify a task ID or say 'first task', 'last task', etc.")

            # DELETE TASK intent
            elif any(word in cmd_lower for word in ["delete", "remove", "cancel", "get rid"]):
                numbers = re.findall(r'\d+', cmd)
                task_id = None

                if numbers:
                    task_id = int(numbers[0])
                else:
                    for pos in ["first", "last", "second", "third"]:
                        if pos in cmd_lower:
                            task_id = get_task_by_position(pos)
                            break

                if task_id:
                    result = delete_task(task_id=task_id)
                    tool_calls_made.append(ToolCallResult(
                        tool="delete_task",
                        parameters={"task_id": task_id},
                        result=result
                    ))
                    if result["status"] == "success":
                        responses.append(f"Deleted '{result['data']['title']}'")
                    else:
                        responses.append(result["message"])
                else:
                    responses.append("Which task? Please specify a task ID or say 'first task', 'last task', etc.")

            # UPDATE TASK intent
            elif any(word in cmd_lower for word in ["change", "update", "modify", "rename", "edit"]):
                numbers = re.findall(r'\d+', cmd)
                if numbers:
                    task_id = int(numbers[0])
                    # Try to extract new title
                    match = re.search(r'to\s+["\']?(.+?)["\']?\s*$', cmd, re.IGNORECASE)
                    if match:
                        new_title = match.group(1).strip()
                        result = update_task(task_id=task_id, title=new_title)
                        tool_calls_made.append(ToolCallResult(
                            tool="update_task",
                            parameters={"task_id": task_id, "title": new_title},
                            result=result
                        ))
                        if result["status"] == "success":
                            responses.append(f"Updated task to '{result['data']['title']}'")
                        else:
                            responses.append(result["message"])
                    else:
                        responses.append(f"What would you like to change task {task_id} to?")
                else:
                    responses.append("Which task? Please specify the task ID.")

    # If no commands were processed
    if not responses:
        return (
            "I can help you manage your tasks! Try:\n"
            "- \"Add buy groceries\" to create a task\n"
            "- \"Show my tasks\" to see your list\n"
            "- \"Complete task 1\" to mark done\n"
            "- \"Delete task 2\" to remove\n"
            "- \"Add X and add Y\" for multiple tasks",
            []
        )

    # Combine responses
    if len(responses) == 1:
        final_response = responses[0]
    else:
        final_response = "Done! " + " | ".join(responses)

    return final_response, tool_calls_made
