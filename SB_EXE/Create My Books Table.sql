DROP TABLE "My Books"

CREATE TABLE "My Books"(
	"ID" INTEGER UNIQUE PRIMARY KEY,
	"Title" CHARACTER(50),
	"House" CHARACTER(50),
	"Room" CHARACTER(50),
	"Skill Book" CHARACTER(3),
	"Spell Tome" CHARACTER(3)
	);