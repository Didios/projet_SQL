SELECT primaryName
FROM name_basics
JOIN title_principals ON title_principals.nconst = name_basics.nconst
JOIN title_basics ON title_basics.tconst = title_principals.tconst
WHERE category = "writer"
AND job = "scenario"
AND originalTitle = "Taxi"
AND startYear = 1998
AND titleType = "movie"