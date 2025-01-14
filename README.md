# CursorBoost

CursorBoost is a CLI tool designed to dynamically generate and maintain an accurate `.cursorrules` file for improved integration with **Cursor**, a VSCode fork powered by GPT-4o. By automating system and project environment analysis, CursorBoost ensures that `.cursorrules` stays up-to-date, reducing errors and enhancing coding assistance in complex development environments.

## Features
- **System Snapshot**: Collects real-time system information (e.g., Docker status, disk usage, memory stats, network ports).
- **Project Analysis**: Scans project directories and dependencies to provide detailed context.
- **LLM Integration**: Uses OpenAI's GPT-4o to generate `.cursorrules` based on collected data.
- **Docker Logs**: Includes logs from running Docker containers for debugging.
- **Continuous Updates**: Periodically refreshes `.cursorrules` and system snapshots.

## How It Works
- **Run Location**: CursorBoost is designed to run from the **root of your project directory**. 
  - Example directory structure:
    ```
    .
    ..
    .cursorboost/
    .cursorrules
    ```
  - The `.cursorboost` directory contains the tool's configuration and scripts.
  - The `.cursorrules` file is generated in the **parent directory** of `.cursorboost` (i.e., the root of your project).

- **Output Files**:
  - `.cursorrules`: A dynamically generated file that integrates system and project context for Cursor.
  - `snapshot.txt`: Contains the latest system and project snapshots for reference.

## Installation
1. Navigate to your project's root directory:
   ```bash
   cd /path/to/your/project
   ```
2. Clone the repository:
   ```bash
   git clone git@github.com:grp06/cursor-boost.git .cursorboost
   cd .cursorboost
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the `.cursorboost` directory:
     ```bash
     touch .cursorboost/.env
     ```
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage
1. **Run CursorBoost**:
   - Navigate to the **root of your project directory** (where `.cursorboost` is located).
   - Run the tool:
     ```bash
     python .cursorboost/index.py
     ```
   - The tool will continuously monitor and update `.cursorrules` every 60 seconds.

2. **Configuration**:
   - Modify `.cursorboost/config.json` to customize settings like directory depth, ignored patterns, and disk usage thresholds.
   - **Set Your Root Path**:
     - Open `.cursorboost/config.json` and update the `base_project_path` field to point to the root directory of your project. For example:
       ```json
       {
         "base_project_path": "/path/to/your/project"
       }
       ```
     - If you leave the default value (`"<your_project_path>"`), the tool will raise an error and prompt you to update it.

3. **Project List**:
   - Add project directories to `.cursorboost/containers-list.md` in the following format:
     ```
     - project_name_1
     - project_name_2
     ```

## Output
- **`.cursorrules`**: Generated in the parent directory of `.cursorboost` (i.e., the root of your project).
- **`snapshot.txt`**: Contains the latest system and project snapshots for reference.

## Troubleshooting
- **Missing `config.json`**: Default settings will be used if the file is not found.
- **Invalid `base_project_path`**: If the `base_project_path` is not set or points to a non-existent directory, the tool will raise an error. Update the path in `config.json` to fix this.
- **Docker Errors**: Ensure Docker is installed and running.
- **OpenAI API Key Missing**: Add your API key to the `.env` file.

## Example Directory Structure
Here’s an example of how your project directory might look:
```
.
├── .cursorboost/
│   ├── index.py
│   ├── config.json
│   ├── README.md
│   ├── containers-list.md
│   └── ...
├── .cursorrules
├── snapshot.txt
├── project-folder-1/
├── project-folder-2/
└── ...
```
- **`.cursorboost/`**: Contains the CursorBoost tool and configuration files.
- **`.cursorrules`**: Generated at the root of your project directory.
- **`snapshot.txt`**: Contains the latest system and project snapshots.

## New Module Structure
The `index.py` file has been refactored into smaller, more focused modules:

- `config_loader.py`: Handles configuration loading and validation.
- `command_runner.py`: Handles system and project command execution.
- `snapshot_writer.py`: Handles writing snapshots to files.
- `docker_logs.py`: Handles Docker log retrieval.
- `openai_integration.py`: Handles OpenAI API interaction.

Make sure to update your imports in `index.py` to use these new modules.
