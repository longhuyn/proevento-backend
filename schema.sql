DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Profile;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Notification;
DROP TABLE IF EXISTS ChatRoom;
DROP TABLE IF EXISTS UserChat;
DROP TABLE IF EXISTS GroupChat;
DROP TABLE IF EXISTS ChatMessage;
DROP TABLE IF EXISTS UserGroup;
DROP TABLE IF EXISTS GroupSuggestion;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Badges;

CREATE TABLE User (
  userId INTEGER PRIMARY KEY AUTOINCREMENT,
  fullName TEXT NOT NULL,
  email TEXT NOT NULL,
  username TEXT NOT NULL,
  profileImage TEXT NOT NULL,
  sendNotification BOOLEAN
);

CREATE TABLE Event (
  eventId INTEGER PRIMARY KEY AUTOINCREMENT,
  eventName TEXT NOT NULL,
  userId INTEGER NOT NULL,
  description TEXT NOT NULL,
  tags TEXT NOT NULL,
  categories TEXT NOT NULL,
  participants TEXT,
  reviews TEXT,
  favorites TEXT,
  type TEXT NOT NULL,
  zoomLink TEXT NOT NULL,
  eventImage TEXT NOT NULL,
  date TEXT NOT NULL,
  numParticipate INTEGER NOT NULL,
  recorded BOOLEAN,
  Record TEXT
);

CREATE TABLE Profile (
  profileId INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER NOT NULL,
  tags TEXT,
  followers TEXT,
  following TEXT,
  bio TEXT,
  badges TEXT
);

CREATE TABLE Notification (
  notificationId INTEGER PRIMARY KEY AUTOINCREMENT,
  recipientId INTEGER NOT NULL,
  type TEXT NOT NULL,
  date TEXT NOT NULL,
  eventId INTEGER,
  eventName TEXT,
  userId INTEGER,
  userName TEXT,
  groupId INTEGER,
  groupName TEXT,
  uploadLink TEXT
);

CREATE TABLE UserGroup (
  groupId INTEGER PRIMARY KEY AUTOINCREMENT,
  ownerId INTEGER NOT NULL,
  name TEXT NOT NULL,
  logo TEXT,
  description NOT NULL,
  categories TEXT,
  participants TEXT,
  suggestionDate TEXT
);

CREATE TABLE GroupSuggestion (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  date TEXT NOT NULL,
  description TEXT,
  tags TEXT NOT NULL,
  categories TEXT NOT NULL,
  eventImage TEXT,
  userId INTEGER NOT NULL,
  groupId Integer NOT NULL,
  status TEXT,
  voters TEXT,
  recorded BOOLEAN
);

CREATE TABLE UserChat (
  roomId INTEGER PRIMARY KEY AUTOINCREMENT,
  user1 INTEGER NOT NULL,
  user2 INTEGER NOT NULL
);

CREATE TABLE GroupChat (
  roomId INTEGER PRIMARY KEY AUTOINCREMENT,
  groupId INTEGER NOT NULL,
  userId INTEGER NOT NULL
);

CREATE TABLE ChatMessage (
  messageId INTEGER PRIMARY KEY AUTOINCREMENT,
  roomId INTEGER NOT NULL,
  userId INTEGER NOT NULL,
  message TEXT NOT NULL,
  chatType INTEGER, /* 0 for user_chat, 1 for group_chat */
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Category (
  categoryId INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

INSERT INTO Category (name) VALUES ("education");
INSERT INTO Category (name) VALUES ("sports");
INSERT INTO Category (name) VALUES ("music");
INSERT INTO Category (name) VALUES ("stonks");
INSERT INTO Category (name) VALUES ("memes");
INSERT INTO Category (name) VALUES ("religion");
INSERT INTO Category (name) VALUES ("coding");
INSERT INTO Category (name) VALUES ("FUCLA");
INSERT INTO Category (name) VALUES ("fitness");
INSERT INTO Category (name) VALUES ("animals");
INSERT INTO Category (name) VALUES ("hobbies");
INSERT INTO Category (name) VALUES ("politics");
INSERT INTO Category (name) VALUES ("instagram");
INSERT INTO Category (name) VALUES ("technology");
INSERT INTO Category (name) VALUES ("gaming");
INSERT INTO Category (name) VALUES ("food");
INSERT INTO Category (name) VALUES ("environment");
INSERT INTO Category (name) VALUES ("relationships");
INSERT INTO Category (name) VALUES ("anime");
INSERT INTO Category (name) VALUES ("comedy");
INSERT INTO Category (name) VALUES ("culture");
INSERT INTO Category (name) VALUES ("18+");

CREATE TABLE Badges (
  badgeId INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

INSERT INTO Badges (name) VALUES ("Entertaining");
INSERT INTO Badges (name) VALUES ("On Time");
INSERT INTO Badges (name) VALUES ("Informative");
INSERT INTO Badges (name) VALUES ("Life Changing");
INSERT INTO Badges (name) VALUES ("Trash");
INSERT INTO Badges (name) VALUES ("Amazing");
INSERT INTO Badges (name) VALUES ("Must Watch");
INSERT INTO Badges (name) VALUES ("Visionary");
INSERT INTO Badges (name) VALUES ("Waste of Time");
INSERT INTO Badges (name) VALUES ("Lovely");