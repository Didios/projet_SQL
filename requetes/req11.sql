SELECT originalTitle
FROM title_basics
JOIN title_ratings ON title_ratings.tconst = title_basics.tconst
WHERE averageRating > 9
AND numVotes > 10000
AND titleType = "movie"