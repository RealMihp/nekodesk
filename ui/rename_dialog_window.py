import PySide6
from PySide6.QtWidgets import *
import anitopy
import keyring
from core.logic import FileScanner, qbit
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QThread, QThreadPool, QUrl, QTimer, Signal

import sys, os, shutil, re

from ui.loading_dialog import LoadingDialog
from ui.ui_rename_dialog import *
from core.db import *
from core.utils import *
from core.api.anilist_api import *
from core.logic import FileScanner
from core.models import RenameConfig
from core.renamer import RenamerService
from core.worker import RenameWorker

VIDEO_EXTS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm')
SUB_EXTS = ('.ass', '.srt', '.ssa', '.vtt')
DUB_EXTS = ('.mka', '.mp3', '.aac', '.ac3', '.flac')
PATH_ROLE = 32
ORIGINAL_NAME_ROLE = 33
INVALID_PATH_CHARS = re.compile(r'[\\/:*?"<>|]')

class RenameWindow(QDialog):
    def __init__(self, parent=None, title_data: dict = {}, folder_path: str = "", db = LibraryDB):
        super().__init__(parent)
        self.ui = Ui_RenameDialog()
        self.ui.setupUi(self)
        self.parent=parent
        if not db:
            db = self.parent.ldbclient
        self.imgmClient = ImageManager()
        self.filemClient = FileManager()
        self.settings_db = SettingsDB()
        self.prefManager = PreferencesManager(db)
        
        

        self.qbit = self.settings_db.get('qbit', 'False')
        if self.qbit == "True":
            self.qbit = True
            creds = {
            "host": self.settings_db.get('qbit_ip'),
            "port": int(self.settings_db.get("qbit_port")),
            "username": self.settings_db.get("qbit_username"),
            "password": keyring.get_password("nekodesk", self.settings_db.get("qbit_username", "admin"))
            }
            
            self.qbitClient = qbit(**creds)
        else:
            self.qbit = False
            self.ui.torrent_widget.hide()
            self.ui.rename_torrent_checkBox.hide()


        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(300)     # Interval
        # Сначала пересчитываем, какие видеофайлы попадают в диапазон серий
        # (Episodes/Start from/Type могли измениться), и только потом
        # перестраиваем дерево — иначе чекбоксы в дереве отрисуются по
        # устаревшему набору отмеченных файлов.
        self.preview_timer.timeout.connect(self._auto_select_video_files)
        self.preview_timer.timeout.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))

        fields = [
            self.ui.title_lineEdit, self.ui.season_num_lineEdit, self.ui.season_lineEdit,
            self.ui.season_year_lineEdit, self.ui.type_comboBox, self.ui.studio_lineEdit,
            self.ui.duration_lineEdit, self.ui.source_lineEdit, self.ui.resolution_lineEdit,
            self.ui.fansub_lineEdit, self.ui.country_lineEdit, self.ui.score_lineEdit,
            self.ui.status_lineEdit, self.ui.episodes_lineEdit, self.ui.start_from_lineEdit,
            self.ui.template_lineEdit, self.ui.folder_name_lineEdit,
            self.ui.save_poster_lineEdit, self.ui.save_banner_lineEdit, self.ui.torrent_name_lineEdit
            ]
        for field in fields:
            if isinstance(field, QComboBox):
                field.currentTextChanged.connect(self.preview_timer.start)
            elif isinstance(field, QLineEdit):
                field.textChanged.connect(self.preview_timer.start)

        self.history = []
        self.forward_stack = []
        self.title_data = title_data
        self.folder_path = folder_path
        self.current_dir = folder_path

        # Постоянное хранилище отмеченных элементов: path -> {'name','path','is_dir'}.
        # В отличие от обхода preview_treeWidget, не привязано к тому, какая
        # папка сейчас отображена в дереве, поэтому галочки не теряются при
        # переходе между папками (например, при заходе в подпапку с сабами
        # и возврате обратно).
        self.checked_paths_data = {}

        # get from settings
        self.template = self.settings_db.get("files_template")
        self.folder_name = self.settings_db.get("folder_template")
        self.poster_template = self.settings_db.get("poster_template")
        self.banner_template = self.settings_db.get("banner_template")
        self.torrent_template = self.settings_db.get("torrent_template") 

        self.populate_tree(folder_path)
        self.insert_data()

        # Сразу при открытии окна отмечаем видеофайлы, подходящие под
        # текущие Episodes/Start from/Type — не дожидаясь debounce-таймера
        # предпросмотра (который тоже это сделает при последующих правках
        # полей).
        self._auto_select_video_files()
        self.populate_tree(self.ui.path_lineEdit.text())
        
        self.ui.save_poster_checkBox.toggled.connect(lambda: self.handle_checkboxes('save_poster_checkBox'))
        self.ui.save_banner_checkBox.toggled.connect(lambda: self.handle_checkboxes('save_banner_checkBox'))
        self.ui.rename_folder_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_folder_checkBox'))
        self.ui.rename_subs_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_subs_checkBox'))
        self.ui.rename_dubs_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_dubs_checkBox'))
        self.ui.show_only_video_files_checkBox.toggled.connect(lambda: self.populate_tree(self.current_dir))
        self.ui.preview_treeWidget.itemDoubleClicked.connect(self.open_item)
        # Клик по галочке файла/папки в дереве должен пересчитывать превью
        self.ui.preview_treeWidget.itemChanged.connect(self.on_tree_item_changed)
        self.ui.back_pushButton.pressed.connect(self.back)
        self.ui.refresh_pushButton.pressed.connect(self.refresh)
        self.ui.forward_pushButton.pressed.connect(self.forward)
        self.ui.preview_checkBox.toggled.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))


        self.ui.template_pushButton.pressed.connect(self.show_template_info)
        self.ui.folder_name_pushButton.pressed.connect(self.show_template_info)
        self.ui.torrent_name_pushButton.pressed.connect(self.show_template_info)

        self.ui.rename_torrent_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_torrent_checkBox'))
        
        self.handle_checkboxes()


    def accept(self):
        print("Rename dialog OK")
    
        if not self.handle_errors():
            return

        # Ничего не отмечено галочками — ничего не переименовываем. Раньше
        # тут был неявный fallback "если пусто — берём всю папку", из-за
        # которого можно было случайно переименовать вообще всё, просто
        # ничего не выбрав.
        checked_items = self.get_checked_items()
        if not checked_items:
            QMessageBox.information(
                self,
                "Nothing selected",
                "No files are checked for renaming. Check the files you want to rename in the tree and try again."
            )
            return

        title = self.parent.current_library_widget.selectedItems()[0].text(0) if self.parent.current_library_widget.selectedItems() else 'Unknown'
        
        self.loading_window = LoadingDialog(f'Renaming files for {title}...', 'Processing...', self)
        self.loading_window.show()

        config = self._build_config()
        rename_queue = RenamerService.build_queue(config, checked_items)

        self.save_pictures()

        torrent_obj = None
        if config.use_qbit and hasattr(self, "qbitClient"):
            torrent_obj = self.qbitClient.find_torrent_by_content_path(self.folder_path)
            if not torrent_obj:
                print("Торрент не найден в qBittorrent. Переключаемся на обычный режим.")
                config.use_qbit = False

        # Папку переименовываем ПОСЛЕ файлов (см. RenameWorker) — но новое
        # имя и сам факт переименования нужно знать заранее: и для бэкапа,
        # и чтобы передать воркеру.
        folder_rename = None
        if config.rename_folder:
            new_folder_name = RenamerService.generate_name(config.folder_template, config)
            if new_folder_name:
                parent_dir = os.path.dirname(os.path.normpath(self.folder_path))
                new_folder_path = os.path.normpath(os.path.join(parent_dir, new_folder_name))
                if new_folder_path != os.path.normpath(self.folder_path):
                    folder_rename = (self.folder_path, new_folder_path)

        # Имя торрента в клиенте (не путь на диске) — отдельная галочка,
        # требует найденного torrent_obj.
        new_torrent_name = None
        if config.rename_torrent and config.use_qbit and torrent_obj:
            generated_name = RenamerService.generate_name(config.torrent_template, config)
            if generated_name:
                new_torrent_name = generated_name

        # Перед реальным переименованием сохраняем скрытый файл со снимком
        # оригинального содержимого папки, картой old_name -> new_name для
        # файлов и (если применимо) переименования самой папки. Это
        # делается ДО запуска воркера, пока старые пути ещё существуют на
        # диске. Сбой создания снимка не должен блокировать переименование —
        # просто логируем и продолжаем.
        try:
            RenamerService.create_backup_snapshot(self.folder_path, rename_queue, folder_rename=folder_rename)
        except OSError as e:
            print(f"Не удалось создать резервный файл с оригинальными именами: {e}")

        self.worker = RenameWorker(
            rename_queue=rename_queue,
            config=config,
            qbit_client=self.qbitClient if config.use_qbit else None,
            torrent_obj=torrent_obj,
            folder_rename=folder_rename,
            new_torrent_name=new_torrent_name,
            parent=self
        )

        self.worker.completed.connect(self.finish_rename)
        self.worker.error_occurred.connect(self.show_error_dialog)
        self.worker.start()

    def finish_rename(self):
        """Вызывается по завершении работы RenameWorker."""
        # Закрываем диалог загрузки, если он открыт
        if hasattr(self, 'loading_window') and self.loading_window:
            self.loading_window.close()
            self.loading_window = None

        print("Переименование успешно завершено!")

        # Если нужно обновить список файлов в UI или закрыть само окно:
        # self.populate_tree()  # Обновить список файлов, если окно остаётся открытым
        super().accept()  # Закрывает диалоговое окно RenameWindow с результатом QDialog.Accepted

    def show_error_dialog(self, error_msg):
        from PySide6.QtWidgets import QMessageBox
        text = error_msg if error_msg else "Unknown error occurred."
        QMessageBox.critical(self, "Error", text)

    def generate_name(self, template: str = "", episode: int = 0) -> str:
        """Прокси-метод для безопасного вызова генератора имён из RenamerService."""
        config = self._build_config()
        return RenamerService.generate_name(template, config, episode)



    def handle_errors(self):
        file_template = self.ui.template_lineEdit.text().strip()
        folder_template = self.ui.folder_name_lineEdit.text().strip()
        poster_name = self.generate_name(self.ui.save_poster_lineEdit.text())
        banner_name = self.generate_name(self.ui.save_banner_lineEdit.text())
        torrent_template = self.ui.torrent_name_lineEdit.text().strip()
        
        poster_checkbox = self.ui.save_poster_checkBox.isChecked()
        banner_checkbox = self.ui.save_banner_checkBox.isChecked()
        
        header = None
        text = None

        # 1. Проверки на пустые поля
        if not file_template:
            header = 'Template is empty'
            text = "Template can't be empty!"
        elif self.ui.rename_folder_checkBox.isChecked() and not folder_template:
            header = 'Folder name is empty'
            text = "Folder name can't be empty!"
        elif poster_checkbox and not poster_name:
            header = 'Poster file name is empty'
            text = "Poster file name can't be empty!"
        elif banner_checkbox and not banner_name:
            header = 'Banner file name is empty'
            text = "Banner file name can't be empty!"
        elif poster_checkbox and banner_checkbox and poster_name == banner_name:
            header = 'Assets file names conflict'
            text = "Poster and banner file names can't be the same!"
        elif self.qbit and self.ui.rename_torrent_checkBox.isChecked() and not torrent_template:
            header = 'Torrent name is empty'
            text = "Torrent name can't be empty!"
        
        if header and text:
            QMessageBox.warning(self, header, text)
            return False

        test_generated = self.generate_name(file_template, 1)
        if not test_generated:
            QMessageBox.warning(self, 'Invalid template result', "Could not generate name from the current template! Please check the input fields.")
            return False

        names = set()
        root_count = self.ui.preview_treeWidget.topLevelItemCount()
        
        for i in range(root_count):
            item = self.ui.preview_treeWidget.topLevelItem(i)
            if item:
                name = item.text(0)
                
                if INVALID_PATH_CHARS.search(name):
                    QMessageBox.warning(self, 'Invalid file name', f"File name contains invalid characters (\\ / : * ? \" < > |):\n\n{name}")
                    return False

                if name in names:
                    QMessageBox.warning(self, 'File name conflict', f"Found multiple files with the same name: '{name}'. Please check your template fields.")
                    return False
                names.add(name)
        
        return True # No errors found 


    def insert_data(self):
        """Insert data to lineEdits using self.title_data and names of video files in the folder"""
        ...
        data = self.title_data
        folder_path = self.folder_path

        local_data = FileScanner.get_title_local_data(folder_path)
        fansub_groups = local_data.get('groups', '')
        first_group = fansub_groups[0] if fansub_groups else ""
        max_ep = local_data.get('max_ep', '')
        resolution = local_data.get('resolution')
        source = local_data.get('source', '')
        title_romaji = data.get('title_romaji')
        title_native = data.get('title_native')
        title_english = data.get('title_english') 
        season_num = str(data.get('season_num', ''))
        if season_num == 'None':
            season_num = '1'

        format = data.get('format', '')
        if format == 'MOVIE':
            format = 'Movie'
        elif format == 'TV_SHORT':
            format = 'TV Short'
        elif format == 'SPECIAL':
            format = 'Special'

        title = self.prefManager.get_title_title(data.get('anilist_id')) or title_romaji or title_native or title_english

        self.ui.fansub_lineEdit.setText(first_group)

        eps_in_folder_str = '(' + str(max_ep) + ' in folder)' if max_ep > 0 else ''
        self.ui.episodes_in_folder_label.setText(eps_in_folder_str)
        
        self.ui.title_lineEdit.setText(title)
        #self.ui.season_num_lineEdit.setText(str(self.extract_season(title)))
        self.ui.season_num_lineEdit.setText(season_num)
        self.ui.season_lineEdit.setText(data.get('season', ''))
        self.ui.season_year_lineEdit.setText(str(data.get('season_year', '')))
        self.ui.type_comboBox.setCurrentText(format)
        self.ui.studio_lineEdit.setText(data.get('studio', ''))
        self.ui.duration_lineEdit.setText(str(data.get('duration', '')))
        self.ui.episodes_lineEdit.setText(str(data.get('episodes', '')))
        self.ui.start_from_lineEdit.setText('1')
        self.ui.score_lineEdit.setText(str(data.get('score', '')))
        self.ui.status_lineEdit.setText(data.get('status', ''))
        self.ui.resolution_lineEdit.setText(resolution)
        self.ui.source_lineEdit.setText(source)
        self.ui.country_lineEdit.setText(data.get('origin_country'))

        self.ui.template_lineEdit.setText(self.template)
        self.ui.folder_name_lineEdit.setText(self.folder_name)
        self.ui.save_poster_lineEdit.setText(self.poster_template)
        self.ui.save_banner_lineEdit.setText(self.banner_template)
        self.ui.torrent_name_lineEdit.setText(self.torrent_template)

        self.poster_link = data.get('poster_large_link')
        self.banner_link = data.get('banner_link')
        poster_color = data.get('poster_color')

        self.placeholder_poster = self.imgmClient.get_color_pixmap(poster_color, 191, 300).scaledToWidth(191, Qt.TransformationMode.SmoothTransformation)
        self.placeholder_banner = self.imgmClient.get_color_pixmap(poster_color, 998, 300).scaledToWidth(998, Qt.TransformationMode.SmoothTransformation)

        self.ui.poster_label.setPixmap(self.placeholder_poster)
        self.ui.poster_label.setFixedSize(self.placeholder_poster.size())
        self.ui.banner_label.setPixmap(self.placeholder_banner)

        links = [self.poster_link, self.banner_link]
        img_manager = ImageManager()
        worker = DownloadPostersWorker(links, img_manager.posters_path)
        worker.signals.finished.connect(self.on_posters_ready)

        self.parent.thread_pool.start(worker)

    def on_posters_ready(self, posters_data: dict):
        poster_path = posters_data.get(self.poster_link) if self.poster_link else None
        banner_path = posters_data.get(self.banner_link) if self.banner_link else None
        
        if poster_path and os.path.exists(poster_path):
            real_poster = QPixmap(poster_path)
        else:
            real_poster = self.placeholder_poster
            
        if banner_path and os.path.exists(banner_path):
            real_banner = QPixmap(banner_path)
        else:
            real_banner = self.placeholder_banner

        if not real_banner.isNull():
            self.banner = real_banner.scaledToWidth(998, Qt.TransformationMode.SmoothTransformation)
            self.ui.banner_label.setPixmap(self.banner)

        if not real_poster.isNull():
            self.poster = real_poster.scaledToWidth(191, Qt.TransformationMode.SmoothTransformation)
            self.ui.poster_label.setPixmap(self.poster)
            self.ui.poster_label.setFixedSize(self.poster.size())


    def extract_season(self, text: str) -> int:
        patterns = [
            r'\s+(\d+)$',
            r'[sS](\d+)\b',                         # S2, s02
            r'[sS]eason\s*(\d+)',                   # Season 2, season02
            r'[тТ][вВ]-(\d+)',                      # ТВ-2, тв-02
            r'(\d+)\s*(?:season|сезон|nd|rd|th|st)' # 2nd Season, 3 сезон
            r'\s+(?:II|III|IV|V|VI|VII)\b'          # II, III
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                val = int(match.group(1))
                if 1 <= val <= 10:
                    return val
                continue

        if re.search(r'\s+NEXT\b', text, re.IGNORECASE): # NEXT, Next, next
            return 2

        roman_match = re.search(r'\s+(II|III|IV|V|VI|VII)\b', text)
        if roman_match:
            roman_to_int = {'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}
            return roman_to_int[roman_match.group(1)]
            
        k_on_match = re.search(r'[a-zA-Zа-яА-Я]+(!+)', text)
        if k_on_match and len(k_on_match.group(1)) == 2:
            return 2
            
        return 1
        
    def handle_checkboxes(self, checkbox = None):
        if not checkbox or checkbox == 'save_poster_checkBox':
            self.ui.save_poster_lineEdit.setEnabled(self.ui.save_poster_checkBox.isChecked())
        if not checkbox or checkbox == 'save_banner_checkBox':
            self.ui.save_banner_lineEdit.setEnabled(self.ui.save_banner_checkBox.isChecked())
        if not checkbox or checkbox == 'rename_folder_checkBox':
            ischecked = self.ui.rename_folder_checkBox.isChecked()
            self.ui.folder_name_lineEdit.setEnabled(ischecked)
            self.ui.folder_name_label.setEnabled(ischecked)
        if self.qbit and (not checkbox or checkbox == 'rename_torrent_checkBox'):
            ischecked = self.ui.rename_torrent_checkBox.isChecked()
            self.ui.torrent_name_label.setEnabled(ischecked)
            self.ui.torrent_name_lineEdit.setEnabled(ischecked)
            self.ui.torrent_name_arrow_label.setEnabled(ischecked)
            self.ui.torrent_name_preview_label.setEnabled(ischecked)
        if not checkbox or checkbox == 'rename_subs_checkBox':
            self._auto_select_extra_files(SUB_EXTS, self.ui.rename_subs_checkBox.isChecked())
        if not checkbox or checkbox == 'rename_dubs_checkBox':
            self._auto_select_extra_files(DUB_EXTS, self.ui.rename_dubs_checkBox.isChecked())
        self.populate_tree(self.ui.path_lineEdit.text())

    def _auto_select_extra_files(self, extensions, select: bool):
        """Ставит (select=True) или снимает (select=False) галочки со всех
        файлов с указанными расширениями (сабы/дабы) по всей папке релиза
        рекурсивно — включая вложенные подпапки вроде "Subs", в которые
        пользователь мог и не заходить. Технический контент (NCED/NCOP/
        превью и т.п.) пропускается, как и при обычном сканировании."""
        if not self.folder_path or not os.path.isdir(self.folder_path):
            return

        for dirpath, dirnames, filenames in os.walk(self.folder_path):
            for f in filenames:
                if not f.lower().endswith(extensions):
                    continue
                if RenamerService.is_extra(f):
                    continue
                full = os.path.join(dirpath, f).replace('\\', '/')
                if select:
                    self._mark_checked(full)
                else:
                    self._unmark_checked(full)

    def _auto_select_video_files(self):
        """Автоматически отмечает видеофайлы, чей номер серии (распознанный
        из имени файла) попадает в текущий диапазон Episodes/Start from —
        и снимает отметку с тех, что в него не попадают. Вызывается при
        открытии окна и при любом изменении настроек серии/типа, чтобы не
        приходилось искать и отмечать видео вручную каждый раз.

        Если тип релиза — одиночный (Movie/OVA/Special с Episodes=1) и во
        всей папке релиза нашёлся ровно один видеофайл, он отмечается
        безусловно (у одиночных релизов номер серии в имени файла часто
        отсутствует). Если видеофайлов несколько — доверяем только тому,
        что реально распознано в имени файла, чтобы не отметить чужие
        серии, лежащие в той же папке (как в примере с сериалом + OVA)."""
        if not self.folder_path or not os.path.isdir(self.folder_path):
            return

        config = self._build_config()

        if config.episodes_num <= 0 and not config.is_movie:
            # Число серий релиза не задано — надёжно определить диапазон
            # нельзя, галочки на видео не трогаем.
            return

        is_single_release = config.is_movie or (
            config.media_type in ['MOVIE', 'OVA', 'SPECIAL'] and config.episodes_num == 1
        )
        max_allowed_ep = (
            config.start_from_ep + config.episodes_num - 1
            if config.episodes_num > 0 else config.start_from_ep
        )

        candidates = []
        for dirpath, dirnames, filenames in os.walk(self.folder_path):
            for f in filenames:
                if not f.lower().endswith(VIDEO_EXTS):
                    continue
                if RenamerService.is_extra(f):
                    continue
                candidates.append(os.path.join(dirpath, f).replace('\\', '/'))

        single_candidate = is_single_release and len(candidates) == 1

        for full in candidates:
            if single_candidate:
                matches = True
            else:
                parsed_ep = RenamerService.extract_episode(os.path.basename(full), config.episodes_num)
                matches = parsed_ep is not None and config.start_from_ep <= parsed_ep <= max_allowed_ep

            if matches:
                self._mark_checked(full)
            else:
                self._unmark_checked(full)
    
    def save_pictures(self):
        self.poster_link = self.title_data.get('poster_large_link')
        self.banner_link = self.title_data.get('banner_link')
        links = []

        # Poster
        if self.ui.save_poster_checkBox.isChecked() and self.poster_link:
            links.append(self.poster_link)
            
        # Banner
        if self.ui.save_banner_checkBox.isChecked() and self.banner_link:
            links.append(self.banner_link)
            
        if links:
            worker = DownloadPostersWorker(links, self.imgmClient.posters_path)
            worker.signals.finished.connect(self.on_pictures_ready)
            QThreadPool.globalInstance().start(worker)

    def on_pictures_ready(self, pics: dict[str, str]):
        # Poster
        poster_src = pics.get(self.poster_link)
        if poster_src:
            _, poster_src_ext = os.path.splitext(poster_src)
            poster_name = (self.ui.save_poster_lineEdit.text() or 'poster')
            poster_name = self.generate_name(poster_name)
            poster_name = poster_name + poster_src_ext
            poster_dst = os.path.join(self.folder_path, poster_name).replace('\\', '/')

            try:
                if os.path.abspath(poster_src) != os.path.abspath(poster_dst):
                    shutil.copy2(poster_src, poster_dst)
            except OSError as e:
                # Например, self.folder_path успели переименовать (галочка
                # "Rename folder") пока постер ещё качался в фоне.
                print(f"Не удалось сохранить постер в {poster_dst}: {e}")

        # Banner
        banner_src = pics.get(self.banner_link)
        if banner_src:
            _, banner_src_ext = os.path.splitext(banner_src)
            
            banner_name = (self.ui.save_banner_lineEdit.text() or 'banner')
            banner_name = self.generate_name(banner_name)
            banner_name = banner_name + banner_src_ext
            banner_dst = os.path.join(self.folder_path, banner_name).replace('\\', '/')

            try:
                if os.path.abspath(banner_src) != os.path.abspath(banner_dst):
                    shutil.copy2(banner_src, banner_dst)
            except OSError as e:
                print(f"Не удалось сохранить баннер в {banner_dst}: {e}")

    def populate_tree(self, folder_path):
        preview = self.ui.preview_checkBox.isChecked()
        widget = self.ui.preview_treeWidget
        items = FileScanner.get_items(folder_path)
        current_dir = folder_path

        # Запоминаем отмеченные пути ДО очистки дерева, чтобы не терять
        # галочки пользователя при каждом перестроении превью.
        # Если вызов пришёл из-за клика по чекбоксу (on_tree_item_changed),
        # состояние в дереве уже обновлено на момент этого вызова.
        previously_checked_paths = {
            item['path'] for item in self.get_checked_items()
        }

        self.ui.path_lineEdit.setText(folder_path)
        config = self._build_config()
        only_video = self.ui.show_only_video_files_checkBox.isChecked()

        # Блокируем сигналы на время перестройки дерева, иначе setCheckState/
        # setText ниже будут заново вызывать itemChanged -> populate_tree
        # (бесконечная рекурсия) и сбрасывать только что расставленные галочки.
        widget.blockSignals(True)
        try:
            widget.headerItem().setText(0, 'Folder')
            widget.clear()

            preview_map = {}

            if preview:
                # Превью строится ТОЛЬКО по отмеченным галочками файлам —
                # так же, как реально работает переименование. Если ничего
                # не отмечено, превью пустое (имена остаются как есть), а
                # не "как переименовалась бы вся папка" — иначе превью
                # обманывало бы про итоговый результат.
                preview_source_items = [
                    d for d in items if d['path'] in previously_checked_paths
                ]

                rename_queue = RenamerService.build_queue(config, preview_source_items)
                for old_path, new_path in rename_queue:
                    preview_map[old_path] = os.path.basename(new_path)

                if self.ui.save_poster_checkBox.isChecked():
                    poster_file_name = self.generate_name(self.ui.save_poster_lineEdit.text())
                    poster_path = os.path.join(self.folder_path, poster_file_name).replace('\\', '/')
                    preview_map[poster_path] = os.path.basename(poster_file_name)
                if self.ui.save_banner_checkBox.isChecked():
                    banner_file_name = self.generate_name(self.ui.save_banner_lineEdit.text())
                    banner_path = os.path.join(self.folder_path, banner_file_name).replace('\\', '/')
                    preview_map[banner_path] = os.path.basename(banner_file_name)

            # Отрисовка элементов с поддержкой галочек
            for data in items:
                if only_video and not data['name'].lower().endswith(VIDEO_EXTS):
                    continue

                item = QTreeWidgetItem(widget)
                item.setData(0, PATH_ROLE, data['path'])
                # Храним исходное имя файла отдельно от текста, который
                # мы подменяем на превью — иначе повторный пересчёт превью
                # брал бы уже переименованный текст как "исходное" имя.
                item.setData(0, ORIGINAL_NAME_ROLE, data['name'])

                # Включаем чекбокс для элемента
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                # Восстанавливаем состояние галочки. Для папок состояние —
                # не то, что когда-то было явно проставлено на самой папке
                # (мы это больше не храним), а вычисляется на лету по её
                # содержимому: полностью/частично/не отмечена.
                if data.get('is_dir'):
                    restored_state = self._compute_dir_check_state(data['path'])
                else:
                    restored_state = (
                        Qt.CheckState.Checked
                        if data['path'] in previously_checked_paths
                        else Qt.CheckState.Unchecked
                    )
                item.setCheckState(0, restored_state)

                if preview and data['path'] in preview_map:
                    item.setText(0, preview_map[data['path']])
                else:
                    item.setText(0, data['name'])

                icon_type = QStyle.SP_DirIcon if data.get('is_dir') else QStyle.SP_FileIcon
                item.setIcon(0, self.style().standardIcon(icon_type))

            if preview and self.ui.save_poster_checkBox.isChecked() and folder_path == self.folder_path:
                poster_name = self.generate_name(self.ui.save_poster_lineEdit.text())
                item = QTreeWidgetItem(widget)
                item.setText(0, poster_name)
                poster_path = os.path.join(self.folder_path, poster_name).replace('\\', '/')
                item.setData(0, PATH_ROLE, poster_path)
                item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))

            if preview and self.ui.save_banner_checkBox.isChecked() and folder_path == self.folder_path:
                banner_name = self.generate_name(self.ui.save_banner_lineEdit.text())
                item = QTreeWidgetItem(widget)
                item.setText(0, banner_name)
                banner_path = os.path.join(self.folder_path, banner_name).replace('\\', '/')
                item.setData(0, PATH_ROLE, banner_path)
                item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))
        finally:
            widget.blockSignals(False)

        self.ui.back_pushButton.setEnabled(len(self.history) > 0)
        self.ui.forward_pushButton.setEnabled(len(self.forward_stack) > 0)
        self.ui.refresh_pushButton.setEnabled(True if current_dir else False)

        if preview and self.ui.rename_folder_checkBox.isChecked() and folder_path == self.folder_path:
            preview_folder_name = self.generate_name(self.ui.folder_name_lineEdit.text())
            widget.setHeaderLabel(preview_folder_name)
        else:
            widget.setHeaderLabel(os.path.basename(folder_path))

        if self.qbit:
            torrent_name_preview = RenamerService.generate_name(
                template=self.ui.torrent_name_lineEdit.text(),
                config=config,
                episode=0
            )
            self.ui.torrent_name_preview_label.setText(torrent_name_preview)

    def on_tree_item_changed(self, item, column):
        """Срабатывает при клике по чекбоксу файла/папки в дереве превью.

        ВАЖНО: здесь нельзя вызывать populate_tree() / widget.clear() — это
        происходило бы синхронно прямо во время обработки клика в самом
        QTreeWidget (item пересоздаётся, пока Qt ещё обрабатывает нажатие на
        него), из-за чего чекбоксы переставали реагировать на клики вообще.
        Поэтому просто обновляем текст (превью-имя) существующих элементов,
        не трогая сами чекбоксы и не пересоздавая дерево.
        """
        if column != 0:
            return
        if getattr(self, '_updating_preview_texts', False):
            return

        # Синхронизируем постоянное хранилище галочек с тем, что реально
        # кликнул пользователь. Это единственное место, где галочки
        # добавляются/убираются из self.checked_paths_data — восстановление
        # состояния в populate_tree сигналы не шлёт (blockSignals), поэтому
        # рекурсии тут не будет.
        path = item.data(0, PATH_ROLE)
        if path:
            if item.checkState(0) == Qt.CheckState.Checked:
                self._mark_checked(path)
            else:
                self._unmark_checked(path)

        self.refresh_preview_texts()

    def _mark_checked(self, root_path):
        """Отмечает root_path как выбранный. Если это папка — каскадно
        отмечает всё её содержимое (рекурсивно). Сама папка как отдельная
        запись в checked_paths_data НЕ хранится — состояние её чекбокса
        всегда вычисляется на лету по вложенным файлам
        (см. _compute_dir_check_state). Благодаря этому точечное снятие
        галочки с одного файла внутри ранее отмеченной папки корректно
        переводит папку в частично отмеченное состояние, а не остаётся
        "залипшей" в Checked."""
        if os.path.isdir(root_path):
            for dirpath, dirnames, filenames in os.walk(root_path):
                for f in filenames:
                    full = os.path.join(dirpath, f).replace('\\', '/')
                    self.checked_paths_data[full] = {'name': f, 'path': full, 'is_dir': False}
        else:
            self.checked_paths_data[root_path] = {
                'name': os.path.basename(root_path),
                'path': root_path,
                'is_dir': False,
            }

    def _unmark_checked(self, root_path):
        """Снимает отметку с root_path. Если это папка — каскадно снимает
        отметку со всего содержимого (рекурсивно)."""
        if os.path.isdir(root_path):
            for dirpath, dirnames, filenames in os.walk(root_path):
                for f in filenames:
                    full = os.path.join(dirpath, f).replace('\\', '/')
                    self.checked_paths_data.pop(full, None)
        else:
            self.checked_paths_data.pop(root_path, None)

    def _compute_dir_check_state(self, dir_path):
        """Возвращает состояние чекбокса папки — Checked, если отмечены
        ВСЕ файлы внутри неё (рекурсивно), Unchecked, если ни одного, и
        PartiallyChecked, если только часть. Вычисляется на лету при
        каждом показе дерева, а не хранится, чтобы всегда быть в
        актуальном состоянии независимо от того, где именно (в каком
        вложенном подкаталоге) были сняты/поставлены отдельные галочки."""
        total = 0
        checked = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for f in filenames:
                total += 1
                full = os.path.join(dirpath, f).replace('\\', '/')
                if full in self.checked_paths_data:
                    checked += 1

        if total == 0 or checked == 0:
            return Qt.CheckState.Unchecked
        if checked == total:
            return Qt.CheckState.Checked
        return Qt.CheckState.PartiallyChecked

    def refresh_preview_texts(self):
        """Лёгкое обновление текста элементов дерева под текущий набор
        отмеченных галочками файлов, без clear()/пересоздания элементов."""
        widget = self.ui.preview_treeWidget
        if not self.ui.preview_checkBox.isChecked():
            return

        config = self._build_config()
        checked_items = self.get_checked_items()

        # Как и при реальном переименовании: ничего не отмечено — превью
        # пустое, а не "как будто отмечена вся папка".
        rename_queue = RenamerService.build_queue(config, checked_items) if checked_items else []
        preview_map = {old: os.path.basename(new) for old, new in rename_queue}

        self._updating_preview_texts = True
        try:
            for i in range(widget.topLevelItemCount()):
                tree_item = widget.topLevelItem(i)
                path = tree_item.data(0, PATH_ROLE)
                if not path:
                    continue
                original_name = tree_item.data(0, ORIGINAL_NAME_ROLE) or os.path.basename(path)
                new_text = preview_map.get(path, original_name)
                if tree_item.text(0) != new_text:
                    tree_item.setText(0, new_text)
        finally:
            self._updating_preview_texts = False

    def get_checked_items(self):
        # Берём накопленные галочки из постоянного хранилища
        return [dict(data) for data in self.checked_paths_data.values()]
        
    def open_item(self, item, column):
        if item:
            path = item.data(0, PATH_ROLE)
            if path:
                if os.path.isdir(path):
                    current_dir = self.ui.path_lineEdit.text()
                    self.current_dir = path
                    if current_dir:
                        self.history.append(current_dir)
                        self.forward_stack.clear()
                    self.populate_tree(path)
                else:
                    #self.open_file(path)
                    pass

    def open_file(self, path):
        file_url = QUrl.fromLocalFile(path)
        QDesktopServices.openUrl(file_url)

    def back(self):
        if self.history:
            current_dir = self.ui.path_lineEdit.text()
            last_folder = self.history.pop()
            self.forward_stack.append(current_dir)
            self.populate_tree(last_folder)
            self.current_dir = last_folder
            
    
    def refresh(self):
        current_dir = self.ui.path_lineEdit.text()
        self.current_dir = current_dir
        if current_dir:
            self.populate_tree(current_dir)
            self.ui.preview_treeWidget.scrollToTop()

    def forward(self):
        if self.forward_stack:
            current_dir = self.ui.path_lineEdit.text()
            self.history.append(current_dir)
            
            next_folder = self.forward_stack.pop()
            self.populate_tree(next_folder)
            self.current_dir = next_folder


    def show_template_info(self):
        ui = self.ui
        episodes = ui.episodes_lineEdit.text()
        padding = max(2, len(episodes))
        formatted_ep = str(ui.start_from_lineEdit.text()).zfill(padding)

        if 'p' not in ui.resolution_lineEdit.text():
            quality = ui.resolution_lineEdit.text().split('x')[-1]+'p'
        else:
            quality = ui.resolution_lineEdit.text().split('x')[-1]

        text = 'You can use these variables to automatically insert title information.\n\n' + \
            '{title} → ' + f'{ui.title_lineEdit.text()}\n' + \
            '{season_num} → ' + f'{ui.season_num_lineEdit.text().zfill(2)}\n' + \
            '{season} → ' + f'{ui.season_lineEdit.text()}\n' + \
            '{year} → ' + f'{ui.season_year_lineEdit.text()}\n' + \
            '{type} → ' + f'{ui.type_comboBox.currentText()}\n' + \
            '{studio} → ' + f'{ui.studio_lineEdit.text()}\n' + \
            '{duration} → ' + f'{ui.duration_lineEdit.text()}\n' + \
            '{source} → ' + f'{ui.source_lineEdit.text()}\n' + \
            '{resolution} → ' + f'{ui.resolution_lineEdit.text()}\n' + \
            "{height} → " + f"{ui.resolution_lineEdit.text().split('x')[-1]}\n" + \
            "{width} → " + f"{ui.resolution_lineEdit.text().split('x')[0]}\n" + \
            '{quality} → ' + f'{quality}\n' + \
            '{fansub} → ' + f'{ui.fansub_lineEdit.text()}\n' + \
            '{score} → ' + f'{ui.score_lineEdit.text()}\n' + \
            '{status} → ' + f'{ui.status_lineEdit.text()}\n' + \
            '{episodes} → ' + f'{ui.episodes_lineEdit.text()}\n' + \
            '{country} → ' + f'{ui.country_lineEdit.text()}\n' + \
            '{episode} → ' + f'{formatted_ep}'
        

        QMessageBox.information(self, "Template info", text)

    


    def _build_config(self) -> RenameConfig:
        """Собирает все текущие настройки из элементов GUI в один объект RenameConfig."""
        ui = self.ui

        return RenameConfig(
            folder_path=self.folder_path,
            template=ui.template_lineEdit.text(),
            folder_template=ui.folder_name_lineEdit.text(),
            torrent_template=ui.torrent_name_lineEdit.text(),
            # Метаданные релиза
            title=ui.title_lineEdit.text(),
            season_num=ui.season_num_lineEdit.text(),
            season=ui.season_lineEdit.text(),
            year=ui.season_year_lineEdit.text(),
            media_type=ui.type_comboBox.currentText(),
            studio=ui.studio_lineEdit.text(),
            duration=ui.duration_lineEdit.text(),
            source=ui.source_lineEdit.text(),
            resolution=ui.resolution_lineEdit.text(),
            fansub=ui.fansub_lineEdit.text(),
            score=ui.score_lineEdit.text(),
            status=ui.status_lineEdit.text(),
            country=ui.country_lineEdit.text(),
            # Флаги
            rename_subs=ui.rename_subs_checkBox.isChecked(),
            rename_dubs=ui.rename_dubs_checkBox.isChecked(),
            rename_folder=ui.rename_folder_checkBox.isChecked(),
            rename_torrent=ui.rename_torrent_checkBox.isChecked() if self.qbit else False,
            # Режимы серий
            is_movie=ui.type_comboBox.currentText().strip().upper() == 'MOVIE',
            episodes_num=int(ui.episodes_lineEdit.text()) if ui.episodes_lineEdit.text().isdigit() else 0,
            start_from_ep=int(ui.start_from_lineEdit.text()) if ui.start_from_lineEdit.text().isdigit() else 1,
            # qBittorrent
            use_qbit=self.qbit
        )