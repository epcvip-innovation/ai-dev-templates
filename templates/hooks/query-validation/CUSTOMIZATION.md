# Query Validation Hook — Customization

[← Back to Query Validation README](./README.md)

**Purpose**: Per-database patterns and hook extension points for the query validation hook.

---

## Add Custom Query Runners

Edit `~/.claude/hooks/validate-query-execution.py`, find `is_query_execution()`:

```python
def is_query_execution(command):
    # ... existing code ...

    patterns = [
        r'python3?\s+run_validation_query\.py',
        r'python3?\s+run_query\.py',
        r'python3?\s+.*athena_client\.py',
        r'python3?\s+-m\s+core\.athena_client',
        r'python3?\s+my_custom_runner\.py',  # Add your runner
        r'node\s+run_bigquery\.js',          # Add BigQuery runner
    ]

    return any(re.search(pattern, command) for pattern in patterns)
```

---

## Add Custom Whitelist Commands

Edit hook, find early exit section:

```python
def is_query_execution(command):
    command_stripped = command.strip()
    if command_stripped.startswith(('ls', 'cd', 'cat', 'grep', 'find', 'echo',
                                    'pwd', 'mkdir', 'rm', 'cp', 'mv', 'touch',
                                    'head', 'tail', 'wc', 'sort', 'uniq', 'git',
                                    'npm', 'node', 'pip')):  # Add your commands
        return False
    # ... rest of function ...
```

---

## Change Marker Location

Edit hook, find `check_validation_marker()`:

```python
def check_validation_marker(query_path):
    # Default: /tmp/query_validated_<hash>.marker
    marker_path = Path(f'/tmp/query_validated_{path_hash}.marker')

    # Custom: Use project directory
    # marker_path = Path(f'./.query_markers/validated_{path_hash}.marker')

    return marker_path.exists(), marker_path
```

**Note**: Must also update `/validate-query` slash command to use the same location.

---

## Adapt for Other Databases

Update patterns to match your database execution commands:

**BigQuery**:
```python
patterns = [
    r'python3?\s+run_bigquery\.py',
    r'bq\s+query',
]
```

**Snowflake**:
```python
patterns = [
    r'python3?\s+run_snowflake\.py',
    r'snowsql\s+-q',
]
```

**Postgres**:
```python
patterns = [
    r'psql\s+-f',
    r'python3?\s+run_postgres\.py',
]
```

---

## Per-Project Validation

Use project-level hooks with custom logic per project:

```python
# .claude/hooks/validate-query-execution.py
import os

project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')

if 'project-a' in project_dir:
    # Strict validation for project A
    require_partition_filter()
elif 'project-b' in project_dir:
    # Relaxed validation for project B
    pass
```

---

## Add Content-Based Validation Checks

Extend the hook to inspect query content before execution:

```python
# After extracting query_path
with open(query_path) as f:
    query = f.read()

# Check for partition filters
if 'WHERE' not in query:
    block_execution("Missing WHERE clause - add partition filter")

# Check for expensive operations
if 'SELECT *' in query and 'LIMIT' not in query:
    block_execution("SELECT * without LIMIT - add row limit")
```

---

**Related**: [Query Validation README](./README.md) | [Hooks README](../README.md) | [Hooks Reference](../HOOKS_REFERENCE.md)
