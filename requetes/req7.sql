SELECT originalTitle
FROM title_basics
JOIN title_principals ON title_principals.tconst = title_basics.tconst
JOIN name_basics ON name_basics.nconst = title_principals.nconst
WHERE primaryName = "Olivier Nakache"
AND titleType = "movie"