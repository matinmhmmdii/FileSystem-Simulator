# File System Simulator

A simple in-memory file system simulator written in Python. This project implements a file system with support for commands like `mkdir`, `touch`, `rm`, `cd`, `ls`, `nwfiletxt`, `appendtxt`, `editline`, `deline`, `cat`, `mv`, `cp`, and `rename`. The file system operates entirely in memory and does not interact with the disk.

## Features

- Supports absolute and relative paths.
- Implements a tree structure for directories and files.
- Deep copy for file and directory copying to ensure independence.
- Error handling for invalid paths, existing files/directories, and more.
- No dependency on the `os` module, fully in-memory.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/matinmhmmdii/FileSystem-Simulator.git
   cd file_system_project
   ```
2. Ensure Python 3.6+ is installed.
3. No external dependencies are required.

## Usage

Run the main script:

```bash
python main.py
```

Enter commands at the prompt (e.g., `/ $`). Type `exit` to quit.

### Supported Commands

- `mkdir <name>`: Create a new directory.
- `touch <name>`: Create a new text file.
- `rm <path>`: Remove a file or directory.
- `cd <path>`: Change current directory.
- `ls`: List contents of current directory.
- `cat <path>`: Display file content.
- `nwfiletxt <path>`: Write new content to a file.
- `appendtxt <path>`: Append content to a file.
- `editline <path> <line_num> <text>`: Edit a specific line in a file.
- `deline <path> <line_num>`: Delete a specific line in a file.
- `mv <src_path> <dst_path>`: Move a file or directory.
- `cp <src_path> <dst_path>`: Copy a file or directory.
- `rename <path> <new_name>`: Rename a file or directory.

## Project Structure

```
file_system_project/
├── src/
│   ├── __init__.py
│   ├── node.py        
│   └── filesystem.py  
│          
├── .gitignore
├── main.py 
├── README.md
└── requirements.txt
```

## License

MIT License