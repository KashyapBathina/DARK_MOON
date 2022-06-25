SELECT AVG(rating) FROM ratings
JOIN movies ON ratings.movie_id = movies.id AND movies.year = 2012;

--when year = 2012
--and when its movieid matches the ratingsid
--selects the average rating