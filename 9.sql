SELECT name FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id AND movies.year = 2012
ORDER BY people.birth