from datetime import datetime
from sqlalchemy import cast, Date
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, AnyOf, URL, InputRequired, optional
from enums import State, Genre
from models import Show, Artist


class ValidateValues(object):
    """
    Compares the values of the fields to an enum.

    :param values:
        enum of values to compair to.
    :param message:
        Error message to raise in case of a validation error.
    """

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


class Available:
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the artist id field to check availability.
    :param past_message:
        Error message to raise in case if the show is in the past.
    :param booked_message:
        Error message to raise in case if the artist is booked at the specified date.
    :param unavailable_message:
    Error message to raise in case if the artist is unavailable at the specified date.
    """

    def __init__(self, fieldname, past_message=None, booked_message=None, unavailable_message=None):
        self.fieldname = fieldname
        self.past_message = past_message
        self.booked_message = booked_message
        self.unavailable_message = unavailable_message

    def __call__(self, form, field):
        try:
            id = form[self.fieldname]
        except KeyError:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            )
        if field.data < datetime.now():
            message = self.past_message
            if message is None:
                message = 'The date you specified is in the past.'
            raise ValidationError(message)
        show = Show.query.filter(
            Show.artist_id == id.data).filter(cast(Show.start_time, Date) == field.data.date()).first()
        if show:
            message = self.booked_message
            if message is None:
                message = f'{show.artist.name} is already booked on the specified date'
            raise ValidationError(message)
        artist = Artist.query.get(id.data)
        date, str = artist.availableOn(field.data)
        if not date:
            message = self.unavailable_message
            if message is None:
                message = f'{artist.name} is not available on {str}s.'
            raise ValidationError(message)


class ShowForm(Form):
    artist_id = SelectField('Select artist', coerce=int, validators=[
                            InputRequired(message='Please choose the artist')])
    venue_id = SelectField('Select venue', coerce=int, validators=[
                           InputRequired(message='Please choose the venue')])
    start_time = DateTimeField(
        'Start time',
        validators=[DataRequired(), Available('artist_id')],
        default=datetime.now()
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
