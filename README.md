# InfiniteShelf
### A continuously growing virtual bookshelf with Random Book Generation

## Overview

InfiniteShelf is a Python-based desktop application that combines a traditional library management system with an automated book generation engine. Unlike conventional library software, InfiniteShelf can continuously generate realistic book records using the Faker library until the user manually stops the generation process.

The application provides an intuitive Tkinter GUI for managing books while storing all records in JSON format for persistent storage.

---

## Features

### Library Management
- Add new books
- Delete books (status-based deletion)
- Search books by:
  - Title
  - Author
  - Year
  - Book ID
- Sort books by:
  - Title
  - Author
  - Year
- View detailed book information
- Rent and return books
- Track book availability

---

### Continuous Book Generation

One of the unique features of InfiniteShelf is its **continuous random book generation engine**.

The application:

- Generates realistic book titles
- Generates random author names
- Assigns publication years
- Assigns random availability status
- Continuously creates new book entries
- Stops only when the user presses **Stop Generation**

This makes the application useful for generating large datasets for testing, UI validation, database experiments, and performance benchmarking.

---

## Technologies Used

- Python
- Tkinter
- Faker
- JSON
- Threading
- Object-Oriented Programming

---

## Project Structure

```
InfiniteShelf/
│
├── main.py
├── lib_default.json
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/InfiniteShelf.git
```

Install dependencies

```bash
pip install faker
```

Run

```bash
python main.py
```

---

## How It Works

1. Launch the application.
2. Create or load a JSON library.
3. Manage books manually.
4. Click **Generate Random Books**.
5. InfiniteShelf continuously generates realistic book records.
6. Press **Stop Generation** whenever you want.
7. All generated books are automatically saved into the JSON database.

---

## Future Enhancements

- SQLite/MySQL database integration
- Barcode support
- QR code generation
- User authentication
- Borrowing history
- Book recommendations
- Dark mode
- Statistics dashboard
- CSV and Excel export

---

## Learning Outcomes

This project demonstrates practical implementation of:

- GUI Development using Tkinter
- JSON File Handling
- Multithreading
- Data Structures
- Event-Driven Programming
- Random Data Generation
- CRUD Operations
- Search and Sorting Algorithms
