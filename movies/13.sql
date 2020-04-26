SELECT DISTINCT name FROM people JOIN stars ON people.id = stars.person_id WHERE person_id IN
(SELECT DISTINCT person_id FROM stars WHERE (movie_id IN
(SELECT movie_id FROM stars WHERE person_id IN
(SELECT id FROM people WHERE name = "Kevin Bacon" AND birth= 1958))
AND person_id IS NOT
(SELECT id FROM people WHERE name = "Kevin Bacon" AND birth= 1958))) ORDER BY name ASC;