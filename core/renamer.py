import os
import re
import json
import time
from typing import Optional
import anitopy
from core.models import RenameConfig

VIDEO_EXTS = ('.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm')
SUB_EXTS = ('.ass', '.srt', '.vtt')
DUB_EXTS = ('.mka', '.aac', '.ac3', '.mp3', '.flac')

class RenamerService:
    EXTRA_KEYWORDS = (
        'bonus', 'nced', 'ncop', 'menu', 'pv', 'cm', 
        'preview', 'creditless', 'no-credit', 'nocredit', 'no_credit'
    )

    # Скрытый файл-снимок, который создаётся в папке релиза перед
    # переименованием. Хранит полный список файлов "как было" (чтобы потом
    # можно было отличить оригинальные файлы от добавленных позже постеров/
    # баннеров) и карту original_name -> current_name для отката.
    BACKUP_FILENAME = 'nekodesk.json'

    @classmethod
    def is_extra(cls, file_name: str) -> bool:
        name_lower = file_name.lower()
        for kw in cls.EXTRA_KEYWORDS:
            if re.search(r'(?:^|[_\s\.-])' + re.escape(kw) + r'(?:[_\s\.-]|\b)', name_lower):
                return True
        return False

    @staticmethod
    def generate_name(template: str, config: RenameConfig, episode: int = 0) -> str:
        episodes_str = str(config.episodes_num) if config.episodes_num > 0 else ""
        
        res = config.resolution.strip()
        width, height = "", ""

        match_res = re.search(r'(?:(\d+)\s*x\s*)?(\d+)', res, re.IGNORECASE)
        if match_res:
            if match_res.group(1):
                width = match_res.group(1)
            height = match_res.group(2)

        quality = f"{height}p" if height else ""

        padding = max(2, len(episodes_str))
        formatted_ep = str(episode).zfill(padding)

        replacements = {
            '{title}': config.title,
            '{season_num}': str(config.season_num).zfill(2),
            '{season}': config.season,
            '{year}': config.year,
            '{type}': config.media_type,
            '{studio}': config.studio,
            '{duration}': config.duration,
            '{source}': config.source,
            '{resolution}': res,
            '{height}': height,
            '{width}': width,
            '{quality}': quality,
            '{fansub}': config.fansub,
            '{score}': config.score,
            '{status}': config.status,
            '{episodes}': episodes_str,
            '{country}': config.country,
            '{episode}': formatted_ep,
            '{ep}': formatted_ep
        }

        result = template
        for tag, val in replacements.items():
            result = result.replace(tag, str(val if val is not None else ""))

        result = re.sub(r'[\\/*?:"<>|]', '', result)
        return result.strip()
    
    @staticmethod
    def extract_episode(file_name: str, max_eps: int) -> Optional[int]:
        parsed = anitopy.parse(file_name)
        if parsed and parsed.get('episode_number'):
            ep_val = parsed.get('episode_number')
            if isinstance(ep_val, list):
                ep_val = ep_val[0]
            try:
                ep_num = int(ep_val)
                if ep_num <= 999:
                    return ep_num
            except (ValueError, TypeError):
                pass

        match = re.search(r'(?:S\d+E|EP?|SP|[_\s\[\(-])(\d{1,3})(?:[_\s\]\)-]|\b)', file_name, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass

        return None

    @classmethod
    def build_queue(cls, config: RenameConfig, items: list) -> list[tuple[str, str]]:
        rename_queue = []
        used_new_paths = set()
        
        # 1. Подготовка разрешенных расширений
        allowed_video = tuple(VIDEO_EXTS)
        allowed_subs = tuple(SUB_EXTS) if config.rename_subs else ()
        allowed_dubs = tuple(DUB_EXTS) if config.rename_dubs else ()
        allowed_extra_media = allowed_subs + allowed_dubs

        max_allowed_ep = (config.start_from_ep + config.episodes_num - 1) if config.episodes_num > 0 else 999

        # 2. Сбор уникальных файлов из отмеченных галочками элементов
        all_found_files = {} 
        
        for item in items:
            path = item['path']
            if item.get('is_dir'):
                for root, _, files in os.walk(path):
                    for f in files:
                        if not cls.is_extra(f):
                            full_path = os.path.join(root, f).replace('\\', '/')
                            all_found_files[full_path] = {'name': f, 'path': full_path}
            else:
                name = item['name']
                if not cls.is_extra(name):
                    # Приводим путь к единому стандарту для ключа словаря
                    std_path = path.replace('\\', '/')
                    all_found_files[std_path] = item
        
        unique_files = list(all_found_files.values())

        # 3. Этап 1: Обработка только ВИДЕОфайлов
        video_entries = [] 
        
        for data in unique_files:
            file_name = data['name']
            if not file_name.lower().endswith(allowed_video):
                continue

            # Жесткое присвоение номера для одиночных файлов (фильмы/OVA)
            if config.is_movie or (config.media_type in ['MOVIE', 'OVA', 'SPECIAL'] and config.episodes_num == 1):
                parsed_ep = config.start_from_ep
            else:
                # Парсинг для сериалов
                parsed_ep = cls.extract_episode(file_name, config.episodes_num)
                if parsed_ep is None:
                    continue
                if config.episodes_num > 0 and not (config.start_from_ep <= parsed_ep <= max_allowed_ep):
                    continue

            video_entries.append((data, parsed_ep))

        # Карта привязки: {номер_эпизода: путь_к_папке_видео}
        matched_episodes = {ep: os.path.dirname(data['path']) for data, ep in video_entries}

        # 4. Этап 2: Обработка СУБТИТРОВ и АУДИО
        extra_entries = []
        if allowed_extra_media:
            # Тот же критерий "одиночного релиза", что и для видео на этапе 1 —
            # нужен, чтобы сабы без номера серии в имени файла можно было
            # привязать к единственному эпизоду, даже если видео вообще не
            # отмечено.
            is_single_release = config.is_movie or (config.media_type in ['MOVIE', 'OVA', 'SPECIAL'] and config.episodes_num == 1)

            for data in unique_files:
                file_name = data['name']
                if not file_name.lower().endswith(allowed_extra_media):
                    continue

                parsed_ep = cls.extract_episode(file_name, config.episodes_num)

                if matched_episodes:
                    # Есть подходящие отмеченные видеофайлы — привязываем
                    # сабы/дабы к их номерам серий, как и раньше.
                    if parsed_ep is None and len(matched_episodes) == 1:
                        parsed_ep = list(matched_episodes.keys())[0]
                    if parsed_ep not in matched_episodes:
                        continue
                else:
                    # Видео не отмечено (или не найдено вовсе) — переименовываем
                    # сабы/дабы сами по себе, проверяя номер серии по общему
                    # диапазону релиза, точно так же, как это делается для видео.
                    if parsed_ep is None:
                        if is_single_release:
                            parsed_ep = config.start_from_ep
                        else:
                            continue
                    elif config.episodes_num > 0 and not (config.start_from_ep <= parsed_ep <= max_allowed_ep):
                        continue

                extra_entries.append((data, parsed_ep))

        # 5. Формирование финальной очереди
        final_targets = video_entries + extra_entries

        for data, ep_num in final_targets:
            file_name = data['name']
            file_path = data['path']
            
            ext = os.path.splitext(file_name)[1]
            base_new_name = cls.generate_name(config.template, config, ep_num)
            new_name = base_new_name + ext
            
            file_dir = os.path.dirname(file_path)
            new_file_path = os.path.normpath(os.path.join(file_dir, new_name)).replace('\\', '/')

            if new_file_path in used_new_paths:
                continue

            used_new_paths.add(new_file_path)
            rename_queue.append((file_path, new_file_path))

        return rename_queue

    # ------------------------------------------------------------------
    # Резервный снимок оригинальных имён
    # ------------------------------------------------------------------

    @classmethod
    def snapshot_file_path(cls, folder_path: str) -> str:
        """Путь к скрытому файлу-снимку внутри папки релиза."""
        return os.path.join(folder_path, cls.BACKUP_FILENAME)

    @staticmethod
    def _hide_file_windows(path: str) -> None:
        """На Windows ведущая точка в имени не делает файл скрытым сама по
        себе — выставляем атрибут Hidden явно. На других ОС ничего не
        делаем (там достаточно точки в начале имени)."""
        if os.name == 'nt':
            try:
                import ctypes
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)
            except Exception:
                pass

    @classmethod
    def _scan_folder_snapshot(cls, folder_path: str) -> list[str]:
        """Полный список файлов в папке (пути относительно folder_path),
        не считая сам скрытый файл резервной копии."""
        result = []
        for root, _, files in os.walk(folder_path):
            for f in files:
                if f == cls.BACKUP_FILENAME:
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, folder_path).replace('\\', '/')
                result.append(rel_path)
        return sorted(result)

    @classmethod
    def create_backup_snapshot(
        cls,
        folder_path: str,
        rename_queue: list[tuple[str, str]],
        folder_rename: Optional[tuple[str, str]] = None,
    ) -> Optional[str]:
        """
        Создаёт (или дополняет) скрытый файл ``nekodesk.json``
        в папке с медиа. Файл хранит:

          - ``original_files`` — полный список файлов папки на момент ПЕРВОГО
            запуска переименования для этой папки (точка отсчёта). Не
            перезаписывается при повторных запусках, чтобы не потерять
            изначальное состояние. Сравнивая его с текущим содержимым папки,
            позже можно понять, какие файлы были добавлены позже (например,
            сохранённые постеры/баннеры).
          - ``rename_map`` — карта «оригинальное относительное имя файла» ->
            «текущее относительное имя файла». Накапливается между запусками
            и всегда указывает от самого первого имени файла к последнему.
          - ``folder_rename`` — ``{"original": <имя>, "current": <имя>}`` для
            самой папки релиза (если её тоже переименовывают), по той же
            логике: "original" не перезаписывается, "current" обновляется.

        ``folder_rename`` — (старый_путь_папки, новый_путь_папки), если в
        этом запуске папку тоже собираются переименовать. Вызывать ДО того,
        как реально что-то переименуется на диске (пока старые пути ещё
        существуют).
        """
        if not rename_queue and not folder_rename and not os.path.isdir(folder_path):
            return None

        backup_path = cls.snapshot_file_path(folder_path)

        original_files = None
        rename_map: dict[str, str] = {}
        folder_rename_data = None
        created_at = time.time()

        if os.path.isfile(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8') as fh:
                    existing = json.load(fh)
                original_files = existing.get('original_files')
                rename_map = existing.get('rename_map') or {}
                folder_rename_data = existing.get('folder_rename')
                created_at = existing.get('created_at', created_at)
            except (OSError, ValueError):
                original_files = None
                rename_map = {}
                folder_rename_data = None

        if original_files is None:
            # Первый запуск для этой папки — фиксируем полный список файлов
            # "как было", до какого-либо переименования.
            original_files = cls._scan_folder_snapshot(folder_path)

        for old_path, new_path in rename_queue:
            old_rel = os.path.relpath(old_path, folder_path).replace('\\', '/')
            new_rel = os.path.relpath(new_path, folder_path).replace('\\', '/')

            # Если файл уже переименовывался раньше, находим его самое
            # первое (оригинальное) имя и обновляем конечную точку, а не
            # создаём новую запись с промежуточным именем в качестве ключа.
            original_key = old_rel
            for orig_name, current_name in rename_map.items():
                if current_name == old_rel:
                    original_key = orig_name
                    break

            rename_map[original_key] = new_rel

        if folder_rename:
            old_folder, new_folder = folder_rename
            new_folder_name = os.path.basename(os.path.normpath(new_folder))
            if folder_rename_data and folder_rename_data.get('original'):
                # Папку уже переименовывали раньше — сохраняем самое первое
                # имя, обновляем только текущее.
                original_folder_name = folder_rename_data['original']
            else:
                original_folder_name = os.path.basename(os.path.normpath(old_folder))
            folder_rename_data = {'original': original_folder_name, 'current': new_folder_name}

        data = {
            'folder_path': folder_path,
            'created_at': created_at,
            'updated_at': time.time(),
            'original_files': original_files,
            'rename_map': rename_map,
            'folder_rename': folder_rename_data,
        }

        tmp_path = backup_path + '.tmp'
        with open(tmp_path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        os.replace(tmp_path, backup_path)

        cls._hide_file_windows(backup_path)

        return backup_path

    @classmethod
    def build_restore_queue(cls, folder_path: str) -> list[tuple[str, str]]:
        """
        Читает скрытый файл-снимок и строит очередь для отката
        переименования ФАЙЛОВ: (текущий_путь, оригинальный_путь).

        В очередь попадают только файлы, которые всё ещё существуют на
        диске под переименованным именем. Файлы, добавленные в папку уже
        после снимка (постеры/баннеры и т.п.), в rename_map не входят и
        восстановлением не затрагиваются — их можно получить отдельно через
        ``list_added_files``. ``folder_path`` — ТЕКУЩИЙ путь к папке (как
        она называется сейчас).
        """
        backup_path = cls.snapshot_file_path(folder_path)
        if not os.path.isfile(backup_path):
            return []

        try:
            with open(backup_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            return []

        rename_map = data.get('rename_map') or {}
        restore_queue = []

        for original_rel, current_rel in rename_map.items():
            current_path = os.path.normpath(os.path.join(folder_path, current_rel))
            original_path = os.path.normpath(os.path.join(folder_path, original_rel))
            if current_path != original_path and os.path.isfile(current_path):
                restore_queue.append((current_path, original_path))

        return restore_queue

    @classmethod
    def get_folder_restore(cls, folder_path: str) -> Optional[tuple[str, str]]:
        """
        Возвращает (текущий_путь_папки, оригинальный_путь_папки), если саму
        папку релиза переименовывали и это можно откатить, иначе None.
        ``folder_path`` — ТЕКУЩИЙ путь к папке (как она называется сейчас).

        Ничего не откатывает сама — только строит пару путей, которую можно
        скормить в RenameWorker как ``folder_rename`` (в обратном
        направлении: current -> original).
        """
        backup_path = cls.snapshot_file_path(folder_path)
        if not os.path.isfile(backup_path):
            return None

        try:
            with open(backup_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            return None

        folder_rename = data.get('folder_rename')
        if not folder_rename:
            return None

        original_name = folder_rename.get('original')
        current_name = folder_rename.get('current')
        if not original_name or not current_name or original_name == current_name:
            return None

        current_folder_path = os.path.normpath(folder_path)

        # Имя папки на диске сейчас должно совпадать с тем, что записано как
        # "current" в снимке — иначе её, видимо, переименовали вручную мимо
        # программы, и откат тут не поможет (не пытаемся угадывать).
        if os.path.basename(current_folder_path) != current_name:
            return None

        parent_dir = os.path.dirname(current_folder_path)
        original_folder_path = os.path.normpath(os.path.join(parent_dir, original_name))

        return (current_folder_path, original_folder_path)

    @classmethod
    def has_restorable_changes(cls, folder_path: str) -> bool:
        """Удобная проверка «есть ли вообще что откатывать в этой папке»
        (файлы и/или сама папка) — для показа пункта меню Restore."""
        if cls.build_restore_queue(folder_path):
            return True
        return cls.get_folder_restore(folder_path) is not None

    @classmethod
    def list_added_files(cls, folder_path: str) -> list[str]:
        """
        Сравнивает текущее содержимое папки со списком файлов на момент
        создания снимка и возвращает относительные пути файлов, которых
        тогда не было — то есть добавленных позже (постеры, баннеры,
        .torrent-файлы и т.п.).
        """
        backup_path = cls.snapshot_file_path(folder_path)
        if not os.path.isfile(backup_path):
            return []

        try:
            with open(backup_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            return []

        original_files = set(data.get('original_files') or [])
        current_files = set(cls._scan_folder_snapshot(folder_path))

        return sorted(current_files - original_files)