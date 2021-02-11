SELECT originalTitle
FROM title_basics
JOIN title_ratings ON title_ratings.tconst = title_basics.tconst
WHERE titleType = "movie"
ORDER BY numVotes DESC
LIMIT 1