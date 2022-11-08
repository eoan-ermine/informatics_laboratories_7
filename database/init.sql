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

-- Тестовые данные

INSERT INTO bot.metainfo (current_week) VALUES (0);

INSERT INTO
	bot.subject (id, name)
VALUES
	(1, 'Вычислительная техника'), (2, 'Высшая математика'),
	(3, 'Философия'), (4, 'Введение в информационные технологии'),
	(5, 'Компьютерная графика'), (6, 'Социология'),
	(7, 'Иностранный язык'), (8, 'Физическая культура и спорт'),
	(9, 'Алгебра и геометрия')
;

INSERT INTO
	bot.class_type (id, name)
VALUES
	(1, 'Лекция'), (2, 'Практическое занятие'), (3, 'Лабораторная работа')
;

INSERT INTO
	bot.class (id, subject, class_type)
VALUES
	(1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 2, 1), (5, 2, 2),
	(6, 3, 1), (7, 3, 2), (8, 4, 1), (9, 4, 2), (10, 4, 3),
	(11, 5, 1), (12, 5, 2), (13, 6, 1), (14, 6, 2),
	(15, 7, 1), (16, 7, 2), (17, 8, 2), (18, 9, 1), (19, 9, 2)
;

INSERT INTO
	bot.classes_timetable (id, start_time)
VALUES
	(1, '9:30'), (2, '11:20'), (3, '13:10'), (4, '15:25'), (5, '17:15')
;

INSERT INTO
	bot.teacher (id, full_name)
VALUES
	(1, 'Бабердин П.В.'), (2, 'Изотова А.А.'), (3, 'Девайкин И.А.'),
	(4, 'Рывлина А.А.'), (5, 'Артамонова Я.С.'), (6, 'Мальцева С.Н.'),
	(7, 'Горячева Н.Н.'), (8, 'Гематудинов Р.А.'), (9, 'Клешнин Н.Г.'),
	(10, 'Попов А.П.')
;

INSERT INTO
	bot.teacher_class (teacher, class)
VALUES
	-- Бабердин — лекции по вычтеху
	(1, 1),
	-- Изотова — лекции, практики по вычтеху, практики по аиг и вышмату
	(2, 2), (2, 3), (2, 5), (2, 19),
	-- Девайкин — практики по философии
	(3, 7),
	-- Рывлина — лекции и практические по компьютерной графике
	(4, 11), (4, 12),
	-- Артамонова — лекции и практики по социологии
	(5, 13), (5, 14),
	-- Мальцева — лекции и практики по английскому языку
	(6, 15), (6, 16),
	-- Горячева — практики по физической культуре
	(7, 17),
	-- Гематудинов — лекции по ВВИТ
	(8, 8),
	-- Клешнин — практики по ВВИТ
	(9, 9),
	-- Попов А.П. - лекции по философии
	(10, 6)
;

INSERT INTO
	bot.timetable (week, day, class, room_number, class_number)
VALUES
	(0, 1, 1, 518, 2), (0, 1, 3, 520, 3),
	(0, 2, 5, 406, 1), (0, 2, 7, 131, 2), (0, 2, 10, 515, 3), (0, 2, 12, 223, 4),
	(0, 3, 14, 336, 1), (0, 3, 16, 412, 2), (0, 3, 17, 212, 3),
	(0, 4, 8, 344, 4), (0, 4, 9, 456, 5),
	(0, 5, 13, 344, 1), (0, 5, 17, 212, 2), (0, 5, 19, 406, 3), (0, 5, 2, 302, 4)
;

INSERT INTO
	bot.timetable (week, day, class, room_number, class_number)
VALUES
	(1, 1, 11, 511, 1), (1, 1, 17, 212, 2),
	(1, 3, 12, 223, 1), (1, 3, 9, 518, 2), (1, 3, 5, 520, 3), (1, 3, 3, 406, 4),
	(1, 4, 6, 518, 1), (1, 4, 7, 131, 2), (1, 4, 17, 212, 3)
;
