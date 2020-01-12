"""
Copyright (c) 2019 paint-it

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import click  # Used for command line interface
import diceware  # Used for creating password
from genpass.database import DatabaseConnection
import random

db_obj = DatabaseConnection()


@click.command(help="Get secrete key")
def secretekey():
    """Used to provide secrete to user to see saved passwords"""
    secrete_key = random.randint(1111, 9999)
    email = click.prompt("Enter Email ID")
    db_obj.secrete_table()
    exist_key = db_obj.get_key(email)
    if exist_key is None:
        db_obj.add_key(email=email, key=secrete_key)

    key = db_obj.get_key(email)
    click.echo(f"This is your secrete key: {key}. Please do not share with anyone!!!")


@click.command(help="Show Version")
def version():
    click.echo("Genpass v0.1")


@click.command(help="Delete password")
def delpass():
    """used to delete existing password"""
    portal_name = click.prompt("Enter portal name", default="None")
    db_obj.delete_data(portal_name=portal_name)


@click.command(help="Update password")
def modpass():
    """Update existing password"""
    portal_name = click.prompt("Enter portal name", default="None")
    mod = click.prompt("Enter new password", default="None", hide_input=True)
    db_obj.update_data(portal_name=portal_name, password=mod)


@click.command(help="Save existing passwords")
def savepass():
    """Used to take portal name and password from user"""
    portal_name = click.prompt("Enter portal name", default="None")
    pwd = click.prompt("Enter your password", default="None", hide_input=True)
    attach_key = db_obj.whole_key()
    db_obj.create_table()
    db_obj.insert_data(portal_name=portal_name, password=pwd, key=attach_key)


@click.command(help="Create new password")
def createpass():
    """Used for taking input from user to create password"""
    portal_name = click.prompt("Enter portal name", default="None")
    password = diceware.get_passphrase()
    attach_key = db_obj.whole_key()
    db_obj.create_table()
    db_obj.insert_data(portal_name=portal_name, password=password, key=attach_key)


@click.command(help="Show password")
def showpass():
    flag = 0
    portal_name = click.prompt("Enter portal name", default="None")
    while flag < 3:
        key = click.prompt("Enter secrete key", hide_input=True)
        spass = db_obj.show_data(portal_name, key)
        if spass is None:
            flag = flag + 1
            click.echo("Invalid secrete key or portal name. Please try again!!!")
        else:
            click.echo(spass)
            exit()
