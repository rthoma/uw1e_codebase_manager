class Table:

    def __init__(self):
        self.name = ''
        self.comment = ''
        self.domain = ''
        self.path = ''

    def make_comment(self):

        tmp_comment = ''
        if self.comment:
            tmp_comment += '** ' + self.comment + '\n'

        return tmp_comment

    def make_name(self):

        tmp_name = 'table '
        tmp_name += self.name + self.domain + '\n'

        return tmp_name

    def make_body(self):

        tmp_body = '$ondelim\n'
        tmp_body += '$include ' + self.make_path() + '\n'
        tmp_body += '$offdelim\n' + ';\n\n'

        return tmp_body

    def make_path(self):

        tmp_path = ''
        tmp_path += self.path

        return tmp_path

    def write_table(self, file_handle):
        file_handle.write(self.make_comment())
        file_handle.write(self.make_name())
        file_handle.write(self.make_body())


class Parlist:

    def __init__(self, list_container):
        self.name = ''
        self.comment = ''
        self.list_container = list_container

    def make_comment(self):
        tmp_comment = ''
        if self.comment:
            tmp_comment += '** ' + self.comment + '\n'

        return tmp_comment

    def make_name(self):
        tmp_name = self.name

        return tmp_name

    def make_body(self, inline_flag):
        tmp_body = ''
        text_stop = max([len(item[0]) for item in self.list_container])

        for k in range(len(self.list_container)):

            item = self.list_container[k]
            tmp_body += 8*inline_flag*' ' + item[0]

            if item[1]:
                tmp_body += (text_stop - len(item[0]))*' ' + 8*' ' + item[1]

            if k < len(self.list_container) - 1:
                tmp_body += '\n'
            elif k == len(self.list_container) - 1:
                tmp_body += inline_flag*'\n'

        tmp_body += ';\n\n'

        return tmp_body

    def write_parlist(self, file_handle):
        file_handle.write(self.make_comment())
        file_handle.write(self.make_name())
        file_handle.write(self.make_body(True))

    def inline_parlist(self, file_handle):
        file_handle.write(self.make_name() + ' ' + self.make_body(False))
