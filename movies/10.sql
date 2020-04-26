SELECT name FROM people WHERE id IN (SELECT DISTINCT	 person_id FROM directors JOIN ratings ON directors.movie_id = ratings.movie_id WHERE ratings.movie_id IN (SELECT movie_id FROM ratings WHERE rating >= 9));