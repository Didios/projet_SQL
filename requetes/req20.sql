SELECT primaryName, primaryTitle
FROM name_basics, title_basics, name_titles, title_ratings
WHERE name_basics.nconst = name_titles.nconst
AND knownForTitles = title_basics.tconst
AND title_basics.tconst = title_ratings.tconst
AND titleType = "movie"
AND primaryProfession LIKE "%director%"
ORDER BY averageRating DESC
LIMIT 5