SELECT originalTitle
FROM title_basics
WHERE titleType = "movie"
ORDER BY runtimeMinutes DESC
LIMIT 5