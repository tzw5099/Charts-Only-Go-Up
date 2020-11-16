
-- https://flask.palletsprojects.com/en/0.12.x/tutorial/schema/#tutorial-schema
drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
