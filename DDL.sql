create extension pgcrypto;

create table User_Details
	(UserID			varchar(20),
	 FName			varchar(15),
	 LName			varchar(15),
	 PhNo			char(10),
	 emailID		varchar(25) not NULL,
	 password		text not NULL,
	 primary key(UserID)
	 );

create table Identty
	(GameID			 serial,
	 Game_name		 varchar(50) not NULL,
	 Date_of_release	 date not NULL,
	 primary key(GameID)
	);

create table Game
	(Game_name		varchar(50) not NULL,
	 Date_of_release	date not NULL,
	 Game_size		numeric(4, 1) not NULL,
	 Prod_Studio		varchar(30) not NULL,
	 MRP			numeric(5, 2) not NULL,
	 game_link		text not NULL,
--	 Image			blob,
	 Description		text,
	 Curr_Version		varchar(10) not NULL,
	 Update_Link		text default NULL,
	 Date_of_update		date default NULL,
	 primary key(Game_name, Date_of_release)
	);

create table Category
	(GameID			serial,
	 Cat_Name		varchar(20),
	 primary key(GameID, Cat_Name),
	 foreign key(GameID) references Identty
	);
	
create table Transactions
	(GameID			serial,
	 UserID			varchar(20),
	 Selling_date		date not NULL,
	 Price			numeric(5, 2) not NULL,
	 Curr_Version		varchar(10),
	 PaymentOpt		varchar(20) not NULL,
	 primary key(GameID, UserID),
	 foreign key(GameID) references Identty,
	 foreign key(UserID) references User_Details
	);

create table RateReview
	(GameID			serial,
	 UserID			varchar(20),
	 Rating			numeric(1,0),
	 ReviewText		text,
	 primary key(GameID, UserID),
	 foreign key(GameID) references Identty,
	 foreign key(UserID) references User_Details
	);
