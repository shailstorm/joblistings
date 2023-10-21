from flask import render_template, request
from app import jobapp
from app import filters


@jobapp.route('/')
@jobapp.route('/home')
def home():
    return render_template('home.html',
                           listings=filters.getListings(),
                           filters=filters.getFilters()
                           )