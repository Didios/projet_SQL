SELECT primaryTitle
FROM title_basics
WHERE titleType = "movie"
ORDER BY runtimeMinutes
DESC
LIMIT 1