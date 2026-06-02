

class MusicFile:

    def __init__(self, json_data: dict):
        """
        Stores the clean JSON file data and retrieves critical info.

        @param json_data (dict): The clean JSON file data.
        """
        self.data = json_data

    
    def instruments(self) -> list[str]:
        """
        The defined instruments by the JSON file.

        return (list[str]): The list of instruments.
        """
        return list(self.data["instruments"].keys())
    

    def pitches(self, instrument: str) -> list[str]:
        """
        The pitches of a particular instrument.

        @param instrument (str): The instrument name.

        return (list[str]): The list of pitches for an instrument.
        """
        return [partial[0] for partial in self.data["instruments"][instrument]]


    def amplitudes(self, instrument: str) -> list[str]:
        """
        The amplitudes of a particular instrument.

        @param instrument (str): The instrument name.

        return (list[str]): The list of amplitudes for an instrument.
        """
        return [partial[1] for partial in self.data["instruments"][instrument]]
    

    def track_names(self) -> list[str]:
        """
        The names of all listed tracks.

        return (list[str]): The list of track names.
        """
        return [track["name"] for track in self.data["tracks"]]
            

    def track_notes(self, track_name: str) -> list[str]:
        """
        The sequence of notes for a given track.

        return (list[str]): The list of notes for a track.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["notes"]
            
    
    def track_instrument(self, track_name: str) -> str:
        """
        The instrument corresponding to a track.

        return (str): The name of an instrument.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["instrument"]
            

    def track_dynamic(self, track_name: str) -> str:
        """
        The dynamic corresponding to a track.

        return (str): A dynamic.
        """
        for track in self.data["tracks"]:
            if (track["name"] == track_name):
                return track["dynamic"]

