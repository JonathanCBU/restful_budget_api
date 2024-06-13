CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  UNIQUE (username)
);

INSERT INTO users (username, password) 
VALUES
    ("tester_1", "pwd1"),
    ("tester_2", "pwd2"),
    ("tester_3", "pwd3");

CREATE TABLE IF NOT EXISTS assets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  report_id INTEGER,
  date TEXT NOT NULL,
  description TEXT NOT NULL,
  value REAL NOT NULL,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(report_id) REFERENCES reports(id)
);

CREATE TABLE IF NOT EXISTS liabilities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  report_id INTEGER,
  date TEXT NOT NULL,
  description TEXT NOT NULL,
  value REAL NOT NULL,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(report_id) REFERENCES reports(id)
);

CREATE TABLE IF NOT EXISTS reports (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  net_worth REAL NOT NULL,
  FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS patterns (
  id INTEGER PRIMARY KEY,
  title TEXT,
  date TEXT,
  value TEXT,
  UNIQUE (title)
)
