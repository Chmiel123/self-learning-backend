do $$
declare
	lang_id integer;
begin
	lang_id := (SELECT id FROM system.language WHERE code = 'en');
	INSERT INTO content.category
	    (name, content, nr_courses, language_id, created_date)
	VALUES
		('Maths', 'Maths is the queen of all sciences.', 0, lang_id, '2012-12-07'),
		('Geography', 'Learn all the countries and capitals.', 0, lang_id, '2012-12-07'),
		('Chemistry', 'Be careful not to blow anything up.', 0, lang_id, '2012-12-07'),
		('Biology', 'All the squishy parts.', 0, lang_id, '2012-12-07');
end $$;