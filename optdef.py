class Constraint:

    def __init__(self):
        self.name = ''
        self.domain = ''
        self.domain_modifier = ''
        self.lhs = ''
        self.rhs = ''
        self.operator = 'NULL'
        self.comment = ''
        self.num_indent = 8
        self.hour_ahead = False

    def make_operator(self):
        return '=' + self.operator + '='

    def make_comment(self):

        tmp_comment = ''

        if self.comment:
            tmp_comment += '** ' + self.comment + '\n'

        return tmp_comment

        # def make_comment end

    def make_name(self):

        tmp_name = ''
        tmp_name += self.name

        if bool(self.domain):
            tmp_name += self.domain

        if bool(self.domain_modifier):
            if self.hour_ahead:
                tmp_name += '$' + "(t_ha(t) and " + self.domain_modifier + ')'
            else:
                tmp_name += '$' + self.domain_modifier
        elif 't' in self.domain:
            if self.hour_ahead:
                tmp_name += '$' + "(t_ha(t))"

        tmp_name += '..'
        tmp_name += '\n'

        return tmp_name

        # end make_name

    def make_body(self):

        tmp_body = ' '*self.num_indent
        tmp_body += self.lhs + ' ' + self.make_operator() + ' '
        tmp_body += self.rhs
        tmp_body += ';\n\n'

        return tmp_body

        # end make_body

    def write_constraint(self, file_handle):

        file_handle.write(self.make_comment())
        file_handle.write(self.make_name())
        file_handle.write(self.make_body())

    def write_comment(self, file_handle):

        file_handle.write(self.make_comment())

        # end write_constraint
