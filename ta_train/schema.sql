drop table if exists Price;
drop table if exists Variety;

create table Variety (
  id INT(32) UNSIGNED AUTO_INCREMENT NOT NULL,
  type ENUM('ST', 'FX', 'FU') NOT NULL,
  exchange VARCHAR(20),
  name VARCHAR(128) CHARACTER SET utf8 NOT NULL,
  code VARCHAR(16) NOT NULL,

  PRIMARY KEY (id),
  UNIQUE KEY (type, exchange, code)
);

create table Price (
  id INT(64) UNSIGNED AUTO_INCREMENT NOT NULL,
  vid INT(32) UNSIGNED NOT NULL,
  unit ENUM('CNY', 'USD', 'HKD') NOT NULL,
  period VARCHAR(16) NOT NULL,
  start_date DATETIME NOT NULL,
  start_ts TIMESTAMP NOT NULL,
  open INT(32) NOT NULL,
  high INT(32) NOT NULL,
  low INT(32) NOT NULL,
  close INT(32) NOT NULL,
  volume INT(64) NOT NULL,
  turnover INT(64) NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (vid) REFERENCES Variety(id),
  UNIQUE KEY (vid, period, start_ts)
);