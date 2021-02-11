SELECT primaryTitle
FROM title_basics
JOIN title_episode ON title_episode.tconst = title_basics.tconst
WHERE parentTconst IN(SELECT title_basics.tconst
					FROM title_basics
					WHERE primaryTitle = "Game of Thrones"
					AND titleType = "tvSeries")