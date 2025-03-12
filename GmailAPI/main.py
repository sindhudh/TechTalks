import argparse
import datetime
import email.utils as e
from sqlalchemy import desc

from clients.email_factory import EmailClientFactory

from models.model import init_db, SessionLocal, Email

from Buildqueryfromrules import process_emails

def fetch_and_store_emails(provider):
    """
    Fetch emails from the specified provider and store them in the database.
    This function initializes the database, retrieves the latest email ID, 
    fetches new emails from the given provider, and stores them in the database.
    Args:
        provider (str): The email provider from which to fetch emails.
    Raises:
        Exception: If there is an error in fetching or storing emails.
    Example:
        fetch_and_store_emails("gmail")
    Note:
        Ensure that the database and email client are properly configured 
        before calling this function.
    """
   
   
    try:
        print("Started fetching emails")
        init_db()
        db = SessionLocal()
        email_client = EmailClientFactory.get_email_client(provider)
        emails = email_client.fetch_emails()

        for email in emails:
            db_email = Email(
                id=email["id"],
                From=email["From"],
                Subject=email["Subject"],
                message=email["message"],
                Date=datetime.datetime.fromtimestamp(e.mktime_tz(e.parsedate_tz(email["Date"]))),
                To=email.get("To", ""),
                Cc=email.get("Cc", ""),
                label=email.get("labels", "")
            )
            db.merge(db_email)
        db.commit()
        print("Emails fetched successfully")
    except Exception as error:
        print(f"Exception in fetching email from {provider}\n Exception Message : {str(error)}")

def main():
    # Set up argparse to accept command line parameters
    parser = argparse.ArgumentParser(description="Fetch and process emails from a specified provider.")
    
    # Adding the arguments
    parser.add_argument(
        '--provider', 
        type=str, 
        required=True, 
        choices=["gmail", "outlook", "yahoo"],  # Add more email providers if needed
        help="Email provider to fetch emails from"
    )
    parser.add_argument(
        '--fetch_emails', 
        type=bool, 
        default=False, 
        help="Set to True to fetch and store emails"
    )
    parser.add_argument(
        '--process_emails', 
        type=bool, 
        default=False, 
        help="Set to True to process emails"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Fetch emails if requested
    if args.fetch_emails:
        fetch_and_store_emails(args.provider)
    
    # Process emails if requested
    if args.process_emails:
        process_emails(args.provider)



if __name__ == "__main__":
    main()
    # provider = "gmail"  # Change to "gmail" or other providers
    # fetch_and_store_emails(provider)
    # process_emails(provider)