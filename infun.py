# Functions for input file specification

import optdef
import headdef
import indef


def input_sets(input_file, hour_ahead):

    input_file.write(79*'*' + '\n')
    input_file.write('*** SETS' + 70*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    set_list_short = [
        ('d', 'index of storage devices', '/d1/'),
        ('i', 'index of generators', '/i1*i38/'),
        ('b', 'index of generator blocks', '/b1*b3/'),
        ('s', 'index of buses', '/s1*s2764/'),
        ('l', 'index of transmission lines', '/l1*l3318/'),
        ('w', 'index of wind generators', '/w1*w73/'),
        ('r', 'index of solar generators', '/r1*r5/'),
        ('f', 'index of fixed generators', '/f1*f440/'),
        ('t', 'index of time periods', '/t1*t24/')
    ]

    if hour_ahead:
        set_list_short += \
        [('t_ha(t)', 'index of time periods in the hour ahead horizon', '')]

    set_short = indef.Setlist(set_list_short)
    set_short.write_setlist(input_file)

    set_list_long = [
        ('snopud(s)', 'buses that belong to the snopud area', '/s1831*s1958/'),
        ('from_to', 'lines from and to', '/from, to/'),
        ('column', 'generator connected to bus', '/col/'),
        ('wcolumn', 'wind connected to bus', '/wcol/'),
        ('rcolumn', 'solar connected to bus', '/rcol/'),
        ('fcolumn', 'fixed connected to bus', '/fcol/'),
        ('iter', 'number of iterations', '/iter1*iter40/'),
        ('day', 'day counter', '/day1*day5/')
    ]

    set_long = indef.Setlist(set_list_long)
    set_long.write_setlist(input_file)

    # end input_sets


def input_generator_data(input_file, hour_ahead, input_spec):

    def write_time_coupling_parameters(input_file, hour_ahead):

        time_coupling_string = \
        ("** Generator on-off status in initial period\n"
         "parameter onoff_t0_day(day, i) initial unit on-off status;\n"
         "onoff_t0_day(day, i)$(count_on_init_day(day, i) gt 0) = 1;\n\n"
         "** Parameter used for minimum up-time constraints\n"
         "parameter L_up_min_day(day, i) used for minimum up time constraints;\n"
         "L_up_min_day(day, i) = min(card(t), (g_up(i) - count_on_init_day(day, i))\n"
         "                                   * onoff_t0_day(day, i));\n\n"
         "** Parameter used for minimum down-time constraints\n"
         "parameter L_down_min_day(day, i) used for minimum down time constraints;\n"
         "L_down_min_day(day, i) = min(card(t), (g_down(i) - count_off_init_day(day, i))\n"
         "                                    * (1 - onoff_t0_day(day, i)));\n\n")

        input_file.write(time_coupling_string)

        # end write_time_coupling_parameters

    input_file.write(79*'*' + '\n')
    input_file.write('*** GENERATOR DATA' + 60*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # gen_map_aux
    gen_map_tuple = [
        ('gen_map_aux(i, column)',),
        ('Generator_Map!e2:f40', 'gmap2.inc'),
        ('gen_map(i)', 'column')
    ]

    gen_map_aux = indef.TableKernel(gen_map_tuple, input_spec)
    gen_map_aux.comment = \
        "Locations for generating units in the transmission network"
    gen_map_aux.table_tag = "generator map"

    gen_map_aux.write_table_kernel(input_file)

    # g_max_day
    g_max_tuple = [
        ('g_max_day(day, i, b)',),
        ('Generator_CostCurve!a2:f192', 'block_max.inc'),
        ()
    ]

    g_max_day = indef.TableKernel(g_max_tuple, input_spec)
    g_max_day.comment = \
        "Time varying generation cost curve MW block limit"
    g_max_day.table_tag = "generator block output limit"

    g_max_day.write_table_kernel(input_file)

    # g_cap_day
    g_cap_tuple = [
        ('g_cap_day(day, t, i)',),
        ('Generator_Pmax!a2:ao122', 'gcap.inc'),
        ()
    ]

    g_cap_day = indef.TableKernel(g_cap_tuple, input_spec)
    g_cap_day.comment = \
        "Time varying generation capacity"
    g_cap_day.table_tag = "generator capacity"

    g_cap_day.write_table_kernel(input_file)

    # k_day
    k_day_tuple = [
        ('k_day(day, i, b)',),
        ('Generator_CostCurve!i2:n192', 'k.inc'),
        ()
    ]

    k_day = indef.TableKernel(k_day_tuple, input_spec)
    k_day.comment = \
        "Time varying generation cost curve price block"
    k_day.table_tag = "slope of each generator cost curve block"

    k_day.write_table_kernel(input_file)

    # suc_sw
    suc_sw_tuple = [
        ('suc_sw_aux(i, column)',),
        ('Generator_Data!au2:av40', 'start_up_sw.inc'),
        ('suc_sw(i)', 'column')
    ]

    suc_sw = indef.TableKernel(suc_sw_tuple, input_spec)
    suc_sw.comment = "Start-up cost of generator i"
    suc_sw.table_tag = "generator stepwise start-up cost"

    suc_sw.write_table_kernel(input_file)

    # count_off_init_day
    count_off_init_tuple = [
        ('count_off_init_day(day, i)',),
        ('Generator_InitOff!a2:am7', 'aux2.inc'),
        ()
    ]

    count_off_init_day = indef.TableKernel(count_off_init_tuple, input_spec)
    count_off_init_day.comment = \
        "Time varying generation count off initial"
    count_off_init_day.table_tag = \
        "number of time periods each unit has been off"

    count_off_init_day.write_table_kernel(input_file)

    # count_on_init_day
    count_on_init_tuple = [
        ('count_on_init_day(day, i)',),
        ('Generator_InitOn!a2:am7', 'aux3.inc'),
        ()
    ]

    count_on_init_day = indef.TableKernel(count_on_init_tuple, input_spec)
    count_on_init_day.comment = \
        "Time varying generation count on initial"
    count_on_init_day.table_tag = \
        "number of time periods each unit has been on"

    count_on_init_day.write_table_kernel(input_file)

    # aux4 - fixed_op_cost
    fixed_op_cost_tuple = [
        ('aux4(i, column)',),
        ('Generator_Data!j2:k40', 'aux4.inc'),
        ('a(i)', 'column')
    ]

    fixed_op_cost = indef.TableKernel(fixed_op_cost_tuple, input_spec)
    fixed_op_cost.comment = \
        "Fixed operating cost of each generator"
    fixed_op_cost.table_tag = \
        "fixed operating cost of each generator"

    fixed_op_cost.write_table_kernel(input_file)

    # aux5 - gen_ramp_up
    gen_ramp_up_tuple = [
        ('aux5(i, column)',),
        ('Generator_Data!m2:n40', 'aux5.inc'),
        ('ramp_up(i)', 'column')
    ]

    gen_ramp_up = indef.TableKernel(gen_ramp_up_tuple, input_spec)
    gen_ramp_up.comment = "Generator ramp up limit"
    gen_ramp_up.table_tag = "generator ramp-up limit"

    gen_ramp_up.write_table_kernel(input_file)

    # aux6 - gen_ramp_dn
    gen_ramp_dn_tuple = [
        ('aux6(i, column)',),
        ('Generator_Data!p2:q40', 'aux6.inc'),
        ('ramp_down(i)', 'column')
    ]

    gen_ramp_dn = indef.TableKernel(gen_ramp_dn_tuple, input_spec)
    gen_ramp_dn.comment = "Generator ramp down limit"
    gen_ramp_dn.table_tag = "generator ramp down limit"

    gen_ramp_dn.write_table_kernel(input_file)

    # aux7 - min_dn_time
    min_dn_time_tuple = [
        ('aux7(i, column)',),
        ('Generator_Data!s2:t40', 'aux7.inc'),
        ('g_down(i)', 'column')
    ]

    min_dn_time = indef.TableKernel(min_dn_time_tuple, input_spec)
    min_dn_time.comment = "Generator minimum down time"
    min_dn_time.table_tag = "generator minimum down time"

    min_dn_time.write_table_kernel(input_file)

    # aux8 - min_up_time
    min_up_time_tuple = [
        ('aux8(i, column)',),
        ('Generator_Data!v2:w40', 'aux8.inc'),
        ('g_up(i)', 'column')
    ]

    min_up_time = indef.TableKernel(min_up_time_tuple, input_spec)
    min_up_time.comment = "Generator minimum up time"
    min_up_time.table_tag = "generator minimum up time"

    min_up_time.write_table_kernel(input_file)

    # aux9 - min_gen_power
    min_gen_power_tuple = [
        ('aux9(i, column)',),
        ('Generator_Data!y2:z40', 'aux9.inc'),
        ('g_min(i)', 'column')
    ]

    min_gen_power = indef.TableKernel(min_gen_power_tuple, input_spec)
    min_gen_power.comment = "Generator minimum power output"
    min_gen_power.table_tag = "generator minimum power output"

    min_gen_power.write_table_kernel(input_file)

    # g_0_day
    g_0_day_tuple = [
        ('g_0_day(day, i)',),
        ('Generator_PInit!a2:am7', 'aux10.inc'),
        ()
    ]

    g_0_day = indef.TableKernel(g_0_day_tuple, input_spec)
    g_0_day.comment = "Generator initial power output"
    g_0_day.table_tag = "generator initial power output"

    g_0_day.write_table_kernel(input_file)

    write_time_coupling_parameters(input_file, hour_ahead)

    # end input_generator_data


def input_line_data(input_file, hour_ahead, input_spec):

    input_file.write(79*'*' + '\n')
    input_file.write('*** LINE DATA' + 65*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # line_map
    line_map_tuple = [
        ('line_map(l, from_to)',),
        ('Line_Map!e1:g3319', 'line_map.inc'),
        ()
    ]

    line_map = indef.TableKernel(line_map_tuple, input_spec)
    line_map.comment = \
        "Origin and destination buses for each transmission line"
    line_map.table_tag = "To and from buses for each line"

    line_map.write_table_kernel(input_file)

    # line_admittance
    line_admittance_tuple = [
        ('aux11(l, column)',),
        ('Line_Data!a1:b3319', 'aux11.inc'),
        ('admittance(l)', 'column')
    ]

    line_admittance = indef.TableKernel(line_admittance_tuple, input_spec)
    line_admittance.comment = \
        "Admittance of each transmission line"
    line_admittance.table_tag = "line admittance"
    line_admittance.abs_option = True

    line_admittance.write_table_kernel(input_file)

    # line_capacities
    line_capacities_tuple = [
        ('aux12(l, column)',),
        ('Line_Data!j1:k3319', 'aux12.inc'),
        ('l_max(l)', 'column')
    ]

    line_capacities = indef.TableKernel(line_capacities_tuple, input_spec)
    line_capacities.comment = "Line capacity (long-term ratings)"
    line_capacities.table_tag = "line capacity"

    line_capacities.write_table_kernel(input_file)

    # snopud_lines
    snopud_lines_tuple = [
        ('snpd_lines_aux(l, column)',),
        ('', 'snpd_lines.inc'),
        ('snpd_lines_map(l)', 'column')
    ]

    snopud_lines = indef.TableKernel(snopud_lines_tuple, input_spec)
    snopud_lines.comment = "Transmission lines connected to snopud buses"
    snopud_lines.table_tag = "snopud transmission line map"

    snopud_lines.write_table_kernel(input_file)

    # end input_line_data


def input_demand_data(input_file, hour_ahead, input_spec, num_groups):

    input_file.write(79*'*' + '\n')
    input_file.write('*** DEMAND' + 68*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # demand_data
    demand_data_tuple = [
        ('d_day(day, s, t)',),
        ('Load1!a1:aa13821', 'load1.inc'),
        ()
    ]

    demand_data = indef.TableKernel(demand_data_tuple, input_spec)
    demand_data.fix_option = True
    demand_data.comment = "Time varying demand data"
    demand_data.table_tag = "time varying demand data"

    demand_data.write_table_kernel(input_file)

    # more_demand_data

    for k in range(2, num_groups+1):
        more_demand_data_tuple = [
            ('d_day' + str(k) + '(day, s, t)',),
            ('Load1!a1:aa13821', 'load' + str(k) + '.inc'),
            ()
        ]

        more_demand_data = indef.TableKernel(
            more_demand_data_tuple,
            input_spec
        )
        more_demand_data.fix_option = True
        more_demand_data.comment = \
            "Time varying demand for day group " + str(k)
        more_demand_data.table_tag = "demand at bus s"

        more_demand_data.write_table_kernel(input_file)

        more_demand_str = (
            "** Populating the demand parameter with the correct data group\n"
            "d_day(day, s, t)$(d_day2(day, s, t) > 0) = d_day2(day, s, t);\n\n"
        )

        input_file.write(more_demand_str)

        # end for loop

    # map_islands
    map_islands_tuple = [
        ('map_islands_aux(s, column)',),
        ('', 'map_islands.inc'),
        ('map_islands(s)', 'column')
    ]

    map_islands = indef.TableKernel(map_islands_tuple, input_spec)
    map_islands.comment = "Auxiliary parameter to remove islanded buses"
    map_islands.table_tag = "map of islanded buses"

    map_islands.write_table_kernel(input_file)

    island_removal_str = (
        "** Ignore the demand of the islanded areas\n"
        "d_day(day, s, t) = d_day(day, s, t)*map_islands(s);\n\n"
    )

    input_file.write(island_removal_str)

    # end input_demand_data


def input_wind_data(input_file, hour_ahead, input_spec):

    input_file.write(79*'*' + '\n')
    input_file.write('*** WIND DATA' + 65*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # wind_map_aux
    wind_map_aux_tuple = [
        ('win_map_aux(w, wcolumn)',),
        ('Wind!e1:f74', 'wmap2.inc'),
        ('win_map(w)', 'wcolumn')
    ]

    wind_map = indef.TableKernel(wind_map_aux_tuple, input_spec)
    wind_map.comment = "Locations of the wind power plants"
    wind_map.table_tag = "wind power plant locations"

    wind_map.write_table_kernel(input_file)

    # wind_data
    wind_data_tuple = [
        ('wind_deterministic_day(day, t, w)',),
        ('Wind!h1:ce121', 'wind_deterministic.inc'),
        ()
    ]

    wind_data = indef.TableKernel(wind_data_tuple, input_spec)
    wind_data.comment = "Time varying wind data"
    wind_data.table_tag = "time varying wind data"

    wind_data.write_table_kernel(input_file)

    # end input_wind_data


def input_solar_data(input_file, hour_ahead, input_spec):

    input_file.write(79*'*' + '\n')
    input_file.write('*** SOLAR DATA' + 64*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # sol_map_aux
    solar_map_aux_tuple = [
        ('sol_map_aux(r, rcolumn)',),
        ('Solar!e1:f6', 'rmap2.inc'),
        ('sol_map(r)', 'rcolumn')
    ]

    solar_map = indef.TableKernel(solar_map_aux_tuple, input_spec)
    solar_map.comment = "Locations of the solar plants"
    solar_map.table_tag = "solar power plant locations"

    solar_map.write_table_kernel(input_file)

    # solar_data
    solar_data_tuple = [
        ('sol_deterministic_day(day, t, r)',),
        ('Solar!h1:o121', 'solar_deterministic.inc'),
        (),
    ]

    solar_data = indef.TableKernel(solar_data_tuple, input_spec)
    solar_data.comment = "Time varying solar data"
    solar_data.table_tag = "time varying solar data"

    solar_data.write_table_kernel(input_file)

    # end input_solar_data


def input_fixed_data(input_file, hour_ahead, input_spec):

    input_file.write(79*'*' + '\n')
    input_file.write('*** FIXED DATA' + 64*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # fixed_map_aux
    fixed_map_aux_tuple = [
        ('fix_map_aux(f, fcolumn)',),
        ('Fixed!e1:f441', 'fmap2.inc'),
        ('fix_map(f)', 'fcolumn')
    ]

    fixed_map = indef.TableKernel(fixed_map_aux_tuple, input_spec)
    fixed_map.comment = "Locations of the fixed generators"
    fixed_map.table_tag = "fixed generation unit locations"

    fixed_map.write_table_kernel(input_file)

    # fixed_data
    fixed_data_tuple = [
        ('fix_deterministic_day(day, f, t)',),
        ('Fixed!a1:aa2201', 'fixed_deterministic.inc'),
        ()
    ]

    fixed_data = indef.TableKernel(fixed_data_tuple, input_spec)
    fixed_data.fix_option = True
    fixed_data.comment = "Time varying fixed generation data"
    fixed_data.table_tag = "time varying fixed generation data"

    fixed_data.write_table_kernel(input_file)

    # end input_fixed_data


def input_scalars(input_file, hour_ahead, input_spec, path_dict):

    input_file.write(79*'*' + '\n')
    input_file.write('*** SCALARS' + 67*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    scalars_list = []
    if hour_ahead:
        scalars_list += [('horizon', 'optimization horizon /4/')]

    scalars_list += [
        ('penalty_pf', 'penalty factor /2000/'),
        ('VoRS', 'value of wind spillage /20/'),
        ('VoFS', 'value of fixed spillage /1000000/'),
        ('s_base', 'base power /100/'),
        ('counter', 'counter /2/'),
        ('M', 'no. of hours a unit can be on or off /2600/'),
        ('N_iter', 'number of iterations /2/'),
        ('INFEASIBLE_PENALTY', 'infeasibility penalty /100000000/'),
        ('ESS_ADJUST_PENALTY', 'ESS charge adjustment penalty /100/')
    ]

    input_scalars = headdef.Parlist(scalars_list)
    input_scalars.name = 'scalars\n'

    input_scalars.write_parlist(input_file)

    day_number_dict = {
        'dir_path': path_dict['depo_path'],
        'file_name': 'Day_number.csv'
    }

    day_number = indef.SlashTable(day_number_dict)
    day_number.name = 'N'
    day_number.comment = "Index corresponding to the desired day"
    day_number.table_type = 'scalar'

    day_number.write_slash_table(input_file)

    if hour_ahead:
        hour_number_dict = {
            'dir_path': path_dict['depo_path'],
            'file_name': 'Hour_number.csv'
        }

        hour_number = indef.SlashTable(hour_number_dict)
        hour_number.name = 'hour'
        hour_number.comment = "Index corresponding to the desired hour"
        hour_number.table_type = 'scalar'

        hour_number.write_slash_table(input_file)

    # end input_scalars


def input_parameters(input_file, hour_ahead):

    input_file.write(79*'*' + '\n')
    input_file.write('*** PARAMETERS' + 64*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    action_parlist = [
        ('action_aux(t, s),', ''),
        ('action(t, d),', ''),
        ('minimum_load_aux(t, s),', ''),
        ('maximum_load_aux(t, s),', ''),
        ('minimum_load(t, d),', ''),
        ('maximum_load(t, d)', '')
    ]

    action_obj = headdef.Parlist(action_parlist)
    action_obj.comment = "Auxiliary parameters for data output"
    action_obj.name = 'parameters\n'

    action_obj.write_parlist(input_file)

    optpar_parlist = [
        ('g_max(i, b),', ''),
        ('g_cap(t, i),', ''),
        ('k(i, b),', ''),
        ('g_0(i),', ''),
        ('onoff_t0(i),', ''),
        ('L_up_min(i),', ''),
        ('L_down_min(i),', ''),
        ('demand(s, t),', ''),
        ('wind_deterministic(t, w),', ''),
        ('sol_deterministic(t, r),', ''),
        ('fix_deterministic(f, t)', ''),
    ]

    optpar_obj = headdef.Parlist(optpar_parlist)
    optpar_obj.comment = \
        "Auxiliary parameters for the optimization formulation"
    optpar_obj.name = 'parameters\n'

    optpar_obj.write_parlist(input_file)

    parameter_normalization_str = (
        "** Normalization by the system base\n"
        "ramp_up(i) = ramp_up(i)/s_base;\n"
        "ramp_down(i) = ramp_down(i)/s_base;\n"
        "g_min(i) = g_min(i)/s_base;\n"
        "l_max(l) = l_max(l)/s_base;\n"
        "VoRS = VoRS*s_base;\n\n"
    )

    input_file.write(parameter_normalization_str)

    # end input_parameters


def input_storage_data(input_file, hour_ahead, input_spec, path_dict):

    input_file.write(79*'*' + '\n')
    input_file.write('*** STORAGE DATA' + 62*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    # storage_map_aux
    storage_map_aux_tuple = [
        ('storage_map_aux(d, column)',),
        ('map_storage!a2:b3', 'storage_map.inc'),
        ('storage_map(d)', 'column')
    ]

    storage_map_aux = indef.TableKernel(storage_map_aux_tuple, input_spec)
    storage_map_aux.comment = \
        "Locations of the energy storage systems (ESS)"
    storage_map_aux.table_tag = "energy storage system locations"
    storage_map_aux.ess_option = True

    storage_map_aux.write_table_kernel(input_file)

    # area_labels
    area_labels_tuple = [
        ('area_name_storage(d, column)',),
        ('map_storage!d2:e3', 'area_map.inc'),
        ('storage_area(d)', 'column')
    ]

    area_labels = indef.TableKernel(area_labels_tuple, input_spec)
    area_labels.comment = "Area labels for energy storage systems"
    area_labels.table_tag = "energy storage system area labels"
    area_labels.ess_option = True

    area_labels.write_table_kernel(input_file)

    # zone_labels
    zone_labels_tuple = [
        ('zone_name_storage(d, column)',),
        ('map_storage!g2:h3', 'zone_map.inc'),
        ('storage_zone(d)', 'column')
    ]

    zone_labels = indef.TableKernel(zone_labels_tuple, input_spec)
    zone_labels.comment = "Zone labels for energy storage systems"
    zone_labels.table_tag = "energy storage system zone labels"
    zone_labels.ess_option = True

    zone_labels.write_table_kernel(input_file)

    # Energy storage system parameters
    slash_table_dict = {
        'dir_path': '',
        'file_name': ''
    }

    slash_table_list = [
        ('ES_power_max', '(d)', 'ES_power_max.csv', "ES maximum power rating"),
        ('Emax', '(d)', 'Emax.csv', "ES maximum energy rating"),
        ('E_initial', '(d)', 'E_initial.csv', "Initial state of charge"),
        ('E_final', '(d)', 'E_final.csv', "Final state of charge"),
        ('alef_ch', '(d)', 'Efficiency.csv', "ES charging efficiency")
    ]

    for item in slash_table_list:

        slash_table_dict['dir_path'] = path_dict['depo_path']
        slash_table_dict['file_name'] = item[2]

        slash_table_obj = indef.SlashTable(slash_table_dict)
        slash_table_obj.name = item[0]
        slash_table_obj.domain = item[1]
        slash_table_obj.comment = item[3]
        slash_table_obj.delim_flag = True
        slash_table_obj.table_type = 'parameter'

        slash_table_obj.write_slash_table(input_file)

    storage_normalize_str = (
        "** Assume charging and discharging efficiency is identical\n"
        "parameter alef_dis(d);\n"
        "alef_dis(d) = alef_ch(d);\n\n"
        "** Normalize quantites by the system base\n"
        "ES_power_max(d) = ES_power_max(d)/s_base;\n"
        "Emax(d) = Emax(d)/s_base;\n"
        "E_initial(d) = E_initial(d)/s_base;\n"
        "E_final(d) = E_final(d)/s_base;\n\n"
    )

    input_file.write(storage_normalize_str)

    # end input_storage_data


def input_initial_conditions(input_file, hour_ahead, input_spec, path_dict):

    if hour_ahead:

        input_file.write(79*'*' + '\n')
        input_file.write('*** INITIAL CONDITIONS' + 56*' ' + '*\n')
        input_file.write(79*'*' + '\n\n')

        # g_0_previous
        g_0_previous_tuple = [
            ('g_0_previous_aux(i, column)',),
            ('', 'g_0_previous_aux2.inc'),
            ('g_0_previous(i)', 'column')
        ]

        g_0_previous = indef.TableKernel(g_0_previous_tuple, input_spec)
        g_0_previous.comment = "Generation level in the previous period"
        g_0_previous.table_tag = "generation level in the previous period"

        g_0_previous.write_table_kernel(input_file)

        # on_off_status
        on_off_tuple = [
            ('onoff_t0_previous_aux(i, column)',),
            ('', 'onoff_t0_previous_aux2.inc'),
            ('onoff_t0_previous(i)', 'column')
        ]

        on_off_status = indef.TableKernel(on_off_tuple, input_spec)
        on_off_status.comment = "On-off status in the t0 previous period"
        on_off_status.table_tag = "on-off status in the t0 previous period"

        on_off_status.write_table_kernel(input_file)

        # on_off_t1_status
        on_off_t1_tuple = [
            ('onoff_t1_previous_aux(i, column)',),
            ('', 'onoff_t1_previous_aux2.inc'),
            ('onoff_t1_previous(i)', 'column')
        ]

        on_off_t1_status = indef.TableKernel(on_off_t1_tuple, input_spec)
        on_off_t1_status.comment = "On-off status in the t1 previous period"
        on_off_t1_status.table_tag = "on-off status in the t1 previous period"

        on_off_t1_status.write_table_kernel(input_file)

        # count_on_init
        count_on_init_tuple = [
            ('count_on_init_previous_aux(i, column)',),
            ('', 'count_on_init_previous_aux2.inc'),
            ('count_on_init_previous(i)', 'column')
        ]

        count_on_init = indef.TableKernel(count_on_init_tuple, input_spec)
        count_on_init.comment = "Up time in the previous period"
        count_on_init.table_tag = "up time in the previous period"

        count_on_init.write_table_kernel(input_file)

        # count_off_init
        count_off_init_tuple = [
            ('count_off_init_previous_aux(i, column)',),
            ('', 'count_off_init_previous_aux2.inc'),
            ('count_off_init_previous(i)', 'column')
        ]

        count_off_init = indef.TableKernel(count_off_init_tuple, input_spec)
        count_off_init.comment = "Down time in the previous period"
        count_off_init.table_tag = "down time in the previous period"

        count_off_init.write_table_kernel(input_file)

        count_on_init_aux_str = (
            "** Number of hours each unit has been on in the initial period\n"
            "parameter count_on_init_aux(i);\n"
            "count_on_init_aux(i)$((onoff_t1_previous(i) eq onoff_t0_previous(i))\n"
            "        and (onoff_t1_previous(i) eq 1)) = count_on_init_previous(i) + 1;\n\n"
            "count_on_init_aux(i)$((onoff_t1_previous(i) ne onoff_t0_previous(i))\n"
            "        and (onoff_t1_previous(i) eq 1)) = 1;\n\n"
            "count_on_init_aux(i)$(onoff_t1_previous(i) eq 0) = 1;\n\n"
        )

        input_file.write(count_on_init_aux_str)

        count_off_init_aux_str = (
            "** Number of hours each unit has been on in the initial period\n"
            "parameter count_off_init_aux(i);\n"
            "count_off_init_aux(i)$((onoff_t1_previous(i) eq onoff_t0_previous(i))\n"
            "        and (onoff_t1_previous(i) eq 0)) = count_off_init_previous(i) + 1;\n\n"
            "count_off_init_aux(i)$((onoff_t1_previous(i) ne onoff_t0_previous(i))\n"
            "        and (onoff_t1_previous(i) eq 0)) = 1;\n\n"
            "count_off_init_aux(i)$(onoff_t1_previous(i) eq 1) = 0;\n\n"
        )

        input_file.write(count_off_init_aux_str)

        input_file.write(79*'*' + '\n')
        input_file.write('*** DAY AHEAD POWER INJECTIONS' + 48*' ' + '*\n')
        input_file.write(79*'*' + '\n\n')

        da_injections = headdef.Table()
        da_injections.name = 'injection_DA'
        da_injections.domain = '(d, t)'
        da_injections.path = path_dict['day_data_path'] + 'pext_2round.csv'

        da_injections.write_table(input_file)

        da_charge_discharge_str = (
            "parameter ch_day(d, t);\n"
            "ch_day(d, t)$(injection_DA(d, t) gt 0) = injection_DA(d, t);\n"
            "ch_day(d, t)$(injection_DA(d, t) le 0) = 0;\n\n"
            "parameter dis_day(d, t);\n"
            "dis_day(d, t)$(injection_DA(d, t) lt 0) = -injection_DA(d, t);\n"
            "dis_day(d, t)$(injection_DA(d, t) ge 0) = 0;\n\n"
        )

        input_file.write(da_charge_discharge_str)

    # end input_initial_conditions


def input_time_horizon_logic(input_file, hour_ahead):

    input_file.write(79*'*' + '\n')
    input_file.write('*** TIME HORIZON LOGIC' + 56*' ' + '*\n')
    input_file.write(79*'*' + '\n\n')

    if hour_ahead:

# "    demand(s, t)$(t_ha(t) and (ord(t) le 24)) =\n"
# "        d_day(day, s, t)/s_base\n"
# "        + sum(d$(storage_map(d) eq ord(s)), injection_DA(d, t));\n\n"

        ha_horizon_logic_str = (
            "alias(t, tt);\n"
            "alias(day, dayd);\n\n"
            "t_ha(t)$((ord(t) ge hour) and (ord(t) lt hour+horizon)\n"
            "                          and (ord(t) le 24)) = yes;\n\n"
            "loop(day$(ord(day) eq N+counter),\n\n"
            "    g_max(i, b) = g_max_day(day, i, b)/s_base;\n"
            "    k(i, b) = k_day(day, i, b)*s_base;\n\n"
            "** Read the demand and generation data for the selected day\n\n"
            "    demand(s, t)$(t_ha(t) and (ord(t) le 24)) =\n"
            "        d_day(day, s, t)/s_base;\n\n"
            "    sol_deterministic(t, r)$(t_ha(t) and (ord(t) le 24)) =\n"
            "        sol_deterministic_day(day, t, r)/s_base;\n\n"
            "    fix_deterministic(f, t)$(t_ha(t) and (ord(t) le 24)) =\n"
            "        abs(fix_deterministic_day(day, f, t))/s_base;\n\n"
            "    wind_deterministic(t, w)$(t_ha(t) and (ord(t) le 24)) =\n"
            "        wind_deterministic_day(day, t, w)/s_base;\n\n"
            "** Read the initial conditions from the day-ahead stage in the first period\n\n"
            "    if((hour eq 1) and (N+counter eq 2),\n"
            "        g_0(i) = g_0_day(day, i)/s_base;\n"
            "        onoff_t0(i) = onoff_t0_day(day, i);\n"
            "        L_up_min(i) = L_up_min_day(day, i);\n"
            "        L_down_min(i) = L_down_min_day(day, i);\n"
            "        count_on_init_aux(i) = count_on_init_day(day, i);\n"
            "        count_off_init_aux(i) = count_off_init_day(day, i);\n\n"
            "** Read the initial conditions from the previous hour-ahead run otherwise\n\n"
            "    elseif hour gt 1,\n"
            "        g_0(i) = g_0_previous(i);\n"
            "        onoff_t0(i) = onoff_t1_previous(i);\n"
            "        L_up_min(i) = min(card(t), (g_up(i) - count_on_init_aux(i))\n"
            "                                  * onoff_t1_previous(i));\n"
            "        L_down_min(i) = min(card(t), (g_down(i) - count_off_init_aux(i))\n"
            "                                   * (1 - onoff_t1_previous(i)));\n"
            "    );\n"
            ");\n\n"
            "display t_ha, demand;\n\n"
        )

        input_file.write(ha_horizon_logic_str)

    else:

        da_horizon_logic_str = (
            "** Reading input data for the selected day\n"
            "loop(day$(ord(day) eq N+counter),\n"
            "    g_max(i, b) = g_max_day(day, i, b)/s_base;\n"
            "    k(i, b) = k_day(day, i, b)*s_base;\n"
            "    g_0(i) = g_0_day(day, i)/s_base;\n"
            "    demand(s, t) = d_day(day, s, t)/s_base;\n"
            "    sol_deterministic(t, r) = sol_deterministic_day(day, t, r)/s_base;\n"
            "    fix_deterministic(f, t) = abs(fix_deterministic_day(day, f, t))/s_base;\n"
            "    wind_deterministic(t, w) = wind_deterministic_day(day, t, w)/s_base;\n"
            "    onoff_t0(i) = onoff_t0_day(day, i);\n"
            "    L_up_min(i) = L_up_min_day(day, i);\n"
            "    L_down_min(i) = L_down_min_day(day, i);\n"
            ");\n"
        )

        input_file.write(da_horizon_logic_str)

    # end input_time_horizon_logic
