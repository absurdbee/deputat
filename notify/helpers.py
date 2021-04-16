ITEM, SUGGEST_ITEM = "ITE", "SIT"
COMMENT, WOMEN_COMMENT, GROUP_COMMENT = 'COM', 'WCOM', 'GCOM'
REPLY, WOMEN_REPLY, GROUP_REPLY = 'REP', 'WREP', 'GREP'

LIKE, WOMEN_LIKE, GROUP_LIKE = 'LIK', 'WLIK', 'GLIK'
DISLIKE, WOMEN_DISLIKE, GROUP_DISLIKE = 'DIS', 'WDIS', 'GDIS'
INERT, WOMEN_INERT, GROUP_INERT = 'INS', 'WINS', 'GINS'
LIKE_COMMENT, WOMEN_LIKE_COMMENT, GROUP_LIKE_COMMENT =  'LCO', 'WLCO', 'GLCO'
LIKE_REPLY, WOMEN_LIKE_REPLY, GROUP_LIKE_REPLY = 'LRE', 'WLRE', 'GLRE'
SURVEY_VOTE, WOMEN_SURVEY_VOTE, GROUP_SURVEY_VOTE = 'SVO', 'WSVO', 'GSVO'

#'подал заявку в' друзья 'подал заявку в' сообщество - универсальное
CONNECTION_REQUEST, WOMEN_CONNECTION_REQUEST, GROUP_CONNECTION_REQUEST = 'CRE', 'WCRE', 'GCRE'
#'принят в' друзья 'принят в' сообщество - универсальное
CONNECTION_CONFIRMED, WOMEN_CONNECTION_CONFIRMED, GROUP_CONNECTION_CONFIRMED = 'CCO', 'WCCO', 'GCCO'

REGISTER, WOMEN_REGISTER, GROUP_REGISTER = 'REG', 'WREG', 'GREG'

UNREAD, READ, DELETED, CLOSED = 'U', 'R', 'D', 'C'

VERB = (
    (ITEM, ' разместил'),
    (COMMENT, ' оставил комментарий'), (WOMEN_COMMENT, ' оставила комментарий'), (GROUP_COMMENT, ' оставили комментарий'),
    (REPLY, ' ответил на'), (WOMEN_REPLY, ' ответила на'), (GROUP_REPLY, ' ответили на'),

    (LIKE, ' оценил'), (WOMEN_LIKE, ' оценила'), (GROUP_LIKE, ' оценили'),
    (DISLIKE, ' не оценил'), (WOMEN_DISLIKE, ' не оценила'), (GROUP_DISLIKE, ' не оценили'),
    (INERT, ' считает, что'), (WOMEN_INERT, ' считает, что'), (GROUP_INERT, ' считает, что'),
    (LIKE_COMMENT, ' оценил'), (WOMEN_LIKE_COMMENT, ' оценила '), (GROUP_LIKE_COMMENT, ' оценили'),
    (LIKE_REPLY, ' оценил'), (WOMEN_LIKE_REPLY, ' оценила'), (GROUP_LIKE_REPLY, ' оценили'),
    (SURVEY_VOTE, ' участвовал в опросе'), (WOMEN_SURVEY_VOTE, ' участвовала в опросе'), (GROUP_SURVEY_VOTE, ' участвовали в опросе'),

    (CONNECTION_REQUEST, ' подал заявку в'), (WOMEN_CONNECTION_REQUEST, ' подала заявку в'), (GROUP_CONNECTION_REQUEST, ' подали заявку в'),
    (CONNECTION_CONFIRMED, ' принят в'), (WOMEN_CONNECTION_CONFIRMED, ' принята'), (GROUP_CONNECTION_CONFIRMED, ' приняты'),

    (REGISTER, ' зарегистрировался'), (WOMEN_REGISTER, ' зарегистрировалась'), (GROUP_REGISTER, ' зарегистрировались'),
)

STATUS = ((UNREAD, 'Не прочитано'),(READ, 'Прочитано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто'),)
