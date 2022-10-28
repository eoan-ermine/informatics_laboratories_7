CREATE SCHEMA bot;

CREATE TABLE IF NOT EXISTS bot.metainfo (
	"current_week" int NOT NULL
);

CREATE TABLE IF NOT EXISTS bot.subject (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	CONSTRAINT "subject_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.class_type (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	CONSTRAINT "class_type_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.class (
	"id" serial NOT NULL,
	"subject" int NOT NULL REFERENCES bot.subject(id),
	"class_type" int NOT NULL REFERENCES bot.class_type(id),
	CONSTRAINT "class_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.classes_timetable(
	"id" serial NOT NULL,
	"start_time" time NOT NULL,
	CONSTRAINT "classes_timetable_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.teacher (
	"id" serial NOT NULL,
	"full_name" varchar(255) NOT NULL,
	CONSTRAINT "teacher_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.teacher_class (
	"id" serial NOT NULL,
	"teacher" int NOT NULL REFERENCES bot.teacher(id),
	"class" int NOT NULL REFERENCES bot.class(id),
	CONSTRAINT "teacher_class_pk" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS bot.timetable (
	"id" serial NOT NULL,
	"week" smallint NOT NULL,
	"day" smallint NOT NULL,
	"class" int NOT NULL REFERENCES bot.class(id),
	"class_number" int NOT NULL REFERENCES bot.classes_timetable(id),
	"room_number" int NOT NULL,
	CONSTRAINT "timetable_pk" PRIMARY KEY ("id")
);
