SELECT originalTitle
FROM title_basics
JOIN name_titles ON knownForTitles = tconst
JOIN name_basics ON name_basics.nconst = name_titles.nconst
WHERE primaryName = "Sean Connery"
AND titleType = "movie"