SELECT originalTitle
FROM title_basics
JOIN title_akas ON titleId = tconst
WHERE title = "Les dents de la mer"
AND titleType = "movie"