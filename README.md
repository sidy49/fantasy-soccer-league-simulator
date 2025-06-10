
# ⚽ Fantasy Football League Simulator

A Python-based simulation of a complete fantasy football season built using object-oriented programming and advanced data structures. This project models players, teams, game outcomes, and seasonal standings using custom-built components like hash tables, queues, and linked lists.

---

## 🚀 Features

- Simulates a full season of football matches between custom teams.
- Implements realistic goal scoring using weighted probabilities.
- Tracks player stats, goals, and team histories.
- Supports season delay, game rescheduling, and blogging system for teams.
- Uses efficient data structures like:
  - 🧠 `LazyDoubleTable`: Double-hashing hash table with lazy deletion
  - 🗓 `HashyDateTable`: Date-optimized hash table for blog posts
  - 🔁 `CircularQueue`: Stores game result history
  - 📋 `LinkedList` and `ArrayList`: For flexible team and player storage

---

## 📁 File Structure

| File | Purpose |
|------|---------|
| `player.py` | Manages player info, stats, and performance tracking |
| `team.py` | Handles player rosters, match history, blog posts |
| `season.py` | Generates fixture schedule, simulates matches, maintains leaderboard |
| `game_simulator.py` | Simulates outcomes between two teams using probabilistic models |
| `lazy_double_table.py` | Custom hash table using double hashing and lazy deletion |
| `hashy_date_table.py` | Hash table optimized for date-based blog post indexing |

---

## 🛠 Technologies

- Python
- Object-Oriented Design/ Programming
- Data Structures & Algorithms
- Time Complexity Analysis

---

## 🧪 How to Run

# Run your own test (e.g. run_tests.py)
python test_run.py
