# read_movies.py
# Reads all items from the DynamoDB Movies table and prints them.
# Part of Lab 09 — feature/read-dynamo branch

import boto3
from boto3.dynamodb.conditions import Key, Attr

# -------------------------------------------------------
# Configuration — update REGION if your table is elsewhere
# -------------------------------------------------------
REGION = "us-east-1"
TABLE_NAME = "Movies"


def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)


def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", "No ratings")
    genre = movie.get("Genre", "No genre")

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Genre  : {genre}")
    print()
    # adding a comment to test git


def get_movie_by_title():
    """Prompt the user to enter a movie title and search for it in the DynamoDB table."""
    title = input("Enter the movie title: ").strip()

    # Get the table reference using get_table()
    table = get_table()

    response = table.scan(
        FilterExpression=Attr('Title').eq(title)  # Corrected attribute name (case-sensitive)
    )

    movies = response.get("Items", [])
    if movies:
        print(f"\nFound '{title}':\n")
        for movie in movies:
            print_movie(movie)
    else:
        print(f"\n'{title}' not found.")

def create_movie():
    """Create a new movie item in the DynamoDB table."""
    title = input("Enter the movie title: ").strip()
    year = input("Enter the release year: ").strip()
    ratings = input("Enter the ratings (comma-separated): ").strip()
    genre = input("Enter the genre: ").strip()

    # Get the table reference using get_table()
    table = get_table()

    # Create a new movie item
    movie_item = {
        "Title": title,
        "Year": year,
        "Ratings": ratings.split(","),
        "Genre": genre
    }

    # Put the item into the DynamoDB table
    table.put_item(Item=movie_item)
    print(f"\nMovie '{title}' created successfully.")


def update_rating():
    # Get the table reference using get_table()
    #Use try/except to handle potential errors when updating the item

    table = get_table() 
    

    title = input("What is the movie title? ")
    rating = int(input("What is the rating (integer): "))
    table.update_item(
        Key={"Title": title},
        UpdateExpression="SET Ratings = list_append(Ratings, :r)",
        ExpressionAttributeValues={':r': [rating]}
    )


def new():
    print("This is a new function added to test git branching and merging.")    


def print_all_movies():
    """Scan the entire Movies table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)


def delete_movie():
    """Delete a movie item from the DynamoDB table based on the title."""
    title = input("Enter the movie title to delete: ").strip()

    # Get the table reference using get_table()
    table = get_table()

    # Delete the item from the DynamoDB table
    response = table.delete_item(
        Key={"Title": title}
    )

    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
        print(f"\nMovie '{title}' deleted successfully.")
    else:
        print(f"\nFailed to delete movie '{title}'. Please check if it exists.")

def query_movie():
    # a function that returns the average rating for a given movie.
    title = input("What is the movie title? ")
    table = get_table()
    response = table.get_item(Key={"Title": title})
    movie = response.get("Item")
    if movie and "Ratings" in movie:
        ratings = movie["Ratings"]
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            print(f"\nAverage rating for '{title}': {average_rating:.2f}")
        else:
            print(f"\nNo ratings found for '{title}'.")
    else:
        print(f"\nMovie '{title}' not found or has no ratings.")

def main():
    print("===== Reading from DynamoDB =====\n")
    get_movie_by_title()


if __name__ == "__main__":
    main()
