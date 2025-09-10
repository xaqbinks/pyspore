# Project Progenitus

A 2D single-player life simulation game inspired by Maxis's *Spore*, written in Python with Pygame. This project is currently in development, with the "Cell Stage" being the first playable milestone.

## How to Play

The goal of the Cell Stage is to survive and evolve.
- **Move** your cell around the primordial soup.
- **Eat** food that matches your chosen diet (plants for Herbivores, other small cells for Carnivores) to collect DNA points.
- **Avoid** larger, hostile cells that will hunt you.
- **Evolve** by finding a mate cell. This will open the Cell Editor, where you can spend DNA to add new parts to your cell.
- **Discover** new parts by breaking open meteorites.
- **Win** by collecting enough DNA to fill the progress bar at the top of the screen.

## Controls

- **W, A, S, D** or **Arrow Keys**: Rotate and move your cell.
- **ESC**: Open the Pause Menu. From here you can Save, Resume, or return to the Main Menu.

## Features

*   **Procedural Generation:** All visuals (cells, backgrounds) and audio are generated procedurally.
*   **Life Simulation:** Play as a single cell, eat, grow, and evolve.
*   **Diet System:** Choose to be a Herbivore or Carnivore.
*   **Evolution Editor:** Evolve your cell by adding parts that modify your stats.
*   **Part Unlocking:** Discover new parts by breaking open meteorites.
*   **Save/Load System:** Save your progress at any time and load it from the main menu.

## Getting Started

Follow these steps to run the game on your local machine.

### 1. Prerequisites

Make sure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).

### 2. Clone the Repository

First, you need to get the project files. If you have Git installed, you can clone the repository.
*(Note: A placeholder is used here. You would replace this with the actual URL of the repository.)*
```bash
# Replace the URL below with the actual repository URL
git clone https://github.com/example/project-progenitus.git
cd project-progenitus
```
If you do not have Git, you can download the source code as a ZIP file from the repository page and extract it.

### 3. Set Up a Virtual Environment (Recommended)

A virtual environment helps keep the project's dependencies separate from other Python projects on your system.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```
You should see `(venv)` at the beginning of your command prompt line, indicating the virtual environment is active.

### 4. Install Dependencies

With your virtual environment active, install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```
This command reads the `requirements.txt` file and installs all the necessary packages (like Pygame).

### 5. Run the Game

You are now ready to play! Run the following command from the project's root directory:
```bash
python main.py
```

The game window should now appear. Enjoy!
