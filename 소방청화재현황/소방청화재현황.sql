-- CREATE TABLE fire (
-- 	인명피해 INTEGER,
-- 	사망 INTEGER,
-- 	부상 INTEGER,
-- 	재산피해소계 INTEGER NOT NULL,
-- 	접수일시 TEXT NOT NULL PRIMARY KEY,
-- 	발화층 INTEGER,
-- 	화재유형 INTEGER,
-- 	발화요인대분류 TEXT,
-- 	발화요인소분류 TEXT
-- );

-- CREATE TABLE 온습도 (
-- 	접수일시 TEXT NOT NULL PRIMARY KEY,
-- 	온도 REAL,
-- 	습도 REAL
-- );

-- CREATE TABLE 풍속향 (
-- 	접수일시 TEXT NOT NULL PRIMARY KEY,
-- 	풍속 REAL,
-- 	풍향 REAL
-- );

-- DROP TABLE fire

SELECT 풍속, count(*) FROM 풍속향
GROUP BY 풍속;

SELECT *, count(*) FROM 온습도
GROUP BY 온도, 습도;