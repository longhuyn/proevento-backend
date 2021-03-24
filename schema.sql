DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Profile;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS FollowNotification;
DROP TABLE IF EXISTS EventNotification;

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
  participants TEXT,
  favorites TEXT,
  type TEXT NOT NULL,
  date TEXT NOT NULL,
  zoomLink TEXT NOT NULL,
  eventImage TEXT NOT NULL
);

CREATE TABLE Profile (
  profileId INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER NOT NULL,
  tags TEXT,
  followers TEXT,
  following TEXT
);

CREATE TABLE FollowNotification (
  notificationId INTEGER PRIMARY KEY AUTOINCREMENT,
  recipientId INTEGER NOT NULL,
  status TEXT NOT NULL,
  date TEXT NOT NULL,
  output TEXT NOT NULL,
  followerId INTEGER
);

CREATE TABLE EventNotification (
  notificationId INTEGER PRIMARY KEY AUTOINCREMENT,
  eventId INTEGER NOT NULL,
  recipientId INTEGER NOT NULL,
  date TEXT NOT NULL,
  description TEXT NOT NULL,
  joinurl TEXT NOT NULL,
  eventName TEXT NOT NULL,
  userId TEXT NOT NULL
);