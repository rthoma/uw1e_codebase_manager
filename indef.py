class Setlist:

    def __init__(self, list_container):
        self.list_container = list_container

    def make_body(self):

        tmp_body = ''
        text_stop = max([len(item[0]) for item in self.list_container])

        for item in self.list_container:
            tmp_body += 'set ' + item[0] + (text_stop - len(item[0]))*' '
            tmp_body += 8*' ' + item[1]

            if not item[2]:
                tmp_body += ';\n'
            elif item[2][-1] == '\n':
                tmp_body += ' ' + item[2][:-1] + ';\n\n'
            else:
                tmp_body += ' ' + item[2] + ';\n'

        tmp_body += '\n'

        return tmp_body

    def write_setlist(self, file_handle):
        file_handle.write(self.make_body())


class TableKernel:

    def __init__(self, list_container, input_spec):
        self.list_container = list_container
        self.read_flag = input_spec['read_flag']
        self.read_subdir = input_spec['read_subdir']
        self.data_path = input_spec['data_path']
        self.bpa_sys_file = input_spec['bpa_sys_file']
        self.fixed_data_file = input_spec['fixed_data_file']
        self.ess_data_file = input_spec['ess_data_file']
        self.comment = ''
        self.table_tag = ''
        self.vector_comment = \
            "** Transformation of the previous matrix into a vector\n"
        self.abs_option = False
        self.ess_option = False
        self.fix_option = False

    def make_comment(self):
        tmp_comment = ''
        if self.comment:
            tmp_comment += '** ' + self.comment + '\n'

        return tmp_comment

    def make_body(self):
        tmp_body = ''
        tmp_body += 'table ' + self.list_container[0][0]

        if not self.list_container[2]:
            tmp_body += ' ' + self.table_tag.lower()

        tmp_body += '\n'

        if self.read_flag and self.list_container[1][0]:
            tmp_body += '*$call =xls2gms '
            tmp_body += 'r=' + self.list_container[1][0] + ' '
            tmp_body += 'i=' + self.read_subdir

            if self.ess_option:
                tmp_body += self.ess_data_file
            elif self.fix_option:
                tmp_body += self.fixed_data_file
            else:
                tmp_body += self.bpa_sys_file

            tmp_body += ' o=' + self.read_subdir + self.list_container[1][1] + '\n'

        tmp_body += '$include ' + self.data_path
        tmp_body += self.list_container[1][1] + '\n;\n\n'

        if self.list_container[2]:
            sum_call = 'sum(' + self.list_container[2][1] + ', '
            sum_call += self.list_container[0][0]

            if self.abs_option:
                sum_call = 'abs(' + sum_call
                sum_call += ')'

            sum_call += ');\n\n'

            tmp_body += self.vector_comment
            tmp_body += 'parameter ' + self.list_container[2][0] + ' '
            tmp_body += self.table_tag.lower() + ';\n'
            tmp_body += self.list_container[2][0] + ' = '
            tmp_body += sum_call

        return tmp_body

    def write_table_kernel(self, file_handle):
        file_handle.write(self.make_comment())
        file_handle.write(self.make_body())


class SlashTable:

    def __init__(self, table_def_dict):
        self.comment = ''
        self.name = ''
        self.domain = ''
        self.table_type = ''
        self.delim_flag = False
        self.dir_path = table_def_dict['dir_path']
        self.file_name = table_def_dict['file_name']

    def make_comment(self):
        tmp_comment = ''

        if self.comment:
            tmp_comment += '** ' + self.comment + '\n'

        return tmp_comment

    def make_name(self):
        tmp_name = self.make_comment()
        tmp_name += self.table_type.lower() + ' '
        tmp_name += self.name

        if self.domain:
            tmp_name += self.domain

        tmp_name += ' '

        return tmp_name

    def make_body(self):
        tmp_body = ''
        tmp_body += '/\n'

        include_str = '$include ' + self.dir_path
        include_str += self.file_name + '\n'

        if self.delim_flag:
            include_str = '$ondelim\n' + include_str
            include_str += '$offdelim\n'

        tmp_body += include_str + '/;\n\n'

        return tmp_body

    def write_slash_table(self, file_handle):
        file_handle.write(self.make_name())
        file_handle.write(self.make_body())
