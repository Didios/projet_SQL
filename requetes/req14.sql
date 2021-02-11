SELECT COUNT(originalTitle)
FROM title_basics
WHERE runtimeMinutes > 3 * 60
AND titleType = "movie"