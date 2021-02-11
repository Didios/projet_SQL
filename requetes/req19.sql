SELECT primaryName, originalTitle
FROM name_basics, title_basics
JOIN title_principals ON title_principals.tconst = title_basics.tconst
WHERE title_principals.nconst = name_basics.nconst
AND characters LIKE "%James Bond%"
AND category = "actor"
AND titleType = "movie"