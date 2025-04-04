import pytest
from model import Question

@pytest.fixture
def data():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    return question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_empty_title():
    with pytest.raises(Exception):
        Question(title='', points=1)

def test_create_question_with_invalid_points():
     with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice_with_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)

def test_create_choice_with_long_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a'*101, False)

def test_remove_choice_by_id(data):
    data.remove_choice_by_id(data.choices[0].id)

    assert len(data.choices) == 1
    assert data.choices[0].text == 'b'

def test_remove_choice_with_inalid_id(data):
    with pytest.raises(Exception):
        data.remove_choice_by_id('invalid_id')

def test_remove_all_choices(data):
    data.remove_all_choices()

    assert len(data.choices) == 0

def test_select_choices(data):
    selected_choices = data.select_choices([data.choices[1].id])
    assert len(selected_choices) == 1
    assert selected_choices[0] == data.choices[1].id

def test_select_choice_out_of_range(data):
    with pytest.raises(Exception):
        data.select_choices([data.choices[0].id, data.choices[1].id])

def test_set_correct_choice(data):
    data.set_correct_choices([data.choices[0].id])

    assert data.choices[1].is_correct == True
    assert data.choices[0].is_correct == True

def test_set_all_choices_as_correct(data):
    data.set_correct_choices([choice.id for choice in data.choices])

    assert all(choice.is_correct for choice in data.choices)

def test_set_correct_choice_with_invalid_id(data):
    with pytest.raises(Exception):
        data.set_correct_choices(['invalid_id'])