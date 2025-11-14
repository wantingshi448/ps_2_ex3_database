"""
NBA Database Analysis Functions
================================

This module provides reusable functions for NBA database analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from typing import Optional, Tuple


def run_query(query: str, connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a DataFrame.

    Parameters:
    -----------
    query : str
        SQL query string
    connection : sqlite3.Connection
        Database connection object

    Returns:
    --------
    pd.DataFrame
        Query results

    Example:
    --------
    >>> result = run_query("SELECT * FROM game LIMIT 5", con)
    """
    try:
        result = pd.read_sql(query, connection)
        print(f"✅ Query executed successfully. Rows returned: {len(result)}")
        return result
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return pd.DataFrame()


def create_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    color: str = "skyblue",
) -> None:
    """
    Create a professional bar chart.

    Parameters:
    -----------
    data : pd.DataFrame
        Data to visualize
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    title : str
        Chart title
    xlabel : str, optional
        X-axis label
    ylabel : str, optional
        Y-axis label
    figsize : tuple, optional
        Figure size (width, height)
    color : str, optional
        Bar color
    """
    plt.figure(figsize=figsize)
    plt.bar(data[x_col], data[y_col], color=color, edgecolor="black")
    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel(xlabel or x_col, fontsize=12)
    plt.ylabel(ylabel or y_col, fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


def get_top_n_teams_by_home_wins(
    connection: sqlite3.Connection, n: int = 10
) -> pd.DataFrame:
    """
    Get top N teams by home wins.

    Parameters:
    -----------
    connection : sqlite3.Connection
        Database connection
    n : int, optional
        Number of teams to return (default: 10)

    Returns:
    --------
    pd.DataFrame
        Top teams with home win counts
    """
    query = f"""
        SELECT
            team_name_home,
            COUNT(*) as home_wins
        FROM game
        WHERE wl_home = 'W'
        GROUP BY team_name_home
        ORDER BY home_wins DESC
        LIMIT {n}
    """
    return run_query(query, connection)


def get_highest_scoring_games(
    connection: sqlite3.Connection, n: int = 1
) -> pd.DataFrame:
    """
    Get highest-scoring games in NBA history.

    Parameters:
    -----------
    connection : sqlite3.Connection
        Database connection
    n : int, optional
        Number of games to return (default: 1)

    Returns:
    --------
    pd.DataFrame
        Highest-scoring games with details
    """
    query = f"""
        SELECT
            game_date,
            team_name_home,
            team_name_away,
            pts_home,
            pts_away,
            (pts_home + pts_away) as total_points,
            wl_home
        FROM game
        WHERE team_name_home NOT LIKE '%All Star%'
          AND team_name_away NOT LIKE '%All Star%'
        ORDER BY total_points DESC
        LIMIT {n}
    """
    return run_query(query, connection)


def analyze_data_quality(df: pd.DataFrame) -> None:
    """
    Print data quality report.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to analyze
    """
    print("=" * 60)
    print("📊 Data Quality Report")
    print("=" * 60)
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn Names:\n{df.columns.tolist()}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nFirst 5 Rows:\n{df.head()}")
    print("=" * 60)
