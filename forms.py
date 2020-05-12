from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, AnyOf, URL, InputRequired, optional
from enums import State, Genre


class ValidateValues(object):
    def __init__(self, values, message=None):
        self.values = values
        if not message:
            message = u'Values must be one of: {0}.'.format(
                ','.join(self.values))
        self.message = message

    def __call__(self, form, field):
        error = False
        for value in field.data:
            if value not in self.values:
                error = True
        if error:
            raise ValidationError(self.message)


ValidateValues = ValidateValues


class ShowForm(Form):
    artist_id = SelectField('Select artist', coerce=int, validators=[
                            InputRequired(message='Please choose the artist')])
    venue_id = SelectField('Select venue', coerce=int, validators=[
                           InputRequired(message='Please choose the venue')])
    start_time = DateTimeField(
        'Start time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'Venue name', validators=[DataRequired(message='Please enter a venue name'), Length(min=2, max=50)]
    )
    city = StringField(
        'City', validators=[DataRequired('Please enter the venue\'s city'), Length(min=2, max=50)]
    )
    state = SelectField(
        'State', validators=[DataRequired(message='Please select the venue\'s state'), Length(min=2, max=50), AnyOf([choice.value for choice in State])],
        choices=State.choices()
    )
    address = StringField(
        'Address', validators=[DataRequired(message='Please enter the venue\'s address'), Length(min=10, max=120)]
    )
    phone = StringField(
        'Phone Number'
    )
    image_link = StringField(
        'Image link'
    )
    genres = SelectMultipleField(
        'Genres', validators=[DataRequired(), Length(max=150), ValidateValues([choice.value for choice in Genre])],
        choices=Genre.choices()
    )
    website = StringField(
        'Website', validators=[optional(strip_whitespace=False), URL(message='Please enter a valid URL'), Length(min=10, max=120)]
    )
    facebook_link = StringField(
        'Facebook link', validators=[optional(strip_whitespace=False), URL(message='Please enter a valid URL'), Length(min=15, max=120)]
    )
    seeking_talent = BooleanField(
        'Looking for artists'
    )
    seeking_description = TextAreaField(
        'Description for artists', validators=[Length(max=500)]
    )


class ArtistForm(Form):
    name = StringField(
        'Artist name', validators=[DataRequired(message='Please enter an artist name'), Length(min=2, max=50)]
    )
    city = StringField(
        'City', validators=[DataRequired('Please enter the artist\'s city'), Length(min=2, max=50)]
    )
    state = SelectField(
        'State', validators=[DataRequired(message='Please select the artist\'s state'), Length(min=2, max=50), AnyOf([choice.value for choice in State])],
        choices=State.choices()
    )
    phone = StringField(
        'Phone Number'
    )
    image_link = StringField(
        'Image link'
    )
    genres = SelectMultipleField(
        'Genres', validators=[DataRequired(), Length(max=150), ValidateValues([choice.value for choice in Genre])],
        choices=Genre.choices()
    )
    website = StringField(
        'Website', validators=[optional(strip_whitespace=False), URL(message='Please enter a valid URL'), Length(min=10, max=120)]
    )
    facebook_link = StringField(
        'Facebook link', validators=[optional(strip_whitespace=False), URL(message='Please enter a valid URL'), Length(min=15, max=120)]
    )
    seeking_venue = BooleanField(
        'Available to Venues'
    )
    seeking_description = TextAreaField(
        'Description for venues', validators=[Length(max=500)]
    )
    monday = BooleanField(
        'Monday', default='checked'
    )
    tuesday = BooleanField(
        'Tuesday', default='checked'
    )
    wednesday = BooleanField(
        'Wednesday', default='checked'
    )
    thursday = BooleanField(
        'Thursday', default='checked'
    )
    friday = BooleanField(
        'Friday', default='checked'
    )
    saturday = BooleanField(
        'Saturday', default='checked'
    )
    sunday = BooleanField(
        'Sunday', default='checked'
    )
