import os
import time
from typing import Optional
from PySide6.QtCore import QThread, Signal
from core.models import RenameConfig

class RenameWorker(QThread):
    # Сигналы для связи с GUI
    progress_changed = Signal(int, int, str)  # текущий, всего, имя файла
    error_occurred = Signal(str)             # текст ошибки
    completed = Signal(str)                  # итоговый статус

    def __init__(
        self,
        rename_queue: list[tuple[str, str]],
        config: RenameConfig,
        qbit_client=None,
        torrent_obj=None,
        folder_rename: Optional[tuple[str, str]] = None,
        new_torrent_name: Optional[str] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.rename_queue = rename_queue
        self.config = config
        self.qbit_client = qbit_client
        self.torrent_obj = torrent_obj
        # (старый_путь_папки, новый_путь_папки) — переименовывается ПОСЛЕ
        # всех файлов внутри неё. None, если папку переименовывать не нужно.
        self.folder_rename = folder_rename
        # Новое отображаемое имя торрента в клиенте (не путь на диске).
        # None, если торрент переименовывать не нужно.
        self.new_torrent_name = new_torrent_name

    def run(self):
        total = len(self.rename_queue)

        # 1. Файлы
        for index, (old_path, new_path) in enumerate(self.rename_queue, start=1):
            if os.path.normpath(old_path) == os.path.normpath(new_path):
                continue

            try:
                if self.config.use_qbit and self.qbit_client and self.torrent_obj:
                    self.qbit_client.rename_torrent_file(self.torrent_obj, old_path, new_path)
                else:
                    os.rename(old_path, new_path)

                # Шлем сигнал прогресса
                self.progress_changed.emit(index, total, os.path.basename(new_path))
                time.sleep(0.05)

            except Exception as e:
                msg = str(e) if str(e).strip() else f"Unknown error type: {type(e).__name__}"
                self.error_occurred.emit(f"Ошибка на файле {old_path}:\n{msg}")
                return

        # 2. Сама папка релиза — только после того, как все файлы внутри
        # неё уже переименованы (иначе относительные пути файлов "уехали"
        # бы посреди процесса).
        if self.folder_rename:
            old_folder, new_folder = self.folder_rename
            if os.path.normpath(old_folder) != os.path.normpath(new_folder):
                try:
                    if self.config.use_qbit and self.qbit_client and self.torrent_obj:
                        self.qbit_client.rename_torrent_folder(self.torrent_obj, old_folder, new_folder)
                    else:
                        os.rename(old_folder, new_folder)
                except Exception as e:
                    msg = str(e) if str(e).strip() else f"Unknown error type: {type(e).__name__}"
                    self.error_occurred.emit(f"Ошибка при переименовании папки {old_folder}:\n{msg}")
                    return

        # 3. Отображаемое имя торрента в клиенте (не путь на диске) —
        # отдельная операция, включается своим чекбоксом.
        if self.new_torrent_name and self.config.use_qbit and self.qbit_client and self.torrent_obj:
            try:
                ok = self.qbit_client.rename_torrent(self.torrent_obj, self.new_torrent_name)
                if not ok:
                    self.error_occurred.emit(
                        f"Не удалось переименовать торрент в клиенте на «{self.new_torrent_name}»"
                    )
                    return
            except Exception as e:
                msg = str(e) if str(e).strip() else f"Unknown error type: {type(e).__name__}"
                self.error_occurred.emit(f"Ошибка при переименовании торрента:\n{msg}")
                return

        self.completed.emit("Переименование успешно завершено!")