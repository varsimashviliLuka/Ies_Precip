from flask.cli import with_appcontext
import click
import csv
from os import path

from src.extensions import db
from src.models import Stations, WeatherData, User, Role, DivPositions
from src import Config


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Database Created")


@click.command("populate_db")
@with_appcontext
def populate_db():
    stations_csv_file_path = path.join(Config.BASE_DIR, "stations_2024-12-05.csv")
    weather_data_csv_file_path = path.join(Config.BASE_DIR, "weather_data_2024-06-26_2024-06-28.csv")
    station_div_positions_csv_file_path = path.join(Config.BASE_DIR, "station_div_positions.csv")

    click.echo("Adding Stations")
    with open(stations_csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Create a new Station instance for each row
            new_station = Stations(
                station_name=row['station_name'],
                url=row['url'],
                api=row['api'],
                latitude=row['latitude'],
                longitude=row['longitude']
            )
            new_station.create()

    click.echo("Adding Station Div Positions")
    with open(station_div_positions_csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Create a new Station instance for each row
            new_station_div_position = DivPositions(
                station_id=Stations.query.filter_by(api=row['api']).first().id,
                static_px = row['static_px'],
                left_right = row['left_right'],
                line_rotate = row['line_rotate'],
                line_left_right = row['line_left_right'],
                line_top_bottom = row['line_top_bottom'],
                map_status = row['status'],
                shorten_station_name = row['id'],
                top_bottom = row['top_bottom'],
                first_div_height = row['first_div_height'],
                precip_accum = row['PRECIP_ACCUM'],
                precip_rate = row['PRECIP_RATE'],
                precip_accum_long = row['PRECIP_ACCUM_LONG']
            )
            new_station_div_position.create()

    click.echo("Adding Precip Data")
    with open(weather_data_csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Create a new Station instance for each row
            new_precip = WeatherData(
                station_id=row['station_id'],
                precip_rate=row['precip_rate'],
                precip_accum=row['precip_accum'],
                precip_time=row['precip_time']
            )
            new_precip.create()
    
    click.echo("Creating Role")
    role = Role(name="Admin", is_admin=True)
    role.create()
    role = Role(name="User")
    role.create()

    click.echo("Creating User")
    admin_user = User (
        email="luka.varsimashvili@iliauni.edu.ge",
        password="Lukito592",
        role_id=1
    )

    admin_user.create()
    click.echo("Creating User")
    admin_user = User (
        email="roma.grigalashvili@iliauni.edu.ge",
        password="Grigalash27",
        role_id=1
    )
    admin_user.create()

    click.echo("Creating User")
    admin_user = User(
        email="levan.lomidze.5@iliauni.edu.ge",
        password="fantasticfox",
        role_id=1
    )
    admin_user.create()

    click.echo("Frist Tables Created")

@click.command("insert_db")
@with_appcontext
def insert_db():
    # ყველა სადგურის სტატუსს ცვლის True-თი
    # stations = Stations.query.all()
    # for i in stations:
    #     i.status = True
    #     i.save()

    
    pass