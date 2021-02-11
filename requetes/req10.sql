SELECT primaryName, category, job 
FROM name_basics, title_principals, title_basics
WHERE name_basics.nconst = title_principals.nconst
AND title_principals.tconst = title_basics.tconst
AND primaryTitle LIKE "%Return of the Jedi%"
AND titleType = "movie"