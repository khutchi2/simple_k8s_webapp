DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL
);

-- Insert some initial data
INSERT INTO messages (title, content) VALUES ('Welcome', 'Welcome to the Flask K8s App!');
INSERT INTO messages (title, content) VALUES ('Getting Started', 'This is a simple message board application.');
