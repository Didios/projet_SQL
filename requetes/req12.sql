SELECT originalTitle
FROM title_basics
JOIN title_ratings ON title_ratings.tconst = title_basics.tconst
WHERE genres LIKE "%Romance%"
AND genres LIKE "%Comedy%"
ORDER BY averageRating DESC
LIMIT 5