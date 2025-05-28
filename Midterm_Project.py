
class Folder:
    def __init__(self, name: str, back_folder = None):
        self.name = name
        self.zir_shakhe = []
        self.files_in_folder = []
        self.back_folder: Folder = back_folder


    def make_folder(self,name):
        new_folder = Folder(name)
        self.zir_shakhe.append(new_folder)
        new_folder.back_folder = self


    def get_zir_shakhe(self):
        return self.zir_shakhe

    def add_file(self,file):
        if isinstance(file,File):
            if file in self.files_in_folder:
                print("in file ghablan sakhte shode!")
            else:
                self.files_in_folder.append(file)
        else:
            print("chizi ke mikhay ezafe koni aslan file nist!")

    def delete_folder(self, folder_name):
        for folder in self.zir_shakhe:
            if folder.name == folder_name:
                self.zir_shakhe.remove(folder)
                return
        else:
            print("folder peyda nashod!")

    def delete_file(self, file_name):
        for files in self.files_in_folder:
            if files.name == file_name:
                self.files_in_folder.remove(files)
                return
        else:
            print('file peyda nashod!')

    def get_file_and_folder(self):
        return self.files_in_folder + self.zir_shakhe

    def get_file_by_name(self, name):
        for f in self.files_in_folder:
            if f.name == name:
                return f
        return None

    def get_folder_by_name(self, name):
        for f in self.zir_shakhe:
            if f.name == name:
                return f
        return None




class File:
    def __init__(self, name, parent):
        self.parent: Folder = parent
        self.name = name
        self.matn = []


    def write_matn(self,new_matn:list[str]):
        self.matn = new_matn


    def append_matn(self,new_matn:list[str]):
        self.matn.extend(new_matn)


    def read_matn(self):
        return "\n".join(self.matn)


    def delete_line(self,line:int):
        if len(self.matn) > line:
            self.matn.pop(line)
        else:
            print("in khat ro nadarim!")

    def edit_line(self,new_matn,line:int):
        if len(self.matn) > line:
            self.matn[line] = new_matn
        else:
            print("in khat ro nadarim!")


class Filesystem:
    def __init__(self):
        self.main_folder = Folder("/")
        self.current_folder = self.main_folder
        self.masir = [self.main_folder]

    def mkdir(self,new_folder):
        self.current_folder.make_folder(new_folder)
        
    def rm(self, name):
        if self.current_folder.get_folder_by_name(name):
            self.current_folder.delete_folder(name)
        elif self.current_folder.get_file_by_name(name):
            self.current_folder.delete_file(name)
        else:
            print("file ya folder ba in name vojood nadarad!")
            
    def ls(self):
        for item in self.current_folder.get_file_and_folder():
            print(item.name)

    def cd(self, folder_name):
        folder = self.current_folder.get_folder_by_name(folder_name)
        if folder:
            self.current_folder = folder
            self.masir.append(folder)
        else:
            print("in folder ro nadarim!")

    def cd_up(self):
        if self.current_folder.back_folder:
            self.current_folder = self.current_folder.back_folder
            if self.masir:
                self.masir.pop()
        else:
            print("dar root hastid!")

    def show_masir(self):
        return "/" + "/".join([folder.name for folder in self.masir if folder.name != "/"])
    # -----------------------------------------------------------------------------


    def touch(self,file_name):
        file = File(file_name, self.current_folder)
        if self.current_folder.get_file_by_name(file_name) is None:
            self.current_folder.add_file(file)
        else:
            print('esm file tekrarie!')


    def cat(self, file_name):
        file = self.current_folder.get_file_by_name(file_name)
        if file:
            print(file.read_matn())
        else:
            print('in file ro nadarim!')

    def nwfiletxt(self,file_name,lines: list[str]):
        if self.current_folder.get_file_by_name(file_name) is not None:
            print("File tekrari!!")
        else:
            file = File(file_name, self.current_folder)
            self.current_folder.add_file(file)
            file.write_matn(lines)
            self.cat(file_name)


    def appendtxt(self, file_name,lines:list[str]):
        file = self.current_folder.get_file_by_name(file_name)
        if file:
            file.append_matn(lines)
            self.cat(file_name)
        else:
            print('in file ro nadarim!')

    def editline(self, line:int,file_name):
        file = self.current_folder.get_file_by_name(file_name)
        if file:
            file.edit_line(input('new line:\n'),line)
            self.cat(file_name)
        else:
            print('in file ro nadarim!')

    def deline(self, file_name, line:int):
        file = self.current_folder.get_file_by_name(file_name)
        if file:
            file.delete_line(line)
            self.cat(file_name)
        else:
            print('in file ro nadarim!')
