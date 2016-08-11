# Header for congestion relief problem

import footdef

###############################################################################
# Footer                                                                      #
###############################################################################

def foot_solver_call(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    model_name = ('TEPO_UC', 'TEPO_CR', 'TEPO_CR', 'TEPO_UC')

    for k in range(len(file_list)):
        file_list[k].write(79*'*' + '\n')
        file_list[k].write('*** SOLVER CALL' + 63*' ' + '*\n')
        file_list[k].write(79*'*' + '\n\n')

        solve_str = (
            "model " + model_name[k] + " /all/;\n\n"
            "option reslim = 1000000;\n"
            "option optcr = 0.01;\n"
            "option threads = 1;\n\n"
            "solve " + model_name[k] + " using mip minimizing obj;\n\n"
        )

        file_list[k].write(solve_str)

        if k < len(file_list) - 1:
            file_list[k].write(79*'*' + '\n')
            file_list[k].write('*** CSV OUTPUT FILES' + 58*' ' + '*\n')
            file_list[k].write(79*'*' + '\n\n')

    # end foot_solver_call


def foot_conventional_generators(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]

    conventional_generators = footdef.Putfile()
    conventional_generators.comment = "Conventional generator power output"
    conventional_generators.file_label = 'output1'
    conventional_generators.file_path = path_dict['data_path'] + 'gbis.csv'
    conventional_generators.header_str = "Conventional generator power output"
    conventional_generators.hour_ahead = hour_ahead
    conventional_generators.index_var = 'i'
    conventional_generators.put_precision = 4
    conventional_generators.put_quantity = 'g.l(t, i)'

    conventional_generators.write_put_file(uc_list[0])

    # end foot_conventional_generators


def foot_power_blocks(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]

    # block_one
    block_one = footdef.Putfile()
    block_one.comment = "Conventional generator power output of first block"
    block_one.file_label = 'output2A'
    block_one.file_path = path_dict['data_path'] + 'glin_bisA.csv'
    block_one.header_str = "Power output of block 1"
    block_one.hour_ahead = hour_ahead
    block_one.index_var = 'i'
    block_one.put_precision = 4
    block_one.put_quantity = 'g_lin.l(t, i, \'b1\')'

    block_one.write_put_file(uc_list[0])

    # block_two
    block_two = footdef.Putfile()
    block_two.comment = "Conventional generator power output of second block"
    block_two.file_label = 'output2B'
    block_two.file_path = path_dict['data_path'] + 'glin_bisB.csv'
    block_two.header_str = "Power output of block 2"
    block_two.hour_ahead = hour_ahead
    block_two.index_var = 'i'
    block_two.put_precision = 4
    block_two.put_quantity = 'g_lin.l(t, i, \'b2\')'

    block_two.write_put_file(uc_list[0])

    # block_three
    block_three = footdef.Putfile()
    block_three.comment = "Conventional generator power output of third block"
    block_three.file_label = 'output2C'
    block_three.file_path = path_dict['data_path'] + 'glin_bisC.csv'
    block_three.header_str = "Power output of block 3"
    block_three.hour_ahead = hour_ahead
    block_three.index_var = 'i'
    block_three.put_precision = 4
    block_three.put_quantity = 'g_lin.l(t, i, \'b3\')'

    block_three.write_put_file(uc_list[0])

    # end foot_power_blocks


def foot_slack_spillage(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]

    # slack_wind
    slack_wind = footdef.Putfile()
    slack_wind.comment = "Wind spillage output"
    slack_wind.file_label = 'output3'
    slack_wind.file_path = path_dict['data_path'] + 'slackwindbis.csv'
    slack_wind.header_str = "Wind spillage"
    slack_wind.hour_ahead = hour_ahead
    slack_wind.index_var = 'w'
    slack_wind.put_precision = 4
    slack_wind.put_quantity = 'slack_wind.l(w, t)'

    slack_wind.write_put_file(uc_list[0])

    # slack_solar
    slack_solar = footdef.Putfile()
    slack_solar.comment = "Solar spillage output"
    slack_solar.file_label = 'output4'
    slack_solar.file_path = path_dict['data_path'] + 'slacksolarbis.csv'
    slack_solar.header_str = "Solar spillage"
    slack_solar.hour_ahead = hour_ahead
    slack_solar.index_var = 'r'
    slack_solar.put_precision = 4
    slack_solar.put_quantity = 'slack_solar.l(r, t)'

    slack_solar.write_put_file(uc_list[0])

    # slack_fixed
    slack_fixed = footdef.Putfile()
    slack_fixed.comment = "Fixed generation spillage output"
    slack_fixed.file_label = 'output5'
    slack_fixed.file_path = path_dict['data_path'] + 'slackfixedbis.csv'
    slack_fixed.header_str = "Fixed generation spillage"
    slack_fixed.hour_ahead = hour_ahead
    slack_fixed.index_var = 'f'
    slack_fixed.put_precision = 4
    slack_fixed.put_quantity = 'slack_fixed.l(f, t)'

    slack_fixed.write_put_file(uc_list[0])

    # end foot_slack_spillage

def foot_line_flows(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]

    # slack_fixed
    line_flows = footdef.Putfile()
    line_flows.comment = "Power flow on each transmission line"
    line_flows.file_label = 'output6'
    line_flows.file_path = path_dict['data_path'] + 'powerflow.csv'
    line_flows.header_str = "Transmission line power flows"
    line_flows.hour_ahead = hour_ahead
    line_flows.index_var = 'l'
    line_flows.put_precision = 4
    line_flows.put_quantity = 'pf.l(t, l)'

    line_flows.write_put_file(uc_list[0])

    # end foot_line_flows


def foot_congestion_forecast(file_list, hour_ahead, path_dict):

    cf_list = file_list[1:3]

    # pext
    pext = footdef.Putfile()
    pext.comment = "Power extracted from the energy storage device"
    pext.file_label = 'pext_output'
    pext.file_path = path_dict['data_path'] + 'pext.csv'
    pext.header_str = "Power extracted from energy storage device"
    pext.hour_ahead = hour_ahead
    pext.index_var = 'd'
    pext.put_precision = 4
    pext.put_quantity = 'ch_total.l(t, d) - dis_total.l(t, d)'

    pext.write_put_file(cf_list[0])

    pext.file_label = 'pext2_output'
    pext.file_path = path_dict['data_path'] + 'pext_2round.csv'

    pext.write_put_file(cf_list[1])

    action_str = (
        "** Defining the ESS actions based on the power extracted\n"
        "loop((s, d)$(storage_map(d) eq ord(s)),\n"
        "    action_aux(t, s)$((M_cong(t) eq 1)\n"
        "                 and ((ch_total.l(t, d) - dis_total.l(t, d)) gt 0)) = 1 + eps;\n\n"
        "    action_aux(t, s)$((M_cong(t) eq 1)\n"
        "                 and ((ch_total.l(t, d) - dis_total.l(t, d)) lt 0)) = -1 + eps;\n\n"
        "    action_aux(t, s)$((M_cong(t) eq 1)\n"
        "                 and ((ch_total.l(t, d) - dis_total.l(t, d)) eq 0)) = 0 + eps;\n\n"
        ");\n\n"
        "loop((s, d)$(storage_map(d) eq ord(s)),\n"
        "    action(t, d) = action_aux(t, s);\n"
        ");\n\n"
        "display soc.l, ch_total.l, dis_total.l;\n\n"
    )

    cf_list[0].write(action_str)

    min_max_load_str = (
        "** Minimum and maximum net load injections\n"
        "loop((s,d)$(storage_map(d) eq ord(s)),\n"
        "    minimum_load_aux(t, s)$(((ch_total.l(t, d) - dis_total.l(t, d)) gt 0)) = \n"
        "        (demand(s, t) + (ch_total.l(t, d) - dis_total.l(t, d)))*s_base + eps;\n\n"
        "    minimum_load_aux(t, s)$(((ch_total.l(t, d) - dis_total.l(t, d)) lt 0)) = \n"
        "        (demand(s, t) - ES_power_max(d))*s_base + eps;\n\n"
        "    minimum_load_aux(t, s)$(((ch_total.l(t, d) - dis_total.l(t, d)) eq 0)) = \n"
        "        demand(s, t)*s_base + eps;\n"
        ");\n\n"
        "loop((s, d)$(storage_map(d) eq ord(s)),\n"
        "    maximum_load_aux(t, s)$(((ch_total.l(t, d) - dis_total.l(t, d)) gt 0)) =\n"
        "        (demand(s, t) + ES_power_max(d))*s_base + eps;\n\n"
        "    maximum_load_aux(t, s)$(((ch_total.l(t, d) - dis_total.l(t, d)) lt 0)) =\n"
        "        (demand(s, t) + (ch_total.l(t, d) - dis_total.l(t, d)))*s_base + eps;\n\n"
        "    maximum_load_aux(t, s)$(((ch_total.l(t, d) - dis_total.l(t, d)) eq 0)) =\n"
        "        demand(s, t)*s_base + eps;\n"
        ");\n\n"
        "loop((s, d)$(storage_map(d) eq ord(s)),\n"
        "    minimum_load(t, d) = minimum_load_aux(t, s);\n"
        "    maximum_load(t, d) = maximum_load_aux(t, s);\n"
        ");\n\n"
    )

    cf_list[1].write(min_max_load_str)

    # end foot_congestion_forecast


def foot_cf1_tepo_depo_exchange(file_list, hour_ahead, path_dict):

    cf_list = file_list[1:3]

    cf_list[0].write(79*'*' + '\n')
    cf_list[0].write('*** OUTPUT FILES FROM TEPO TO DEPO' + 44*' ' + '*\n')
    cf_list[0].write(79*'*' + '\n\n')

    cf_list[0].write("option decimals = 6;\n\n")

    ES_info_str = path_dict['depo_path'] + 'ES_information.csv'

    write_es_info_str = (
        'file ES_information_output /\'' + ES_info_str + '\'/;\n'
        'put ES_information_output;\n'
        'put \"** MAP ENERGY STORAGE - BUS, AREA, ZONE **\"/;\n'
        'put \"** AREA = 122 ----> BPA AREA \"/;\n'
        'put \"** ZONE = 468 ----> SNOPUD ZONE \"/;\n'
        'put "BUS, AREA, ZONE",\n\n'
        'put /;\n'
        'loop(d,\n'
        '    put d.tl:0:0, \",\"\n'
        '    put (storage_map(d)):0:0, \",\", (storage_area(d)):0:0, \",\", (storage_zone(d)):0:0,\n'
        'put /;\n'
        ');\n\n'
    )

    cf_list[0].write(write_es_info_str)

    # action_out
    action_out = footdef.Putfile()
    action_out.comment = "Action required for congestion relief"
    action_out.file_label = 'Action_output'
    action_out.file_path = path_dict['depo_path'] + 'Action.csv'
    action_out.header_str = "Action required for congestion relief"
    action_out.hour_ahead = hour_ahead
    action_out.index_var = 'd'
    action_out.put_precision = 0
    action_out.put_quantity = 'action(t, d)'
    action_out.rename_flag = True
    action_out.rename_str = path_dict['depo_path'] + "Action_':0 N:1:0 '.csv"

    action_out.write_put_file(cf_list[0])

    # load_forecast
    load_forecast = footdef.Putfile()
    load_forecast.comment = \
        "Load forecast at buses where storage devices are located"
    load_forecast.file_label = 'Load_forecast_output'
    load_forecast.file_path = path_dict['depo_path'] + 'Load_forecast.csv'
    load_forecast.header_str = "Load forecast at storage buses"
    load_forecast.hour_ahead = hour_ahead
    load_forecast.index_var = 'd'
    load_forecast.put_precision = 4
    load_forecast.put_quantity = \
        'sum(s$(storage_map(d) eq ord(s)), demand(s, t)*s_base)'
    load_forecast.rename_flag = True
    load_forecast.rename_str = path_dict['depo_path'] + "Load_forecast_':0 N:1:0 '.csv"

    load_forecast.write_put_file(cf_list[0])

    # end foot_cf1_tepo_depo_exchange


def foot_cf2_tepo_depo_exchange(file_list, hour_ahead, path_dict):

    cf_list = file_list[1:3]

    cf_list[1].write(79*'*' + '\n')
    cf_list[1].write('*** OUTPUT FILES FROM TEPO TO DEPO' + 44*' ' + '*\n')
    cf_list[1].write(79*'*' + '\n\n')

    cf_list[1].write("option decimals = 6;\n\n")

    # min_load
    min_load = footdef.Putfile()
    min_load.comment = \
        "Minimum load at buses where storage devices are located"
    min_load.file_label = 'Minimum_load_output'
    min_load.file_path = path_dict['depo_path'] + 'Minimum_load.csv'
    min_load.header_str = "Minimum load at storage buses"
    min_load.hour_ahead = hour_ahead
    min_load.index_var = 'd'
    min_load.put_precision = 4
    min_load.put_quantity = 'minimum_load(t, d)'
    min_load.rename_flag = True
    min_load.rename_str = path_dict['depo_path'] + "Minimum_load_':0 N:1:0 '.csv"

    min_load.write_put_file(cf_list[1])

    # max_load
    max_load = footdef.Putfile()
    max_load.comment = \
        "Maximum load at buses where storage devices are located"
    max_load.file_label = 'Maximum_load_output'
    max_load.file_path = path_dict['depo_path'] + 'Maximum_load.csv'
    max_load.header_str = "Maximum load at storage buses"
    max_load.hour_ahead = hour_ahead
    max_load.index_var = 'd'
    max_load.put_precision = 4
    max_load.put_quantity = 'maximum_load(t, d)'
    max_load.rename_flag = True
    max_load.rename_str = path_dict['depo_path'] + "Maximum_load_':0 N:1:0 '.csv"

    max_load.write_put_file(cf_list[1])

    # end foot_cf2_tepo_depo_exchange
