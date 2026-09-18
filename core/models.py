from dataclasses import dataclass
from typing import Optional

@dataclass
class RenameConfig:
    folder_path: str
    template: str
    folder_template: str = ""
    torrent_template: str = ""
    
    # Метаданные релиза для генератора имён
    title: str = ""
    season_num: str = "01"
    season: str = ""
    year: str = ""
    media_type: str = ""
    studio: str = ""
    duration: str = ""
    source: str = ""
    resolution: str = ""
    fansub: str = ""
    score: str = ""
    status: str = ""
    country: str = ""

    # Флаги
    rename_subs: bool = False
    rename_dubs: bool = False
    rename_folder: bool = False
    rename_torrent: bool = False
    
    # Настройки серий/типа
    is_movie: bool = False
    episodes_num: int = 0
    start_from_ep: int = 1
    
    # qBittorrent
    use_qbit: bool = False