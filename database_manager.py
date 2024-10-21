import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

DB_TYPE = 'mysql'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_USER = 'youtubedata'
DB_PASS = 'p0o9i8u7y6'
DB_NAME = 'youtube_data'

engine = create_engine(f'{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def migrate_data_to_sql(channel_df, video_df):
    try:
        print("Starting data migration...")
        print("Channel DataFrame Content:", channel_df.head())
        print("Video DataFrame Content:", video_df.head())
        
        with engine.connect() as connection:
            if not channel_df.empty:
                print("Migrating Channel DataFrame to SQL...")
                channel_df.to_sql('channels', con=connection, if_exists='replace', index=False)
                print("Channel DataFrame migrated successfully.")
            else:
                return "Channel DataFrame is empty. No data to migrate."

            if not video_df.empty:
                print("Migrating Video DataFrame to SQL...")
                video_df.to_sql('videos', con=connection, if_exists='replace', index=False)
                print("Video DataFrame migrated successfully.")
            else:
                return "Video DataFrame is empty. No data to migrate."

        print("Data migration completed successfully.")
        return "Data migrated to SQL successfully."
    except SQLAlchemyError as e:
        print(f"An error occurred while migrating data to SQL: {e}")
        return f"An error occurred while migrating data to SQL: {e}"
