import os
import subprocess

def read_file(filepath: str) -> str:
    """Reads the contents of a file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {filepath}: {e}"

def list_dir(directory: str) -> str:
    """Lists the contents of a directory."""
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing directory {directory}: {e}"

def execute_command(command: str, cwd: str = ".") -> str:
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        output = result.stdout
        if result.stderr:
            output += "\nError Output:\n" + result.stderr
        return output
    except Exception as e:
        return f"Error executing command: {e}"

def write_file(filepath: str, content: str) -> str:
    """Writes the specified content to a file, overwriting it entirely."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing to file {filepath}: {e}"

def replace_file_content(filepath: str, target_content: str, replacement_content: str) -> str:
    """Replaces a specific contiguous block of text in a file with new text."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        if target_content not in content:
            return f"Error: target_content not found in {filepath}. You must provide the EXACT existing string, including whitespace."
            
        new_content = content.replace(target_content, replacement_content, 1)
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        return f"Successfully replaced content in {filepath}"
    except Exception as e:
        return f"Error modifying file {filepath}: {e}"

def find_files(directory: str) -> str:
    """Recursively lists all files in a directory tree."""
    try:
        all_files = []
        ignore_dirs = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'env', 'build', 'dist'}
        
        for root, dirs, files in os.walk(directory):
            # Aggressively filter out massive/noisy directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_dirs]
            
            for file in files:
                if not file.startswith('.'):
                    rel_path = os.path.relpath(os.path.join(root, file), directory)
                    all_files.append(rel_path)
                    
        if not all_files:
            return "No files found."
            
        result = "\n".join(all_files)
        if len(result) > 3500:
            return result[:3500] + "\n...[WARNING: Output too large, some files hidden. Please use list_dir on specific subfolders!]"
        return result
    except Exception as e:
        return f"Error finding files in {directory}: {e}"

# Groq Tool Definitions
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The absolute or relative path to the file."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "Lists the contents of a directory (1 level deep).",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The path to the directory."
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_files",
            "description": "Recursively lists ALL files in a directory and its subfolders. Use this to quickly see the entire project structure.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The path to the root directory to search."
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Executes a shell command and returns the output. Use this for building, testing, or running scripts. DO NOT use this to write files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute."
                    },
                    "cwd": {
                        "type": "string",
                        "description": "The current working directory for the command.",
                        "default": "."
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes the specified content to a file, overwriting it entirely. Use this instead of shell commands to edit code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file."
                    },
                    "content": {
                        "type": "string",
                        "description": "The full code content to write to the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_file_content",
            "description": "Replaces a specific contiguous block of text in an existing file with new text. Much faster and safer than write_file for small edits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file."
                    },
                    "target_content": {
                        "type": "string",
                        "description": "The exact string to be replaced. Must include exact whitespace and indentation."
                    },
                    "replacement_content": {
                        "type": "string",
                        "description": "The content to replace the target content with."
                    }
                },
                "required": ["filepath", "target_content", "replacement_content"]
            }
        }
    }
]

# Map for execution
TOOL_FUNCTIONS = {
    "read_file": read_file,
    "list_dir": list_dir,
    "find_files": find_files,
    "execute_command": execute_command,
    "write_file": write_file,
    "replace_file_content": replace_file_content
}
