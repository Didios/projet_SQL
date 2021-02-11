SELECT originalTitle
FROM title_basics
JOIN title_ratings ON title_ratings.tconst = title_basics.tconst
WHERE genres LIKE "%Animation%"
AND numVotes > 1000
AND titleType = "movie"
ORDER BY averageRating DESC
LIMIT 10