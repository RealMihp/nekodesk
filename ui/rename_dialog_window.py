import PySide6
from PySide6.QtWidgets import *
import anitopy
from core.logic import FileScanner
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

import sys, os, shutil, re

from ui.ui_rename_dialog import *
from core.db import *
from core.utils import *
from core.api.anilist_api import *
from core.logic import FileScanner

VIDEO_EXTS = ('.mp4', '.mkv', '.avi')
SUB_EXTS = ('.ass', '.srt', '.ssa', '.vtt')
DUB_EXTS = ('.mka', '.mp3', '.aac', '.ac3', '.flac')
PATH_ROLE = 32

class RenameWindow(QDialog):
    def __init__(self, parent=None, title_data: dict = {}, folder_path: str = ""):
        super().__init__(parent)
        self.ui = Ui_RenameDialog()
        self.ui.setupUi(self)
        self.imgmClient = ImageManager()
        self.filemClient = FileManager()
        self.history = []
        self.forward_stack = []
        self.title_data = title_data
        self.folder_path = folder_path
        self.current_dir = folder_path

        # get from settings
        self.template = '{title} S{season_num}E{episode} [{source} {quality}]'
        self.folder_name = '{title} S{season_num} [{source}] [{quality}]'
        self.save_poster_file_name = 'poster'
        self.save_banner_file_name = 'banner'   

        self.populate_tree(folder_path)
        self.insert_data()
        
        self.ui.save_poster_checkBox.toggled.connect(lambda: self.handle_checkboxes('save_poster_checkBox'))
        self.ui.save_banner_checkBox.toggled.connect(lambda: self.handle_checkboxes('save_banner_checkBox'))
        self.ui.rename_folder_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_folder_checkBox'))
        self.ui.rename_subs_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_subs_checkBox'))
        self.ui.rename_dubs_checkBox.toggled.connect(lambda: self.handle_checkboxes('rename_dubs_checkBox'))
        self.ui.show_only_video_files_checkBox.toggled.connect(lambda: self.populate_tree(self.current_dir))
        self.ui.preview_treeWidget.itemDoubleClicked.connect(self.open_item)
        self.ui.back_pushButton.pressed.connect(self.back)
        self.ui.refresh_pushButton.pressed.connect(self.refresh)
        self.ui.forward_pushButton.pressed.connect(self.forward)
        self.ui.preview_checkBox.toggled.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))

        self.ui.title_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.season_num_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.season_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.season_year_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.type_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.studio_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.duration_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.source_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.resolution_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.fansub_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.country_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.score_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.status_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.episodes_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.start_from_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))

        self.ui.template_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.folder_name_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))

        self.ui.save_poster_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))
        self.ui.save_banner_lineEdit.textChanged.connect(lambda: self.populate_tree(self.ui.path_lineEdit.text()))




        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def render_preview_tree(self):
        """Render the preview treeWidget"""
        ...

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

        title = title_romaji or title_native or title_english or ''

        self.ui.fansub_lineEdit.setText(first_group)

        eps_in_folder_str = '(' + str(max_ep) + ' in folder)' if max_ep > 0 else ''
        self.ui.episodes_in_folder_label.setText(eps_in_folder_str)
        
        self.ui.title_lineEdit.setText(title)
        self.ui.season_num_lineEdit.setText(str(self.extract_season(title)))
        self.ui.season_lineEdit.setText(data.get('season', ''))
        self.ui.season_year_lineEdit.setText(str(data.get('season_year', '')))
        self.ui.type_lineEdit.setText(data.get('format', '').capitalize() if data.get('format', '') == 'MOVIE' else data.get('format', ''))
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
        self.ui.save_poster_lineEdit.setText(self.save_poster_file_name)
        self.ui.save_banner_lineEdit.setText(self.save_banner_file_name)

        poster_link = data.get('poster_large_link')
        poster_color = data.get('poster_color')
        poster = self.imgmClient.get_poster(poster_link, return_pixmap=True) if poster_link else self.imgmClient.get_color_icon(poster_color)
        placeholder_poster = self.imgmClient.get_color_pixmap(poster_color, 460, 690)
        banner_link = data.get('banner_link')
        placeholder_banner = self.imgmClient.get_color_pixmap(poster_color, 1900, 400)
        banner = self.imgmClient.get_poster(banner_link, return_pixmap=True) if banner_link else placeholder_banner

        if not banner.isNull():
            banner = banner.scaledToWidth(998, Qt.TransformationMode.SmoothTransformation)
            self.ui.banner_label.setPixmap(banner)
            

        if not poster.isNull():
            poster = poster.scaledToWidth(191, Qt.TransformationMode.SmoothTransformation)
            self.ui.poster_label.setPixmap(poster)
            self.ui.poster_label.setFixedSize(poster.size())

        self.ui.banner_label.setPixmap(banner)
        self.ui.poster_label.setPixmap(poster)


    def extract_season(self, text: str) -> int:
        patterns = [
            r'\s+(\d+)$',
            r'[sS](\d+)\b',                         # S2, s02
            r'[sS]eason\s*(\d+)',                   # Season 2, season02
            r'[тТ][вВ]-(\d+)',                      # ТВ-2, тв-02
            r'(\d+)\s*(?:season|сезон|nd|rd|th|st)' # 2nd Season, 3 сезон
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                val = int(match.group(1))
                if 1 <= val <= 10:
                    return val
                continue
            
        k_on_match = re.search(r'[a-zA-Zа-яА-Я]+(!+)', text)
        if k_on_match and len(k_on_match.group(1)) == 2:
            return 2
            
        return 1
        
    def handle_checkboxes(self, checkbox):
        if checkbox == 'save_poster_checkBox':
            self.ui.save_poster_lineEdit.setEnabled(self.ui.save_poster_checkBox.isChecked())
        elif checkbox == 'save_banner_checkBox':
            self.ui.save_banner_lineEdit.setEnabled(self.ui.save_banner_checkBox.isChecked())
        elif checkbox == 'rename_folder_checkBox':
            self.ui.folder_name_lineEdit.setEnabled(self.ui.rename_folder_checkBox.isChecked())
        elif checkbox == 'rename_subs_checkBox':
            pass
        elif checkbox == 'rename_dubs_checkBox':
            pass
        self.populate_tree(self.ui.path_lineEdit.text())
    
    def save_pictures(self):
        poster_link = self.title_data.get('poster_large_link')
        banner_link = self.title_data.get('banner_link')
        
        imgmClient = ImageManager(posters_path=self.folder_path)
        # Poster
        if self.ui.save_poster_checkBox.isChecked() and poster_link:
            poster_src = imgmClient.get_poster(poster_link, return_pixmap=False, is_temp=False)
            if poster_src:
                _, poster_src_ext = os.path.splitext(poster_src)
                
                poster_name = (self.ui.save_poster_lineEdit.text() or 'poster') + poster_src_ext
                poster_dst = os.path.join(self.folder_path, poster_name).replace('\\', '/')

                if os.path.abspath(poster_src) != os.path.abspath(poster_dst):
                    shutil.copy2(poster_src, poster_dst)

        # Banner
        if self.ui.save_banner_checkBox.isChecked() and banner_link:
            banner_src = imgmClient.get_poster(banner_link, return_pixmap=False, is_temp=False)
            if banner_src:
                _, banner_src_ext = os.path.splitext(banner_src)
                
                banner_name = (self.ui.save_banner_lineEdit.text() or 'banner') + banner_src_ext
                banner_dst = os.path.join(self.folder_path, banner_name).replace('\\', '/')

                if os.path.abspath(banner_src) != os.path.abspath(banner_dst):
                    shutil.copy2(banner_src, banner_dst)

    def populate_tree(self, folder_path):
        preview = self.ui.preview_checkBox.isChecked()
        widget = self.ui.preview_treeWidget
        items = FileScanner.get_items(folder_path)
        current_dir = folder_path

        self.ui.path_lineEdit.setText(folder_path)
        
        
        only_video = self.ui.show_only_video_files_checkBox.isChecked()
        widget.headerItem().setText(0, 'Folder')
        widget.clear()

        exts = VIDEO_EXTS
        exts = exts + SUB_EXTS if self.ui.rename_subs_checkBox.isChecked() else exts
        exts = exts + DUB_EXTS if self.ui.rename_dubs_checkBox.isChecked() else exts
            
        
        # subs & dubs
        allitems = items.copy()
        if self.ui.rename_subs_checkBox.isChecked():
            for data in items:
                if 'sub' in data['name'].lower() and data['is_dir'] and folder_path == data['path']:
                    subfiles = []
                    subitems = FileScanner.get_items(data['path'])
                    
                    for subitem in subitems:
                        if subitem['name'].lower().endswith(SUB_EXTS) and folder_path == subitem['path']:
                            subfiles.append(subitem)
                        
                        elif subitem['is_dir']:
                            nested_items = FileScanner.get_items(subitem['path'])
                            for nested_item in nested_items:
                                if nested_item['name'].lower().endswith(SUB_EXTS) and folder_path == nested_item['path']:
                                    subfiles.append(nested_item)
                    
                    allitems.extend(subfiles)
        if self.ui.rename_dubs_checkBox.isChecked():
            for data in items:
                if any(word in data['name'].lower() for word in ('dub', 'sound')) and data['is_dir'] and folder_path == data['path']:
                    dubfiles = []
                    dubitems = FileScanner.get_items(data['path'])
                    
                    for dubitem in dubitems:
                        if dubitem['name'].lower().endswith(DUB_EXTS) and folder_path == data['path']:
                            dubfiles.append(dubitem)
                        
                        elif dubitem['is_dir']:
                            nested_items = FileScanner.get_items(dubitem['path'])
                            for nested_item in nested_items:
                                if nested_item['name'].lower().endswith(DUB_EXTS) and folder_path == data['path']:
                                    dubfiles.append(nested_item)
                    
                    allitems.extend(dubfiles)
        
        items = allitems

        preview_map = {}

        if preview:
            eps_num = int(self.ui.episodes_lineEdit.text())
            start_from_ep = int(self.ui.start_from_lineEdit.text())
            eps_tuple = tuple(range(start_from_ep, eps_num + 1))

            for data in items:
                file_name = data['name']
                file_path = data['path']

                if file_name.lower().endswith(exts):
                    parsed_data = anitopy.parse(file_name)
                    if parsed_data and parsed_data.get('episode_number'):
                        try:
                            parsed_ep = int(parsed_data.get('episode_number'))
                        except ValueError:
                            continue
                        
                        if parsed_ep in eps_tuple:
                            ext = os.path.splitext(file_name)[1]
                            base_new_name = self.generate_name(self.ui.template_lineEdit.text(), parsed_ep)
                            new_name = base_new_name + ext
                            
                            preview_map[file_path] = os.path.basename(new_name)

            # Picters preview
            if self.ui.save_poster_checkBox.isChecked():
                poster_file_name = self.ui.save_poster_lineEdit.text()
                poster_path = os.path.join(self.folder_path, poster_file_name).replace('\\', '/')
                preview_map[poster_path] = os.path.basename(poster_file_name)
            if self.ui.save_banner_checkBox.isChecked():
                banner_file_name = self.ui.save_banner_lineEdit.text()
                banner_path = os.path.join(self.folder_path, banner_file_name).replace('\\', '/')
                preview_map[banner_path] = os.path.basename(banner_file_name)



        for data in items:
            if only_video and not data['name'].lower().endswith(VIDEO_EXTS):
                continue

            item = QTreeWidgetItem(widget)
            item.setData(0, PATH_ROLE, data['path'])

            if preview and data['path'] in preview_map:
                item.setText(0, preview_map[data['path']])
            else:
                item.setText(0, data['name'])

            icon_type = QStyle.SP_DirIcon if data['is_dir'] else QStyle.SP_FileIcon
            item.setIcon(0, self.style().standardIcon(icon_type))

        if preview and self.ui.save_poster_checkBox.isChecked() and folder_path == self.folder_path:
                poster_name = self.ui.save_poster_lineEdit.text()
                item = QTreeWidgetItem(widget)
                item.setText(0, poster_name)

                poster_path = os.path.join(self.folder_path, poster_name).replace('\\', '/')
                item.setData(0, PATH_ROLE, poster_path)
                item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))

        if preview and self.ui.save_banner_checkBox.isChecked() and folder_path == self.folder_path:
            banner_name = self.ui.save_banner_lineEdit.text()
            item = QTreeWidgetItem(widget)
            item.setText(0, banner_name)

            banner_path = os.path.join(self.folder_path, banner_name).replace('\\', '/')
            item.setData(0, PATH_ROLE, banner_path)
            item.setIcon(0, self.style().standardIcon(QStyle.SP_FileIcon))

        self.ui.back_pushButton.setEnabled(len(self.history) > 0)
        self.ui.forward_pushButton.setEnabled(len(self.forward_stack) > 0)
            
        self.ui.refresh_pushButton.setEnabled(True if current_dir else False)

        # Header text
        if preview and self.ui.rename_folder_checkBox.isChecked() and folder_path == self.folder_path:
            preview_folder_name = self.generate_name(self.ui.folder_name_lineEdit.text())
            widget.setHeaderLabel(preview_folder_name)
        else:
            widget.setHeaderLabel(os.path.basename(folder_path))


        
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
                    self.open_file(path)

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


    def rename(self):
        # Files
        items = FileScanner.get_items(self.folder_path)
    
        exts = VIDEO_EXTS
        exts = exts + SUB_EXTS if self.ui.rename_subs_checkBox.isChecked() else exts
        exts = exts + DUB_EXTS if self.ui.rename_dubs_checkBox.isChecked() else exts

        # subs & dubs
        allitems = items.copy()
        if self.ui.rename_subs_checkBox.isChecked():
            for data in items:
                if 'sub' in data['name'].lower() and data['is_dir']:
                    subfiles = []
                    subitems = FileScanner.get_items(data['path'])
                    
                    for subitem in subitems:
                        if subitem['name'].lower().endswith(SUB_EXTS):
                            subfiles.append(subitem)
                        
                        elif subitem['is_dir']:
                            nested_items = FileScanner.get_items(subitem['path'])
                            for nested_item in nested_items:
                                if nested_item['name'].lower().endswith(SUB_EXTS):
                                    subfiles.append(nested_item)
                    
                    allitems.extend(subfiles)
        if self.ui.rename_dubs_checkBox.isChecked():
            for data in items:
                if any(word in data['name'].lower() for word in ('dub', 'sound')) and data['is_dir']:
                    dubfiles = []
                    dubitems = FileScanner.get_items(data['path'])
                    
                    for dubitem in dubitems:
                        if dubitem['name'].lower().endswith(DUB_EXTS):
                            dubfiles.append(dubitem)
                        
                        elif dubitem['is_dir']:
                            nested_items = FileScanner.get_items(dubitem['path'])
                            for nested_item in nested_items:
                                if nested_item['name'].lower().endswith(DUB_EXTS):
                                    dubfiles.append(nested_item)
                    
                    allitems.extend(dubfiles)
        
        items = allitems

        eps_num = int(self.ui.episodes_lineEdit.text())
        start_from_ep = int(self.ui.start_from_lineEdit.text())
        eps_tuple = tuple(range(start_from_ep, eps_num + 1))
        rename_queue = []

        for data in items:
            file_name = data['name']
            file_path = data['path']
            
            if file_name.lower().endswith(exts):
                parsed_data = anitopy.parse(file_name)
                
                if parsed_data and parsed_data.get('episode_number'):
                    try:
                        parsed_ep = int(parsed_data.get('episode_number'))
                    except ValueError:
                        continue
                    if parsed_ep in eps_tuple:
                        ext = os.path.splitext(file_name)[1]
                        
                        base_new_name = self.generate_name(self.ui.template_lineEdit.text(), parsed_ep)
                        new_name = base_new_name + ext

                        file_dir = os.path.dirname(file_path)
                        new_file_path = os.path.join(file_dir, new_name).replace('\\', '/')
                        
                        rename_queue.append((file_path, new_file_path))

        # Rename
        for old_path, new_path in rename_queue:
                self.filemClient.rename_file(old_path, new_path)

        # Folder
        if self.ui.rename_folder_checkBox.isChecked():
            new_folder_name = self.generate_name(self.ui.folder_name_lineEdit.text())
            new_folder_path = self.filemClient.rename_folder(self.folder_path, new_folder_name)

            if new_folder_path:
                self.folder_path = new_folder_path

        self.save_pictures()


    def generate_name(self, template: str = '', episode: int = 0) -> str:
        ui = self.ui
        episodes = ui.episodes_lineEdit.text()
        # Title
        template = template.replace('{title}', ui.title_lineEdit.text())
        # Season
        template = template.replace('{season_num}', ui.season_num_lineEdit.text().zfill(2))
        template = template.replace('{season}', ui.season_lineEdit.text())
        template = template.replace('{year}', ui.season_year_lineEdit.text())
        # Type
        template = template.replace('{type}', ui.type_lineEdit.text())
        # Studio
        template = template.replace('{studio}', ui.studio_lineEdit.text())
        # Duration
        template = template.replace('{duration}', ui.duration_lineEdit.text())
        # Source
        template = template.replace('{source}', ui.source_lineEdit.text())
        # Resolution
        template = template.replace('{resolution}', ui.resolution_lineEdit.text())
        # Height
        template = template.replace('{height}', ui.resolution_lineEdit.text().split('x')[-1])
        # Width
        template = template.replace('{height}', ui.resolution_lineEdit.text().split('x')[0])
        # Quality
        if 'p' not in ui.resolution_lineEdit.text():
            template = template.replace('{quality}', ui.resolution_lineEdit.text().split('x')[-1]+'p')
        else:
            template = template.replace('{quality}', ui.resolution_lineEdit.text().split('x')[-1])
        # Fansub group
        template = template.replace('{fansub}', ui.fansub_lineEdit.text())
        # Score
        template = template.replace('{score}', ui.score_lineEdit.text())
        # Status
        template = template.replace('{status}', ui.status_lineEdit.text())
        # Episodes
        template = template.replace('{episodes}', episodes)
        # Country
        template = template.replace('{country}', ui.country_lineEdit.text())
        template = template.replace('{country_full}', ui.country_lineEdit.text())

        # Episode
        padding = max(2, len(episodes))
        formatted_ep = str(episode).zfill(padding)
        template = template.replace('{episode}', formatted_ep)

        return template

