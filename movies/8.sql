SELECT DISTINCT name FROM people JOIN stars ON people.id = stars.person_id
WHERE id IN (SELECT person_id from stars WHERE movie_id = (SELECT id FROM movies WHERE title = "Toy Story"));