# ------------------------------------------------------------------------------

    def change_masir_by_new_masir(self, new_masir: str):
        parts = new_masir.strip("/").split("/")
        folder = self.main_folder if new_masir.startswith("/") else self.current_folder
        new_stack = [self.main_folder] if new_masir.startswith("/") else self.masir.copy()

        for part in parts:
            if part == "..":
                if folder.back_folder:
                    folder = folder.back_folder
                    if len(new_stack) > 1:
                        new_stack.pop()
                else:
                    print("dar root hastid!")
                    return
            elif part == "." or part == "":
                continue
            else:
                next_folder = folder.get_folder_by_name(part)
                if next_folder:
                    folder = next_folder
                    new_stack.append(folder)
                else:
                    print(f"'{part}' vojood nadarad!")
                    return

        self.current_folder = folder
        self.masir = new_stack

    def _resolve_masir(self, masir: str):
        parts = masir.strip("/").split("/")
        folder = self.main_folder if masir.startswith("/") else self.current_folder

        for part in parts:
            if part == "..":
                if folder.back_folder:
                    folder = folder.back_folder
            elif part == "." or part == "":
                continue
            else:
                next_folder = folder.get_folder_by_name(part)
                if next_folder:
                    folder = next_folder
                else:
                    return None
        return folder


    def mv(self, folder_name, masir):
        self.cp(folder_name, masir, True)

    def cp(self, folder_name, masir, delete = False):
        folder: Folder = self.current_folder.get_folder_by_name(folder_name)
        file: File = self.current_folder.get_file_by_name(folder_name)

        if not folder and not file:
            print("file ya folder vojood nadarad!")
            return

        dest_folder = self._resolve_masir(masir)
        if not dest_folder:
            print("masir ghalat ast!")
            return

        if folder:
            copy_folder = folder
            if delete is True:
               folder.back_folder.zir_shakhe.remove(folder)
            dest_folder.zir_shakhe.append(copy_folder)
            return copy_folder
        elif file:
            copy_file = file
            if delete is True:
                file.parent.files_in_folder.remove(file)
            copy_file.write_matn(file.matn.copy())
            dest_folder.add_file(copy_file)
            return copy_file



    def rename(self, old_name):
        folder = self.current_folder.get_folder_by_name(old_name)
        file = self.current_folder.get_file_by_name(old_name)

        if folder:
            folder.name = input('new name:\n')
        elif file:
            file.name = input('new name:\n')
        else:
            print("che folder che file ba in esm nadarim!")


# ----------------------------------------------------------------------------


class Command:
    def __init__(self, filesystem):
        self.filesystem = filesystem

    def run(self):
        print("\n شبیه‌ساز فایل‌سیستم، برای خروج 'exit' را وارد کنید")

        while True:
            masir = self.filesystem.show_masir()
            try:
                command_input = input(masir + " $ ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nخروج اضطراری")
                break

            if command_input.lower() == "exit":
                break

            if not command_input:
                continue

            parts = command_input.split()
            cmd = parts[0]
            args = parts[1:]

            try:
                if cmd == "mkdir" and len(args) == 1:
                    self.filesystem.mkdir(args[0])

                elif cmd == "rm" and len(args) == 1:
                    self.filesystem.rm(args[0])

                elif cmd == "ls":
                    self.filesystem.ls()

                elif cmd == "cd" and len(args) == 1:
                    if args[0] == "..":
                        self.filesystem.cd_up()
                    else:
                        self.filesystem.cd(args[0])

                elif cmd == "cdpath" and len(args) == 1:
                    self.filesystem.change_masir_by_new_masir(args[0])

                elif cmd == "touch" and len(args) == 1:
                    self.filesystem.touch(args[0])

                elif cmd == "cat" and len(args) == 1:
                    self.filesystem.cat(args[0])

                elif cmd == "nwfiletxt" and len(args) == 1:
                    lines = self._read_lines()
                    self.filesystem.nwfiletxt(args[0], lines)

                elif cmd == "appendtxt" and len(args) == 1:
                    lines = self._read_lines()
                    self.filesystem.appendtxt(args[0], lines)

                elif cmd == "editline" and len(args) >= 2:
                    line_num = int(args[0])
                    file_name = " ".join(args[1:])
                    self.filesystem.editline(line_num, file_name)

                elif cmd == "deline" and len(args) >= 2:
                    self.filesystem.deline(" ".join(args[1:]), int(args[0]))


                elif cmd == "rename" and len(args) == 1:
                    self.filesystem.rename(args[0])

                elif cmd == "mv" and len(args) == 2:
                    self.filesystem.mv(args[0], args[1])

                elif cmd == "cp" and len(args) == 2:
                    self.filesystem.cp(args[0], args[1])

                else:
                    print(" دستور نامعتبر یا تعداد آرگومان اشتباه بود")

            except Exception as e:
                print(" خطا:", e)

    def _read_lines(self):
        print(" خطوط مورد نظر را بنویسید، برای پایان /end/ را وارد کنید:")
        lines = []
        while True:
            line = input()
            if line.strip() == "/end/":
                break
            lines.append(line)
        return lines


# ---------------------------------------------------------
filesystem = Filesystem()
cmd = Command(filesystem)
cmd.run()














