req1.sql
#01.Quels sont les differents types de titres dans cette base de donnees ?
SELECT
DISTINCT(titleType)
FROM title_basics

req2.sql
#02.Combien y a-t-il de titres dans cette base de donnees ?
SELECT
COUNT(primaryTitle)
FROM title_basics

req3.sql
#03.En quelle annee est sortie le film The Godfather  ?
SELECT startYear
FROM title_basics
WHERE originalTitle = "The Godfather"
AND titleType = "movie"

req4.sql
#04.En quelle annee est sortie le premier film Superman ?
SELECT
MIN(startYear)
FROM title_basics
WHERE originalTitle = "Superman"
AND titleType = "movie"

req5.sql
#05.Quel est le titre original du film  Les dents de la mer  ?
SELECT originalTitle
FROM title_basics
JOIN title_akas 
ON titleId = tconst 
WHERE title = "Les dents de la mer"
AND titleType = "movie"

req6.sql
#06.Quel est le metier d Olivier Nakache ?
SELECT primaryProfession
FROM name_basics
WHERE primaryName = "Olivier Nakache"

req7.sql
#07.Quels sont les films d Olivier Nakache ?
SELECT originalTitle
FROM title_basics
JOIN title_principals 
ON title_principals.tconst = title_basics.tconst 
JOIN name_basics 
ON name_basics.nconst = title_principals.nconst 
WHERE primaryName = "Olivier Nakache"
AND titleType = "movie"

req8.sql
#08.Quel est le film ayant recueilli le plus de votes ?
SELECT originalTitle
FROM title_basics
JOIN title_ratings 
ON title_ratings.tconst = title_basics.tconst 
WHERE titleType = "movie"
ORDER BY numVotes 
DESC
LIMIT 1

req9.sql
#09.Qui a ecrit le scenario du film Taxi sorti en 1998 ?
SELECT primaryName
FROM name_basics
JOIN title_principals 
ON title_principals.nconst = name_basics.nconst 
JOIN title_basics 
ON title_basics.tconst = title_principals.tconst 
WHERE category = "writer"
AND job = "scenario"
AND originalTitle = "Taxi"
AND startYear = 1998
AND titleType = "movie"

req10.sql
#10.Quelles sont les noms et roles (category et job) des personnes intervenant dans la production du film Return of the Jedi ?
SELECT primaryName, category, job 
FROM name_basics, title_principals, title_basics
WHERE name_basics.nconst = title_principals.nconst 
AND title_principals.tconst = title_basics.tconst 
AND primaryTitle 
LIKE "%Return of the Jedi%"
AND titleType = "movie"

req11.sql
#11.Quels sont les titres des films notes plus de 9 sur 10 avec plus de 10 000 votes ?
SELECT originalTitle
FROM title_basics
JOIN title_ratings 
ON title_ratings.tconst = title_basics.tconst 
WHERE averageRating > 9
AND numVotes > 10000
AND titleType = "movie"

req12.sql
#12.Quelle sont les 5 comedies romantiques les mieux notees ?
SELECT originalTitle
FROM title_basics
JOIN title_ratings 
ON title_ratings.tconst = title_basics.tconst 
WHERE genres 
LIKE "%Romance%"
AND genres 
LIKE "%Comedy%"
ORDER BY averageRating 
DESC
LIMIT 5

req13.sql
#13.Quels sont les 10 films d animation ayant recu plus de 1000 votes les mieux notes ?
SELECT originalTitle
FROM title_basics
JOIN title_ratings 
ON title_ratings.tconst = title_basics.tconst 
WHERE genres 
LIKE "%Animation%"
AND numVotes > 1000
AND titleType = "movie"
ORDER BY averageRating 
DESC
LIMIT 10

req14.sql
#14.Combien de films durent plus de 3 heures ?
SELECT
COUNT(originalTitle)
FROM title_basics
WHERE runtimeMinutes > 3 * 60
AND titleType = "movie"

req15.sql
#15.Quelle est la duree moyenne d un film ?
SELECT
AVG(runtimeMinutes)
FROM title_basics
WHERE titleType = "movie"

req16.sql
#16.Quel est le film le plus long ?
SELECT primaryTitle
FROM title_basics
WHERE titleType = "movie"
ORDER BY runtimeMinutes
DESC
LIMIT 1

req17.sql
#17.Quels sont les 5 films les plus longs ?
SELECT originalTitle
FROM title_basics
WHERE titleType = "movie"
ORDER BY runtimeMinutes 
DESC
LIMIT 5

req18.sql
#18.Quels sont les titres des films les plus connus de Sean Connery ?
SELECT originalTitle
FROM title_basics
JOIN name_titles 
ON knownForTitles = tconst 
JOIN name_basics 
ON name_basics.nconst = name_titles.nconst 
WHERE primaryName = "Sean Connery"
AND titleType = "movie"

req19.sql
#19.Quels sont les acteurs ayant joue le role de James Bond, et dans quels films ?
SELECT primaryName, originalTitle
FROM name_basics, title_basics
JOIN title_principals 
ON title_principals.tconst = title_basics.tconst 
WHERE title_principals.nconst = name_basics.nconst 
AND characters 
LIKE "%James Bond%"
AND category = "actor"
AND titleType = "movie"

req20.sql
#20.Quel sont les realisateurs ayant fait les cinq film les mieux notes ? Indiquer les noms des films correspondants.  
SELECT primaryName, primaryTitle
FROM name_basics, title_basics
JOIN title_principals 
ON title_principals.nconst = name_basics.nconst
WHERE title_principals.tconst = title_basics.tconst
AND category = "director"
AND title_basics.tconst IN(SELECT title_basics.tconst
					FROM title_basics
					JOIN title_ratings 
					ON title_ratings.tconst = title_basics.tconst
					WHERE titleType = "movie"
					ORDER BY averageRating 
					DESC
					LIMIT 5)

req21.sql
#21.Quels sont les noms des episodes de Game of Thrones ?
SELECT primaryTitle
FROM title_basics
JOIN title_episode 
ON title_episode.tconst = title_basics.tconst 
WHERE parenttconst 
IN(SELECT title_basics.tconst 
	FROM title_basics
	WHERE primaryTitle = "Game of Thrones"
	AND titleType = "tvSeries")