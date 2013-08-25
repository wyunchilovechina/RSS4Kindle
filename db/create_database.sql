create database if not exists RSS4Kindle default charset utf8 COLLATE utf8_general_ci;

use RSS4Kindle
create table if not exists RSSFeeds (
	id integer auto_increment,
	RSSFeedURL varchar(1024) not null,
	RSSFeedTitle varchar(256) not null,
	RSSTag varchar(256),
	primary key(id)
);

create table if not exists RSSItems (
	id integer auto_increment,
	RSSFeedURL varchar(1024) not null,
	ItemTitle varchar(256),
	ItemLink varchar(1024) not null,
	ItemPubDate Datetime,
	primary key(id)
);