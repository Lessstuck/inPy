 SELECT title FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE id IN
 (SELECT  movie_id FROM ratings WHERE movie_id IN
 (SELECT movie_id FROM stars JOIN people ON stars.person_id = people.id  WHERE id =
 (SELECT id FROM people WHERE name = "Chadwick Boseman"))  )   ORDER BY rating DESC LIMIT 5;