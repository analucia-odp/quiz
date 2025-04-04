import pytest
from model import Question


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

def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.remove_choice_by_id(question.choices[0].id)

    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

def test_remove_choice_by_id_not_found():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    with pytest.raises(Exception):
        question.remove_choice_by_id('invalid_id')

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.remove_all_choices()

    assert len(question.choices) == 0

def test_select_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    selected_choices = question.select_choices([question.choices[1].id])
    assert len(selected_choices) == 1
    assert selected_choices[0] == question.choices[1].id

def test_select_choice_out_of_range():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', False)
    question.add_choice('b', True)

    with pytest.raises(Exception):
        question.select_choices([question.choices[0].id, question.choices[1].id])

def test_set_correct_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)

    question.set_correct_choices([question.choices[1].id])

    assert question.choices[1].is_correct == True
    assert question.choices[0].is_correct == False
