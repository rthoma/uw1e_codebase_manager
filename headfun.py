# Header for congestion relief problem

import headdef

###############################################################################
# Header                                                                      #
###############################################################################

def head_options(file_list, hour_ahead):

    base_options = '$onempty\n'
    base_options += '$offlisting\n'
    base_options += '$offupper\n'
    base_options += '$offsymlist\n'
    base_options += '$offsymxref\n'
    base_options += '$offuellist\n'
    base_options += '$offuelxref\n\n'

    for handle in file_list:
        handle.write(79*'*' + '\n')
        handle.write('*** OPTIONS' + 67*' ' + '*\n')
        handle.write(79*'*' + '\n\n')
        handle.write(base_options)

    list_container = [('limrow = 0,', ''),
                      ('limcol = 0,', ''),
                      ('solprint = off,', ''),
                      ('sysout = off', '')]

    options = headdef.Parlist(list_container)
    options.name = 'options\n'

    for handle in file_list:
        options.write_parlist(handle)


def head_inputs(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    base_input = '$include ' + path_dict['base_path']

    if hour_ahead:
        base_input += 'input_data_4hour_TH.gms\n\n'
    else:
        base_input += 'input_data.gms\n\n'

    for handle in file_list:
        handle.write(79*'*' + '\n')
        handle.write('*** INPUT DATA' + 64*' ' + '*\n')
        handle.write(79*'*' + '\n\n')
        handle.write(base_input)

    uc1_table = headdef.Table()
    uc1_table.name = 'p_ext2'
    uc1_table.domain = '(d, t)'
    uc1_table.path = path_dict['data_path'] + 'pext_2round.csv'

    uc1_table.write_table(uc_list[1])

    cf_table_list = [
        ('g_bis2', '(i, t)', 'gbis.csv'),
        ('glin_bis2A', '(i, t)', 'glin_bisA.csv'),
        ('glin_bis2B', '(i, t)', 'glin_bisB.csv'),
        ('glin_bis2C', '(i, t)', 'glin_bisC.csv'),
        ('slack_wind_bis2', '(w, t)', 'slackwindbis.csv'),
        ('slack_solar_bis2', '(r, t)', 'slacksolarbis.csv'),
        ('slack_fixed_bis2', '(f, t)', 'slackfixedbis.csv'),
        ('powerflowUC2', '(l, t)', 'powerflow.csv')
    ]

    cf_table = headdef.Table()

    for item in cf_table_list:
        cf_table.name = item[0]
        cf_table.domain = item[1]
        cf_table.path = path_dict['data_path'] + item[2]

        cf_table.write_table(cf_list[0])
        cf_table.write_table(cf_list[1])

    cf_parameter_list = \
        [('glin_bis(t, i, b)', 'gen block outputs from previous stage'),
         ('slack_solar_bis(r, t)', 'solar spillage in the previous stage'),
         ('slack_wind_bis(w, t)', 'wind spillage in the previous stage'),
         ('slack_fixed_bis(f, t)', 'fixed spillage in the previous stage'),
         ('gbis(t, i)', 'gen power output in previous stage'),
         ('M_cong_aux(t, l)', 'congestion indicator by line'),
         ('M_cong(t)', 'system wide congestion indicator')]

    cf_parameters = headdef.Parlist(cf_parameter_list)
    cf_parameters.name = 'parameters\n'

    cf_parameter_string = \
        ("gbis(t, i) = g_bis2(i, t);\n"
         "glin_bis(t, i, 'b1') = glin_bis2A(i, t);\n"
         "glin_bis(t, i, 'b2') = glin_bis2B(i, t);\n"
         "glin_bis(t, i, 'b3') = glin_bis2C(i, t);\n"
         "slack_wind_bis(w, t) = slack_wind_bis2(w, t);\n"
         "slack_solar_bis(r, t) = slack_solar_bis2(r, t);\n"
         "slack_fixed_bis(f, t) = slack_fixed_bis2(f, t);\n"
         "M_cong_aux(t, l)$(abs(powerflowUC2(l, t)) - l_max(l) ge 0) = 1;\n"
         "M_cong(t)$(sum(l, M_cong_aux(t, l)) gt 0) = 1;\n\n")

    for cf_handle in cf_list:
        cf_parameters.write_parlist(cf_handle)
        cf_handle.write(cf_parameter_string)


def head_bounds(file_list, hour_ahead, path_dict):

    cf_list = file_list[1:3]

    cf_list[1].write(79*'*' + '\n')
    cf_list[1].write('*** AVAILABILITY BOUNDS' + 55*' ' + '*\n')
    cf_list[1].write(79*'*' + '\n\n')

    cf_bound_list = \
        [('ch_DEPO', '(d, t)', 'ch_DEPO.csv'),
         ('dis_DEPO', '(d, t)', 'dis_DEPO.csv'),
         ('C_ch', '(d, t)', 'C_ch.csv'),
         ('C_dis', '(d, t)', 'C_dis.csv'),
         ('C_SC', '(d, t)', 'C_SC.csv'),
         ('C_SD', '(d, t)', 'C_SD.csv'),
         ('P_ch', '(d, t)', 'P_ch.csv'),
         ('P_dis', '(d, t)', 'P_dis.csv')]

    cf_bounds = headdef.Table()

    for item in cf_bound_list:
        cf_bounds.name = item[0]
        cf_bounds.domain = item[1]
        cf_bounds.path = path_dict['depo_path'] + item[2]

        cf_bounds.write_table(cf_list[1])

    cf_bound_parameters_list = \
        [('Bound_ch(t, d),', ''),
         ('Bound_dis(t, d),', ''),
         ('Bound_SD(t, d),', ''),
         ('Bound_SC(t, d)', '')]

    cf_bound_parameters = headdef.Parlist(cf_bound_parameters_list)
    cf_bound_parameters.name = 'parameters\n'

    cf_bound_parameter_string = \
        ("** ESS bounds imposed by DEPO\n\n"
         "Bound_ch(t, d) = (ES_power_max(d)*s_base - ch_DEPO(d, t))$(ch_DEPO(d, t) gt 0)\n"
         "               + (ES_power_max(d)*s_base)$(dis_DEPO(d, t) gt 0)\n"
         "               + (ES_power_max(d)*s_base)$((dis_DEPO(d, t) eq 0)\n"
         "                                           and (ch_DEPO(d, t) eq 0));\n\n"
         "Bound_dis(t, d) = (ES_power_max(d)*s_base)$(ch_DEPO(d, t) gt 0)\n"
         "                + (ES_power_max(d)*s_base - dis_DEPO(d, t))$(dis_DEPO(d, t) gt 0)\n"
         "                + (ES_power_max(d)*s_base)$((dis_DEPO(d, t) eq 0)\n"
         "                                            and (ch_DEPO(d, t) eq 0));\n\n"
         "Bound_SD(t, d) = (0)$(ch_DEPO(d, t) gt 0)\n"
         "               + (dis_DEPO(d, t))$(dis_DEPO(d, t) gt 0)\n"
         "               + (0)$((dis_DEPO(d, t) eq 0) and (ch_DEPO(d, t) eq 0));\n\n"
         "Bound_SC(t, d) = (ch_DEPO(d, t))$(ch_DEPO(d, t) gt 0)\n"
         "               + (0)$(dis_DEPO(d, t) gt 0)\n"
         "               + (0)$((dis_DEPO(d, t) eq 0) and (ch_DEPO(d, t) eq 0));\n\n"
         "** Normalizing quantities by the system base\n\n"
         "Bound_ch(t, d) = Bound_ch(t, d)/s_base;\n"
         "Bound_dis(t, d) = Bound_dis(t, d)/s_base;\n"
         "Bound_SD(t, d) = Bound_SD(t, d)/s_base;\n"
         "Bound_SC(t, d) = Bound_SC(t, d)/s_base;\n"
         "ch_DEPO(d, t) = ch_DEPO(d, t)/s_base;\n"
         "dis_DEPO(d, t) = dis_DEPO(d, t)/s_base;\n"
         "C_ch(d, t) = C_ch(d, t)*s_base;\n"
         "C_dis(d, t) = C_dis(d, t)*s_base;\n"
         "C_SC(d, t) = C_SC(d, t)*s_base;\n"
         "C_SD(d, t) = C_SD(d, t)*s_base;\n"
         "P_ch(d, t) = P_ch(d, t)*s_base;\n"
         "P_dis(d, t) = P_dis(d, t)*s_base;\n\n")

    cf_bound_parameters.write_parlist(cf_list[1])
    cf_list[1].write(cf_bound_parameter_string)


def head_variables(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    for handle in file_list:
        handle.write(79*'*' + '\n')
        handle.write('*** VARIABLES' + 65*' ' + '*\n')
        handle.write(79*'*' + '\n\n')

    variables_list = [('obj', 'objective function'),
                      ('pf(t, l)', 'line flows'),
                      ('theta(t, s)', 'voltage angles')]

    variables = headdef.Parlist(variables_list)
    variables.name = 'variables\n'

    for cf_handle in cf_list:
        variables.write_parlist(cf_handle)

    variables_list += [('g(t, i)', 'generator power output')]

    for uc_handle in uc_list:
        variables.write_parlist(uc_handle)


def head_positive_variables(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    uc_positive_variables_list = [
        ('g_lin(t, i, b)', 'generator block outputs'),
        ('slack_solar(r, t)', 'solar spillage'),
        ('slack_wind(w, t)', 'wind spillage'),
        ('slack_fixed(f, t)', 'fixed spillage')
    ]

    uc_positive_variables = headdef.Parlist(uc_positive_variables_list)
    uc_positive_variables.name = 'positive variables\n'

    uc_positive_variables.write_parlist(uc_list[0])

    uc_positive_variables_list += [
        ('slack_flow(l, t) ', 'line limit slack variables'),
        ('slack_pbal(s, t)', 'nodal power balance slack variables')
    ]

    uc_positive_variables.write_parlist(uc_list[1])

    cf_positive_variables_list = \
        [('ch_total(t, d)', 'total ESS charging amount'),
         ('dis_total(t, d)', 'total ESS discharging amount'),
         ('deltag_plus(t, i)', 'positive dev. for g'),
         ('deltag_minus(t, i)', 'negative dev. for g'),
         ('deltag_lin_plus(t, i, b)', 'positive dev. for g_lin'),
         ('deltag_lin_minus(t, i, b)', 'negative dev. for g_lin'),
         ('slack_wind_plus(t, w)', 'positive dev. for wind power spillage'),
         ('slack_wind_minus(t, w)', 'negative dev. for wind power spillage'),
         ('slack_solar_plus(t, r)', 'positive dev. for solar power spillage'),
         ('slack_solar_minus(t, r)', 'negative dev. for solar power spillage'),
         ('slack_fixed_plus(t, f)', 'positive dev. for fixed power spillage'),
         ('slack_fixed_minus(t, f)', 'negative dev. for fixed power spillage'),
         ('soc(t, d)', 'energy state of charge')]

    cf_positive_variables = headdef.Parlist(cf_positive_variables_list)
    cf_positive_variables.name = 'positive variables\n'

    cf_positive_variables.write_parlist(cf_list[0])

    cf_positive_variables_list += \
        [('slack_pbal(s, t)', 'nodal power balance slack variables'),
         ('ch_TEPO_SD(t, d)', 'stop discharging'),
         ('dis_TEPO_SC(t, d)', 'stop charging'),
         ('ch_TEPO(t, d)', 'charging from TEPO'),
         ('dis_TEPO(t, d)', 'discharging from TEPO')]

    cf_positive_variables.write_parlist(cf_list[1])


def head_binary_variables(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    binary_variables_list = [('v(t, i)', 'commitment variables'),
                             ('y(t, i)', 'start up variables'),
                             ('z(t, i)', 'shut down variables')]

    binary_variables = headdef.Parlist(binary_variables_list)
    binary_variables.name = 'binary variables\n'

    for uc_handle in uc_list:
        binary_variables.write_parlist(uc_handle)

    binary_variables_list += \
        [('v_ch(t, d)', 'binary variable preventing simultaneous ESS action')]

    for cf_handle in cf_list:
        binary_variables.write_parlist(cf_handle)


def head_equations(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    equations_list = \
        [('cost', 'objective function'),
         ('bin_set1(t, i)', 'binary logic constraint 1'),
         ('bin_set10(t, i)', 'binary logic constraint 1_2'),
         ('bin_set2(t, i)', 'binary logic constraint 2'),
         ('min_updown_1(t, i)', 'initial statuses'),
         ('min_updown_2(t, i)', 'minimum up time constraint'),
         ('min_updown_3(t, i)', 'minimum down time constraint'),
         ('slack_wind_constr(t, w)', 'maximum wind spillage constraint'),
         ('slack_solar_constr(t, r)', 'maximum solar spillage constraint'),
         ('slack_fixed_constr(t, f)', 'maximum fixed spillage constraint'),
         ('gen_sum(t, i)', 'summation over all blocks'),
         ('gen_min(t, i)', 'minimum power output of generators'),
         ('block_output(t, i, b)', 'maximum power output of each block'),
         ('ramp_limit_min(t, i)', 'ramp dn constraint'),
         ('ramp_limit_max(t, i)', 'ramp up constraint'),
         ('ramp_limit_min_1(t, i)', 'ramp dn constraint for initial period'),
         ('ramp_limit_max_1(t, i)', 'ramp up constraint for initial period'),
         ('line_flow(t, l)', 'power flow'),
         ('power_balance(t, s)', 'power balance equation'),
         ('voltage_angles_min(t, s)', 'minimum voltage phase angle limits'),
         ('voltage_angles_max(t, s)', 'maximum voltage phase angle limits')]

    equations = headdef.Parlist(equations_list)
    equations.name = 'equations\n'

    equations.write_parlist(uc_list[0])

    equations_list += [('line_capacity_min(t, l)', 'maximum line flow limits'),
                       ('line_capacity_max(t, l)', 'minimum line flow limits')]

    equations.write_parlist(uc_list[1])

    equations_list += \
        [('slack_wind_constr2(t, w)',  'minimum wind spillage constraint'),
         ('slack_solar_constr2(t, r)', 'minimum solar spillage constraint'),
         ('slack_fixed_constr2(t, f)', 'minimum fixed spillage constraint'),
         ('eq_storage_init(t, d)', 'initial ESS stage of charge'),
         ('eq_storage(t, d)', 'ESS state of charge calculation'),
         ('soc_limit(t, d)', 'maximum ESS state of charge'),
         ('eq_soc_final(t, d)', 'final ESS state of charge'),
         ('ch_total_limit(t, d)', 'maximum ESS charging'),
         ('dis_total_limit(t, d)', 'maximum ESS discharging')]

    equations.write_parlist(cf_list[0])

    equations_list += \
        [('eq_ch_total(t, d)', 'total ESS charge amount'),
         ('eq_dis_total(t, d)', 'total ESS discharge amount'),
         ('ch_SD_limit(t, d)', 'stop discharging limit'),
         ('dis_SC_limit(t, d)', 'stop charging limit'),
         ('ch_TEPO_limit(t, d)', 'charging from TEPO limit'),
         ('dis_TEPO_limit(t, d)', 'discharging from TEPO limit')]

    equations.write_parlist(cf_list[1])


def head_aliases(file_list, hour_ahead):

    aliases_list = [('(t, tt)', '')]
    aliases = headdef.Parlist(aliases_list)
    aliases.name = 'alias'

    for handle in file_list:
        aliases.inline_parlist(handle)
