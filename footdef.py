class Putfile:

    def __init__(self):
        self.hour_ahead = False
        self.comment = ''
        self.file_label = ''
        self.file_path = ''
        self.header_str = ''
        self.index_var = ''
        self.put_quantity = ''
        self.put_precision = 4
        self.day_domain = '(ord(t) lt card(t))'
        self.day_domain_end = '(ord(t) eq card(t))'
        self.hour_domain = '(ord(t) lt hour+horizon-1)'
        self.hour_domain_end = '(ord(t) eq hour+horizon-1)'
        self.rename_flag = False
        self.rename_str = ''

    def make_comment(self):

        tmp_comment = ''
        if self.comment:
            tmp_comment += '** ' + self.comment + '\n'

        return tmp_comment

    def make_body(self):

        tmp_body = ''
        tmp_body += 'file ' + self.file_label + ' '
        tmp_body += '/\'' + self.file_path + '\'/;\n'
        tmp_body += 'put ' + self.file_label + ';\n'
        tmp_body += 'put \"** ' + self.header_str + ' **\"/;\n'

        if self.rename_flag:
            tmp_body += "put_utility 'ren' / '" + self.rename_str + "':0;\n\n"
        else:
            tmp_body += '\n'

        tmp_body += 'loop(t,\n'
        tmp_body += 4*' ' + "put \",\", t.tl:0:0,\n" + ');\n\n'
        tmp_body += 'put /;\n'
        tmp_body += 'loop(' + self.index_var + ',\n'
        tmp_body += 4*' ' + "put " + self.index_var + ".tl:0:0, \",\"\n"

        domain_main = ''
        domain_end = ''
        if self.hour_ahead:
            domain_main += 't_ha(t) and (' + self.hour_domain
            domain_main += ' and ' + self.day_domain
            domain_end += 't_ha(t) and (' + self.hour_domain_end
            domain_end += ' and ' + self.day_domain_end
        else:
            domain_main = self.day_domain
            domain_end = self.day_domain_end

        domain_list = [(domain_main, ', \",\"\n'), (domain_end, ',\n')]

        for domain in domain_list:
            tmp_body += 4*' ' + 'loop(t$' + domain[0] + ',\n'
            tmp_body += 8*' ' + 'put (' + self.put_quantity + '):0:'
            tmp_body += str(int(self.put_precision)) + domain[1]
            tmp_body += 4*' ' + ');\n'

        tmp_body += 4*' ' + 'put /;\n'
        tmp_body += ');\n\n'

        return tmp_body

    def write_put_file(self, file_handle):
        file_handle.write(self.make_comment())
        file_handle.write(self.make_body())
