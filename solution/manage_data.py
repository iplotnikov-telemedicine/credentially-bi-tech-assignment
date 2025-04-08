"""
Load the data files into DuckDB.

The files have been downloaded from the Google Drive and placed in '/solution/data' folder
"""

import pandas as pd
import duckdb
import os


def load_data():

    path = os.path.join(os.path.dirname(__file__), 'data')
    df_ref_assigned_to = pd.read_csv(os.path.join(path, 'ref_assigned_to.csv'))
    df_ref_job_positions = pd.read_csv(os.path.join(path, 'ref_job_positions.csv'))
    df_ref_references = pd.read_csv(os.path.join(path, 'ref_references.csv'))
    df_ref_user_tags = pd.read_csv(os.path.join(path, 'ref_user_tags.csv'))

    db = duckdb.connect()
    db.register('ref_assigned_to', df_ref_assigned_to)
    db.register('ref_job_positions', df_ref_job_positions)
    db.register('ref_references', df_ref_references)
    db.register('ref_user_tags', df_ref_user_tags)

    # Add a date table running from 2018-11-29 to 2025-03-20
    dates = pd.date_range('2018-11-29', periods=2303, freq='D')
    dateframe = pd.DataFrame(dates.date, columns=['date'])

    db.register("dates", dateframe)

    return db


def create_view(conn):
    """
    Create a View of data which allows for multiple data summaries to be run against it
    All the data for the Dashboard will be stored in a single view, the 'one-big-table' approach
    :param conn: DuckDB connection
    :return:

    """
    query = """
    CREATE VIEW wide_table AS
    SELECT  
        r.completed_to_reviewed_days,
        r.completed_to_reviewed_time,
        r.cr_created_at,
        r.job_position_id,
        r.marked_compliant_at,
        r.ref_approval_status,
        r.ref_approved_at,
        r.ref_approved_date,
        r.ref_completed_at,
        r.ref_completed_date,
        r.ref_requested_at,
        r.ref_requested_date,
        r.ref_status,
        r.requested_to_completed_days,
        r.requested_to_completed_time,
        r.requested_to_compliant_time,
        r.requested_to_reviewed_time,
        r.is_mandatory,
        r.ref_package_name,
        r.ref_form_name,
        jp.role,
        jp.job_position_status,
        jp.signed_off,
        ut.tag,
        at.assigned_to
    FROM 
        ref_references r
    LEFT JOIN ref_job_positions jp 
        ON r.job_position_id = jp.job_position_id

    -- Filtering logic references ref_user_tags and ref_assigned_to
    LEFT JOIN ref_user_tags ut 
        ON ut.job_position_id = jp.job_position_id

    LEFT JOIN ref_assigned_to at 
        ON at.job_position_id = jp.job_position_id
    """

    conn.execute(query)


def references_handled_by_day(conn) -> pd.DataFrame:
    sql = """
        SELECT d.date, SUM(CASE WHEN wt.ref_status IS NOT NULL THEN 1 ELSE 0 END ) request_count
        FROM dates d
        LEFT JOIN wide_table wt ON d.date = wt.ref_requested_date
        WHERE wt.ref_status = 'SENT' OR wt.ref_status IS NULL
        GROUP BY date
        ORDER BY date
    """

    return conn.execute(sql).fetchdf()


def references_handled_by_month(conn) -> pd.DataFrame:
    sql = """
        SELECT DATE_TRUNC('month', d.date) m, SUM(CASE WHEN wt.ref_status IS NOT NULL THEN 1 ELSE 0 END ) request_count
        FROM dates d
        LEFT JOIN wide_table wt ON d.date = wt.ref_requested_date
        WHERE wt.ref_status = 'SENT' OR wt.ref_status IS NULL
        GROUP BY DATE_TRUNC('month', d.date)
        ORDER BY DATE_TRUNC('month', d.date)
    """

    return conn.execute(sql).fetchdf()


def references_approved_by_assignee_by_month(conn) -> pd.DataFrame:
    sql = """
        SELECT DATE_TRUNC('month', d.date) m, wt.assigned_to assigned_to, SUM(CASE WHEN wt.ref_status IS NOT NULL THEN 1 ELSE 0 END ) request_count
        FROM dates d
        LEFT JOIN wide_table wt ON d.date = wt.ref_requested_date
        WHERE wt.ref_status = 'APPROVED' OR wt.ref_status IS NULL
        GROUP BY DATE_TRUNC('month', d.date), wt.assigned_to
        ORDER BY DATE_TRUNC('month', d.date)
    """

    return conn.execute(sql).fetchdf()


def references_handled_by_package_by_month(conn) -> pd.DataFrame:
    sql = """
            SELECT DATE_TRUNC('month', d.date) m, wt.ref_package_name package_name, SUM(CASE WHEN wt.ref_status IS NOT NULL THEN 1 ELSE 0 END ) request_count
            FROM dates d
            LEFT JOIN wide_table wt ON d.date = wt.ref_requested_date
            WHERE wt.ref_status = 'SENT' OR wt.ref_status IS NULL
            GROUP BY DATE_TRUNC('month', d.date), wt.ref_package_name
            ORDER BY DATE_TRUNC('month', d.date)
        """

    return conn.execute(sql).fetchdf()


def average_completion_in_days(conn) -> pd.DataFrame:
    sql = """
    SELECT ROUND(AVG(requested_to_completed_days), 2) average_completion_days, assigned_to
    FROM wide_table wt 
    WHERE assigned_to IS NOT NULL
      AND requested_to_completed_days IS NOT NULL
    GROUP BY assigned_to
    """

    return conn.execute(sql).fetchdf()

