import pandas as pd

insert_queries_mapping = {"team": 0, "player": 1, "shot": 2}


def get_data_from_csv(csv_file_path: str, columns: list) -> pd.DataFrame:
    """
    :param csv_file_path: path to csv file
    :param columns: list of columns to keep
    :return: pandas dataframe
    """
    df = pd.read_csv(csv_file_path)
    df = df[columns]
    return df.drop_duplicates()


def generate_dataframes(
    csv_file_path: str, player_id: int, team: str, player: str
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    :param csv_file_path: path to csv file
    :param player_id: player id to add to shot data
    :param team: team name to add to team data
    :param player: player name to add to player data
    :return: three pandas dataframes containing shot, player and team data
    """
    shot_data = get_data_from_csv(
        csv_file_path,
        [
            "top",
            "left",
            "date",
            "shot_type",
            "distance_ft",
            "result",
            "color",
            "qtr",
            "time_remaining",
            "season",
        ],
    )
    shot_data["player_id"] = player_id
    player_data = pd.DataFrame({"team_name": [team], "player_name": [player]})
    team_data = (
        get_data_from_csv(csv_file_path, ["opponent"])
        .rename(columns={"opponent": "team_name"})
        ._append({"team_name": team}, ignore_index=True)
    )

    return shot_data, player_data, team_data


def join_teams_data(
    team_data_lj: pd.DataFrame, team_data_jh: pd.DataFrame, team_data_sc: pd.DataFrame
) -> pd.DataFrame:
    """
    :param team_data_lj: team data for LeBron James
    :param team_data_jh: team data for James Harden
    :param team_data_sc: team data for Stephen Curry
    :return: pandas dataframe containing all team data
    """
    return (
        team_data_lj._append(team_data_jh, ignore_index=True)
        ._append(team_data_sc, ignore_index=True)
        .drop_duplicates()
    )


def create_table_queries():
    """
    Important to follow the order of tables in this list since there are foreign key constraints
    :return: list of queries to create tables
    """
    queries = [
        """
        CREATE TABLE IF NOT EXISTS team (
            team_name VARCHAR(50) PRIMARY KEY
        );
        """
        """
        CREATE TABLE IF NOT EXISTS player (
            player_id SERIAL PRIMARY KEY,
            team_name VARCHAR(3) REFERENCES team (team_name),
            player_name VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS shot (
            shot_id SERIAL PRIMARY KEY,
            player_id INT REFERENCES player (player_id),
            top INT,
            "left" INT,
            date VARCHAR(20),
            shot_type INT,
            distance_ft INT,
            result BOOLEAN,
            color VARCHAR(5),
            qtr VARCHAR(10),
            time_remaining VARCHAR(5),
            season INT
        );
        """,
    ]

    return queries


def insert_table_queries():
    """
    Important to follow the order of tables in this list since there are foreign key constraints
    :return: list of queries to insert data into tables
    """
    queries = [
        """
        INSERT INTO team (team_name) VALUES (%s);
        """,
        """
        INSERT INTO player (team_name, player_name) VALUES (%s, %s);
        """,
        """
        INSERT INTO shot (top, "left", date, shot_type, distance_ft, result, color, qtr, time_remaining, season, player_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
    ]

    return queries


def drop_table_queries(tables: list):
    """
    :param tables: list of tables to drop
    :return: list of queries to drop tables
    """
    queries = [
        """
        DROP TABLE IF EXISTS {};
        """.format(
            table
        )
        for table in tables
    ]

    return queries
