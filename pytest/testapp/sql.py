create_testapp_resultview = """CREATE OR REPLACE VIEW testapp_resultview AS 
SELECT game.id,
game.start_on,
game.stop_on,
game.player_id,
game.state,
game.number_of_right_answers,
test.test_id,
test.test_name,
test.test_published,
test.test_author,
test.test_description,
test.test_interval,
test.number_of_questions
FROM ( SELECT game_1.id,
        game_1.start_on,
        game_1.stop_on,
        game_1.player_id,
        game_1.test_id,
        game_1.state,
        COALESCE(gq.number_of_right_answers, 0::bigint) AS number_of_right_answers
        FROM ( SELECT DISTINCT ON (testapp_game.player_id, testapp_game.test_id) testapp_game.id,
                testapp_game.start_on,
                testapp_game.stop_on,
                testapp_game.player_id,
                testapp_game.test_id,
                testapp_game.state
                FROM testapp_game
                WHERE testapp_game.state::text = 'C'::text
                ORDER BY testapp_game.player_id, testapp_game.test_id, testapp_game.start_on DESC) game_1
            LEFT JOIN ( SELECT testapp_gamequestion.game_id,
                count(*) AS number_of_right_answers
                FROM testapp_gamequestion
                WHERE testapp_gamequestion.player_answer::text = testapp_gamequestion.right_answer::text AND testapp_gamequestion.right_answer::text <> ''::text
                GROUP BY testapp_gamequestion.game_id) gq ON game_1.id = gq.game_id) game
    JOIN ( SELECT t.id AS test_id,
        t.name AS test_name,
        t.published AS test_published,
        t.author AS test_author,
        t.description AS test_description,
        t."interval" AS test_interval,
        count(tq.question_id) AS number_of_questions
        FROM testapp_test t
            LEFT JOIN testapp_testquestion tq ON t.id = tq.test_id
        WHERE t.published = true
        GROUP BY t.id) test ON test.test_id = game.test_id;
"""