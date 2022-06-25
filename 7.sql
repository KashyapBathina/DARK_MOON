SELECT ratings.rating, movies.title FROM movies
JOIN ratings on ratings.movie_id = movies.id
WHERE year = 2010
ORDER BY rating DESC, title;