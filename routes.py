from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

main_bp = Blueprint('main', __name__)

# root
@main_bp.route('/')
def root():
    return render_template('index.html')