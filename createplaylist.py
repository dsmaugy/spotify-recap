from datetime import date
import sys
import spotipy
import spotipy.util as util


scope = 'user-library-read user-top-read playlist-modify-public'


class SpotifyApp:
    def __init__(self, username):
        self.username = username

        token = util.prompt_for_user_token(self.username, scope)

        if token:
            self.sp = spotipy.Spotify(auth=token)
        else:
            raise Exception("Couldn't get token")

    # get the user's top numTracks tracks in a default time period of one month
    def get_top_tracks(self, numTracks=20, timeLength="short_term"):
        results = self.sp.current_user_top_tracks(limit=numTracks, time_range=timeLength)
        return [item["id"] for item in results["items"]]
    
    # creates a spotify playlist called playlistName and returns the playlist ID
    def create_playlist(self, playlistName):
        return self.sp.user_playlist_create(user=self.username, name=playlistName, public=True)["id"]

    # adds tracks to a given playlist
    def populate_playlist(self, playlistID, trackList):
        self.sp.user_playlist_add_tracks(user=self.username, playlist_id=playlistID, tracks=trackList)
        

        


if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    sp = SpotifyApp(username)
    
    playlistName = date.today().strftime("%B %Y")
    
    sp.populate_playlist(playlistID=sp.create_playlist(playlistName), trackList=sp.get_top_tracks(numTracks=20))

    print("Playlist '" + playlistName + "' created successfully!")


    