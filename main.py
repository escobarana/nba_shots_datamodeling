import logging
import os

from dotenv import load_dotenv

from helpers.db import Database
from helpers.utils import (
    create_table_queries,
    drop_table_queries,
    generate_dataframes,
    insert_queries_mapping,
    insert_table_queries,
    join_teams_data,
)

logger = logging.getLogger(__name__)

path_to_csv_lj = "data/1_lebron_james_shot_chart_1_2023.csv"
path_to_csv_jh = "data/2_james_harden_shot_chart_1_2023.csv"
path_to_csv_sc = "data/3_stephen_curry_shot_chart_2023.csv"


def drop_database(db: Database):
    """
    Drops a database
    :param db: database object
    :return: None
    """
    db.drop_database("nba")


def drop_tables(db: Database, tables: list):
    """
    Drops tables in the database
    :param db: database object
    :param tables: list of tables to drop
    :return: None
    """
    db.drop_tables(drop_table_queries=drop_table_queries(tables))


def main():
    load_dotenv()
    logging.info("Reading LeBron James data...")
    shot_data_lj, player_data_lj, team_data_lj = generate_dataframes(
        path_to_csv_lj, player_id=1, team="LAL", player="LeBron James"
    )
    logging.info("Reading James Harden data...")
    shot_data_jh, player_data_jh, team_data_jh = generate_dataframes(
        path_to_csv_lj, player_id=2, team="BKN", player="James Harden"
    )
    logging.info("Reading Stephen Curry data...")
    shot_data_sc, player_data_sc, team_data_sc = generate_dataframes(
        path_to_csv_lj, player_id=3, team="GSW", player="Stephen Curry"
    )

    all_teams = join_teams_data(team_data_lj, team_data_jh, team_data_sc)

    logging.info("Connecting to database...")
    db = Database(
        "postgres",
        "localhost",
        os.environ.get("POSTGRES_USERNAME"),
        os.environ.get("POSTGRES_PASSWORD"),
    )

    logging.info("Creating new nba database...")
    db.create_database("nba")

    logging.info("Creating tables in nba database...")
    db.create_tables(create_table_queries=create_table_queries())

    logging.info("Inserting team data in the tables...")
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["team"]], data=all_teams
    )

    logging.info("Inserting player data in the tables...")
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["player"]],
        data=player_data_lj,
    )
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["player"]],
        data=player_data_jh,
    )
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["player"]],
        data=player_data_sc,
    )

    logging.info("Inserting shot data in the tables...")
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["shot"]], data=shot_data_lj
    )
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["shot"]], data=shot_data_jh
    )
    db.insert_data(
        query=insert_table_queries()[insert_queries_mapping["shot"]], data=shot_data_sc
    )

    logging.info("Closing connection to the database...")
    db.close_connection()

    logging.info("Done!")


if __name__ == "__main__":
    main()
