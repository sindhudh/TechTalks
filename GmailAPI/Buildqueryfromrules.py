import json
import datetime
import os

from sqlalchemy import create_engine, and_, or_
from googleapiclient.http import BatchHttpRequest

from config import config 

from models.model import init_db, SessionLocal, Email

from clients.email_factory import EmailClientFactory

def load_rules(file_path=os.getcwd() + "/process_emails/rules/rules.json"):
    """Load rules from JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

def build_query_filters(rule):
    """
    Builds a SQLAlchemy query filter based on the provided rule.
    Args:
        rule (dict): A dictionary containing the rules for building the query.
            The dictionary should have the following structure:
            {
                "predicate": "all" or "any",
                "rules": [
                    {
                        "field": "field_name",
                        "predicate": "contains" or "does not contain" or "equals" or "does not equal" or "less than" or "greater than",
                        "value": value
                    },
                    ...
                ]
            }
    Returns:
        sqlalchemy.sql.elements.BooleanClauseList: A SQLAlchemy filter clause constructed based on the provided rules.
    Raises:
        Exception: If there is an error in building the query filter, an exception is caught and a message is printed.
    """

    try:
        print(f"Started building rules for {str(rule)}")
        conditions = []
        for condition in rule["rules"]:
            field = getattr(Email, condition["field"], None)
            if not field:
                continue
            predicate = condition["predicate"].lower()
            value = condition["value"]

            # Build conditions based on the predicate
            if predicate == "contains":
                conditions.append(field.ilike(f"%{value}%"))
            elif predicate == "does not contain":
                conditions.append(~field.ilike(f"%{value}%"))
            elif predicate == "equals":
                conditions.append(field == value)
            elif predicate == "does not equal":
                conditions.append(field != value)
            elif predicate in ["less than", "greater than"] and condition["field"] == "Date":
                days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=value)
                if predicate == "less than":
                    conditions.append(field < days_ago)
                else:
                    conditions.append(field > days_ago)
        return and_(*conditions) if rule["predicate"].lower() == "all" else or_(*conditions)
    except Exception as error:
        print(f"Exception in building rule for {str(rule)}\n Exception Message : {str(error)}")

def apply_actions(session, emails, actions, provider):
    """
    Apply specified actions to a list of emails using the given session and email provider.

    Parameters:
    session (Session): The database session to commit changes.
    emails (list): A list of email objects to apply actions on.
    actions (list): A list of action dictionaries specifying the actions to perform.
                    Each action dictionary should have an "action" key with values
                    "mark as read" or "move to folder", and optionally a "folder" key.
    provider (str): The email provider to use for performing actions.

    Raises:
    Exception: If there is an error while applying actions.

    Example:
    actions = [
        {"action": "mark as read"},
        {"action": "move to folder", "folder": "archive"}
    ]
    apply_actions(session, emails, actions, "gmail")
    """
    try:
        print(f"applying actions on {emails}")
        email_client = EmailClientFactory.get_email_client(provider)
        mark_as_read = []
        move_emails = {}
        for action in actions:
            if action["action"].lower() == "mark as read":
                for email in emails:
                    print(email)
                    email.label = email.label.replace("UNREAD", "").strip(',')
                    mark_as_read.append(email.id)
            elif action["action"].lower() == "move to folder":
                folder = action.get("folder", "inbox")
                for email in emails:
                    move_emails[email.id] = folder
                    email.label = f"{folder},{email.label}" if folder not in email.label else email.label
        session.commit()
        if mark_as_read:
            email_client.mark_as_read(mark_as_read)
        if move_emails:
            email_client.move_email(move_emails)
    except Exception as error:
        print(f"Exception in applying action \n Exception Mesage:{str(error)}")

def process_emails(provider):
    """
    Processes emails based on predefined rules and applies specified actions.
    Args:
        provider (str): The email provider to process emails for.
    This function performs the following steps:
    1. Loads the rules for processing emails.
    2. Iterates over each rule and builds query filters based on the rule conditions.
    3. Queries the database for emails that match the rule conditions.
    4. Applies the specified actions to the emails in batches of 10.
    5. Closes the database session after processing all emails.
    Prints messages indicating the start and end of the email processing.
    """
    print(f"Started processing emails")
    session = SessionLocal()
    rules = load_rules()

    for rule in rules:
        rule_conditions = build_query_filters(rule["Rule"])
        query = session.query(Email).filter(rule_conditions)
        for batch in query.yield_per(config.get("max_results_db")):
            apply_actions(session, [batch], rule["Rule"]["actions"], provider)

    session.close()
    print(f"End of processing emails")

