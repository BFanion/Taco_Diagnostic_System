# Taco Diagnostic System

A graphical launcher for diagnostic Python scripts.

## Features

- Auto-detects `.py` scripts in the same directory and displays them as launch buttons
- **Setup** button to manually add scripts from any folder via file dialog
- Saves manually added script paths to `menu_config.json` for persistence across sessions
- Remove button (X) to delete manually added scripts from the menu
- Scrollable interface to handle many scripts

## Usage

Run the menu:

```bash
python Taco_Diagnostic_System_Menu.py
```

- Click any script button to launch it
- Click **Setup - Add Scripts** to browse and add external Python files
- Click the red **X** next to an added script to remove it

## Files

| File | Description |
|------|-------------|
| `Taco_Diagnostic_System_Menu.py` | Main GUI launcher |
| `menu_config.json` | Auto-generated config storing manually added script paths |

## Requirements

- Python 3.x
- tkinter (included with standard Python installations)
