import click
from PyInquirer import prompt
from .lessons import lessons, welcome_message

@click.command()
@click.pass_context
def lesson(ctx):
    """ 
    Gitutor lessons right on your terminal !
    """
    click.echo(welcome_message)
    selection = prompt_for_lesson()
    if selection:
        lesson_name = extract_lesson_name(selection['lesson'])
        click.echo(lessons[lesson_name]['content'])


def create_choices_from_lessons():
    return [f'{lesson} - {lessons[lesson]["description"]}' for lesson in lessons]

def extract_lesson_name(selection):
    if selection:
        return selection.split('-')[0].strip()

def prompt_for_lesson():
    message = 'Select a lesson!'
    choices = create_choices_from_lessons()
    question = [
        {
            'type': 'list',
            'message': message,
            'name': 'lesson',
            'choices': choices
        }
    ]
    return prompt(question)