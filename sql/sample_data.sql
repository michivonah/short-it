-- Add sample data to database
INSERT INTO "url" ("slug", "destination", "description") VALUES
	('demo', 'https://youtube.ch', 'YouTube'),
	('michivonah', 'https://michivonah.ch', 'michivonah.ch'),
	('bbzw', 'https://beruf.lu.ch/bbzw', 'Website BBZW');

INSERT INTO "user" ("name", "mail", "token") VALUES
	('admin', 'example@example.com', 'DixIGzHLoZGvo9m4gsXhPyoXViWRktJZ');

INSERT INTO "analytics" ("fk_urlid") VALUES
	((SELECT "urlid" FROM "url" WHERE "slug" = 'demo'));