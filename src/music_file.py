from src.chord import Chord


class MusicFile:

    def __init__(self, json_data: dict):
        """
        Stores the clean JSON file data and retrieves critical info.

        @param json_data (dict): The clean JSON file data.
        """
        self.data = json_data


    def add_chords(self, track_name: str, chords: list[Chord]) -> None:
        """
        Add the chords for a given track produced by an instrument.

        @param track_name (str): The name of a given track.
        @param chords (list[Chord]): The chords for a given track.
        """
        for t, track in enumerate(self.track_names()):
            if (track == track_name):
                break
                
        self.data["tracks"][t]["chords"] = chords

    
    def instruments(self) -> list[str]:
        """
        The defined instruments by the JSON file.

        return (list[str]): The list of instruments.
        """
        return list(self.data["instruments"].keys())
    

    def partials(self, instrument: str) -> list[tuple[float, float]]:
        """
        The partials of a particular instrument.

        @param instrument (str): The instrument name.

        return (list[tuple[float, float]]): The list of partials for an instrument.
        """
        return [partial for partial in self.data["instruments"][instrument]]
    

    def track_names(self) -> list[str]:
        """
        The names of all listed tracks.

        return (list[str]): The list of track names.
        """
        return [track["name"] for track in self.data["tracks"]]
            

    def track_notes(self, track_name: str) -> list[str]:
        """
        The sequence of notes for a given track.

        @param track_name (str): The name of the track.

        return (list[str]): The list of notes for a track.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["notes"]
            
    
    def track_instrument(self, track_name: str) -> str:
        """
        The instrument corresponding to a track.

        @param track_name (str): The name of the track.

        return (str): The name of an instrument.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["instrument"]
            

    def track_dynamic(self, track_name: str) -> str:
        """
        The dynamic corresponding to a track.

        @param track_name (str): The name of the track.

        return (str): A dynamic.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["dynamic"]
            
    
    def track_chords(self, track_name: str) -> list[Chord]:
        """
        The chords of a given track.

        @param track_name (str): The name of the track.

        return (list[Chord]): A list of chords.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["chords"]

