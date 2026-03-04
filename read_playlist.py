#read_playlist.py
# Reads all items from the DynamoDB Playlists table and prints them.

import boto3
from boto3.dynamodb.conditions import Key, Attr
from read_movies import get_movie_by_title, print_movie

# -------------------------------------------------------
# Configuration — update REGION if your table is elsewhere
# -------------------------------------------------------
REGION = "us-east-1"
TABLE_NAME = "Playlist"


def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)


def print_playlist(song):
    title = song.get("Title", "Unknown Title")
    artist = song.get("Artist", "Unknown Artist")
    time = song.get("Time", "Unknown Time")

    print(f"  Title  : {title}")
    print(f"  Artist : {artist}")
    print(f"  Time   : {time}")
    print()



def print_all_playlist():
    """Scan the entire Playlist table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No playlists found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} playlist(s):\n")
    for song in items:
        print_playlist(song)


def main():
    print("===== Reading from DynamoDB =====\n")
    print_all_playlist()


if __name__ == "__main__":
    main()
