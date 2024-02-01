import numpy as np
import matplotlib.pyplot as plt
import requests

def compute_zipf_values(most_listened_artist_scrobbles, n):
    zipf_values = [most_listened_artist_scrobbles / i for i in range(1, n + 1)]
    return zipf_values


def get_top_artists(api_key, username, limit=20):
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={api_key}&format=json&limit={limit}"
    response = requests.get(url)
    data = response.json()

    if 'topartists' in data and 'artist' in data['topartists']:
        top_artists = {}
        for artist in data['topartists']['artist']:
            top_artists[artist['name']] = int(artist['playcount'])  # Corrected: use artist name as key
        return top_artists
    else:
        print("Error: Unable to fetch top artists.")
        return None


def plot_zipf_values(zipf_values, scrobbled_artists=None):
    x = np.arange(1, len(zipf_values) + 1)
    width = 0.35  # Width of the bars

    fig, ax = plt.subplots()
    zipf_bars = ax.bar(x - width / 2, zipf_values, width, color='b', alpha=0.7, label='Zipf Values')

    if scrobbled_artists:
        artists, listens = zip(*scrobbled_artists.items())
        scrobbled_bars = ax.bar(x + width / 2, listens, width, color='r', alpha=0.7, label='Scrobbled Artists')

    ax.set_xlabel('Artist')  # Corrected: set xlabel to 'Artist'
    ax.set_ylabel('Count')
    ax.set_title('Zipf Values and Top Scrobbled Artists')

    # Set x-axis ticks and labels with artist names only
    x_labels = list(scrobbled_artists.keys())  # Corrected: use artist names
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=90)  # Corrected: rotate artist names for better visibility

    ax.legend()

    def autolabel(bars):
        """Attach a text label above each bar in *bars*, displaying its height."""
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{:.0f}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(zipf_bars)
    if scrobbled_artists:
        autolabel(scrobbled_bars)

    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

def read_api_key(filename='api_key.txt'):
    try:
        with open(filename, 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"Error: API key file '{filename}' not found.")
        return None


if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your Last.fm API key
    api_key = read_api_key()

    # Replace 'YOUR_USERNAME' with your Last.fm username
    username = input("Username: ")

    # Fetch top scrobbled artists
    top_artists = get_top_artists(api_key, username)

    if top_artists:
        # Get the number of scrobbles for the most listened artist
        most_listened_artist_scrobbles = max(top_artists.values())

        # Compute Zipf values with the adjusted starting point
        n = 20  # Number of scrobbled artists to consider
        zipf_values = compute_zipf_values(most_listened_artist_scrobbles, n)

        # Plot Zipf values and top scrobbled artists
        plot_zipf_values(zipf_values, top_artists)
