SELECT movies.title FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id AND people.name = "Johnny Depp" AND movies.title IN(
SELECT movies.title FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id AND  people.name = "Helena Bonham Carter")