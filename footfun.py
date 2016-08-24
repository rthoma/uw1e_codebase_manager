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
            "option optcr = 0.001;\n"
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
    action_out.rename_str = path_dict['depo_path']

    if hour_ahead:
        action_out.rename_str += "Action_':0 N:1:0 '_H':0 hour:2:0 '.csv"
    else:
        action_out.rename_str += "Action_':0 N:1:0 '.csv"

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
    load_forecast.rename_str = path_dict['depo_path']

    if hour_ahead:
        load_forecast.rename_str += "Load_forecast_':0 N:1:0 '_H':0 hour:2:0 '.csv"
    else:
        load_forecast.rename_str += "Load_forecast_':0 N:1:0 '.csv"

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
    min_load.rename_str = path_dict['depo_path']

    if hour_ahead:
        min_load.rename_str += "Minimum_load_':0 N:1:0 '_H':0 hour:2:0 '.csv"
    else:
        min_load.rename_str += "Minimum_load_':0 N:1:0 '.csv"

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
    max_load.rename_str = path_dict['depo_path']

    if hour_ahead:
        max_load.rename_str += "Maximum_load_':0 N:1:0 '_H':0 hour:2:0 '.csv"
    else:
        max_load.rename_str += "Maximum_load_':0 N:1:0 '.csv"

    max_load.write_put_file(cf_list[1])

    # end foot_cf2_tepo_depo_exchange


def output_unload_uc1(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    for k in range(len(file_list)):
        file_list[k].write(79*'*' + '\n')
        file_list[k].write('*** UNLOADING OUTPUTS' + 57*' ' + '*\n')
        file_list[k].write(79*'*' + '\n\n')

    param_str = (
        "parameters\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux(t, l),\n"
        "    M_cong_snpd_aux(t, l),\n"
        "    flow_cong_output(l, t),\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out(t, l),\n"
        "    power_output_out(t, i),\n"
        "    slack_solar_out(r, t),\n"
        "    slack_wind_out(w, t),\n"
        "    slack_fixed_out(f, t),\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total\n"
        ";\n\n"
    )

    output_eq_str = "** Output equations\n\n"

    if hour_ahead:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i)$(t_ha(t)), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                              + sum(b, g_lin.l(t, i, b)*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r)$(t_ha(t)), slack_solar.l(r, t))*VoRS\n"
            "           + sum((t, w)$(t_ha(t)), slack_wind.l(w, t))*VoRS\n"
            "           + sum((t, f)$(t_ha(t)), slack_fixed.l(f, t))*VoFS + eps;\n\n"
            "time_elapsed = timeElapsed;\n\n"
            "M_cong_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) - l_max(l) ge 0)) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) - l_max(l) ge 0)\n"
            "                               and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(t_ha(t) and (M_cong_aux(t, l) gt 0.5)) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_UC.modelstat;\n"
            "sst = TEPO_UC.solvestat;\n\n"
            "power_flow_out(t, l)$(t_ha(t)) = pf.l(t, l)$(t_ha(t))*s_base + eps;\n"
            "power_output_out(t, i)$(t_ha(t)) = g.l(t, i)$(t_ha(t))*s_base + eps;\n\n"
            "slack_solar_out(r, t)$(t_ha(t)) = slack_solar.l(r, t)$(t_ha(t))*s_base + eps;\n"
            "slack_wind_out(w, t)$(t_ha(t)) = slack_wind.l(w, t)$(t_ha(t))*s_base + eps;\n"
            "slack_fixed_out(f, t)$(t_ha(t)) = slack_fixed.l(f, t)$(t_ha(t))*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t)$(t_ha(t)), slack_solar.l(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t)$(t_ha(t)), slack_wind.l(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t)$(t_ha(t)), slack_fixed.l(f, t))*s_base + eps;\n\n"
        )
    else:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                      + sum(b, g_lin.l(t, i, b)*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r), slack_solar.l(r, t))*VoRS\n"
            "           + sum((t, w), slack_wind.l(w, t))*VoRS\n"
            "           + sum((t, f), slack_fixed.l(f, t))*VoFS + eps;\n\n"
            "time_elapsed = timeElapsed;\n\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) - l_max(l) ge 0) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) - l_max(l) ge 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) gt 0.5) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_UC.modelstat;\n"
            "sst = TEPO_UC.solvestat;\n\n"
            "power_flow_out(t, l) = pf.l(t, l)*s_base + eps;\n"
            "power_output_out(t, i) = g.l(t, i)*s_base + eps;\n\n"
            "slack_solar_out(r, t) = slack_solar.l(r, t)*s_base + eps;\n"
            "slack_wind_out(w, t) = slack_wind.l(w, t)*s_base + eps;\n"
            "slack_fixed_out(f, t) = slack_fixed.l(f, t)*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t), slack_solar.l(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t), slack_wind.l(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t), slack_fixed.l(f, t))*s_base + eps;\n\n"
        )

    unload_path = path_dict['data_path']

    unload_str = (
        "** Generating the output file\n\n"
        "file uc1_gdxout;\n"
        "put uc1_gdxout\n"
    )

    unload_str += "put_utility 'gdxout' / '"
    unload_str += unload_path + "TEPO_UC1_day':0 N:1:0 '_1ES.gdx':0;\n\n"

    unload_str += (
        "execute_unload\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux,\n"
        "    M_cong_snpd_aux,\n"
        "    flow_cong_output,\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out,\n"
        "    power_output_out,\n"
        "    slack_solar_out,\n"
        "    slack_wind_out,\n"
        "    slack_fixed_out,\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total\n"
        ";"
    )

    uc_list[0].write(param_str)
    uc_list[0].write(output_eq_str)
    uc_list[0].write(unload_str)

    # end output_unload_uc1


def output_unload_uc2(file_list, hour_ahead, path_dict):

    uc_list = file_list[0:4:3]

    param_str = (
        "parameters\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux(t, l),\n"
        "    M_cong_snpd_aux(t, l),\n"
        "    flow_cong_output(l, t),\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out(t, l),\n"
        "    power_output_out(t, i),\n"
        "    slack_solar_out(r, t),\n"
        "    slack_wind_out(w, t),\n"
        "    slack_fixed_out(f, t),\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total,\n"
        "    slack_pbal_out(s, t),\n"
        "    slack_flow_out(l, t)\n"
        ";\n\n"
    )

    output_eq_str = "** Output equations\n\n"

    if hour_ahead:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i)$(t_ha(t)), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                              + sum(b, g_lin.l(t, i, b)*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r)$(t_ha(t)), slack_solar.l(r, t))*VoRS\n"
            "           + sum((t, w)$(t_ha(t)), slack_wind.l(w, t))*VoRS\n"
            "           + sum((t, f)$(t_ha(t)), slack_fixed.l(f, t))*VoFS\n"
            "           + sum((t, s)$(t_ha(t)), slack_pbal.l(s, t))*INFEASIBLE_PENALTY\n"
            "           + sum((t, l)$(t_ha(t)), slack_flow.l(l, t))*INFEASIBLE_PENALTY + eps;\n\n"
            "time_elapsed = timeElapsed;\n\n"
            "M_cong_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) + eps - l_max(l) ge 0)) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) + eps - l_max(l) ge 0)\n"
            "                               and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(t_ha(t) and (M_cong_aux(t, l) gt 0.5)) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_UC.modelstat;\n"
            "sst = TEPO_UC.solvestat;\n\n"
            "power_flow_out(t, l)$(t_ha(t)) = pf.l(t, l)$(t_ha(t))*s_base + eps;\n"
            "power_output_out(t, i)$(t_ha(t)) = g.l(t, i)$(t_ha(t))*s_base + eps;\n\n"
            "slack_solar_out(r, t)$(t_ha(t)) = slack_solar.l(r, t)$(t_ha(t))*s_base + eps;\n"
            "slack_wind_out(w, t)$(t_ha(t)) = slack_wind.l(w, t)$(t_ha(t))*s_base + eps;\n"
            "slack_fixed_out(f, t)$(t_ha(t)) = slack_fixed.l(f, t)$(t_ha(t))*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t)$(t_ha(t)), slack_solar.l(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t)$(t_ha(t)), slack_wind.l(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t)$(t_ha(t)), slack_fixed.l(f, t))*s_base + eps;\n\n"
            "slack_pbal_out(s, t)$(t_ha(t)) = slack_pbal.l(s, t)$(t_ha(t))*s_base + eps;\n"
            "slack_flow_out(l, t)$(t_ha(t)) = slack_flow.l(l, t)$(t_ha(t))*s_base + eps;\n\n"
        )
    else:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                      + sum(b, g_lin.l(t, i, b)*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r), slack_solar.l(r, t))*VoRS\n"
            "           + sum((t, w), slack_wind.l(w, t))*VoRS\n"
            "           + sum((t, f), slack_fixed.l(f, t))*VoFS\n"
            "           + sum((t, s), slack_pbal.l(s, t))*INFEASIBLE_PENALTY\n"
            "           + sum((t, l), slack_flow.l(l, t))*INFEASIBLE_PENALTY + eps;\n\n"
            "time_elapsed = timeElapsed;\n\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) ge 0) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) ge 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) gt 0.5) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_UC.modelstat;\n"
            "sst = TEPO_UC.solvestat;\n\n"
            "power_flow_out(t, l) = pf.l(t, l)*s_base + eps;\n"
            "power_output_out(t, i) = g.l(t, i)*s_base + eps;\n\n"
            "slack_solar_out(r, t) = slack_solar.l(r, t)*s_base + eps;\n"
            "slack_wind_out(w, t) = slack_wind.l(w, t)*s_base + eps;\n"
            "slack_fixed_out(f, t) = slack_fixed.l(f, t)*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t), slack_solar.l(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t), slack_wind.l(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t), slack_fixed.l(f, t))*s_base + eps;\n\n"
            "slack_pbal_out(s, t) = slack_pbal.l(s, t)*s_base + eps;\n"
            "slack_flow_out(l, t) = slack_flow.l(l, t)*s_base + eps;\n\n"
        )

    unload_path = path_dict['data_path']

    unload_str = (
        "** Generating the output file\n\n"
        "file uc2_gdxout;\n"
        "put uc2_gdxout\n"
    )

    unload_str += "put_utility 'gdxout' / '"
    unload_str += unload_path + "TEPO_UC2_day':0 N:1:0 '_1ES.gdx':0;\n\n"

    unload_str += (
        "execute_unload\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux,\n"
        "    M_cong_snpd_aux,\n"
        "    flow_cong_output,\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out,\n"
        "    power_output_out,\n"
        "    slack_solar_out,\n"
        "    slack_wind_out,\n"
        "    slack_fixed_out,\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total,\n"
        "    slack_pbal_out,\n"
        "    slack_flow_out\n"
        ";"
    )

    uc_list[1].write(param_str)
    uc_list[1].write(output_eq_str)
    uc_list[1].write(unload_str)

    # end output_unload_uc2


def output_unload_cf1(file_list, hour_ahead, path_dict):

    cf_list = file_list[1:3]

    param_str = (
        "parameters\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    ess_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux(t, l),\n"
        "    M_cong_snpd_aux(t, l),\n"
        "    flow_cong_output(l, t),\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out(t, l),\n"
        "    power_output_out(t, i),\n"
        "    slack_solar_out(r, t),\n"
        "    slack_wind_out(w, t),\n"
        "    slack_fixed_out(f, t),\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total\n"
        ";\n\n"
    )

    output_eq_str = "** Output equations\n\n"

    if hour_ahead:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i)$(t_ha(t)), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                              + sum(b, (deltag_lin_plus.l(t, i, b)\n"
            "                                      + deltag_lin_minus.l(t, i, b))*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r)$(t_ha(t)), slack_solar_plus.l(t, r)\n"
            "                                 + slack_solar_minus.l(t, r))*penalty_pf\n"
            "           + sum((t, w)$(t_ha(t)), slack_wind_plus.l(t, w)\n"
            "                                 + slack_wind_minus.l(t, w))*penalty_pf\n"
            "           + sum((f, t)$(t_ha(t)), slack_fixed_plus.l(t, f)\n"
            "                                 + slack_fixed_minus.l(t, f))*penalty_pf + eps;\n\n"
            "ess_cost = sum((t, d)$(t_ha(t) and (ch_ini(d, t) ge 0)),\n"
            "                                    ch_TEPO.l(t, d)*2*ESS_ADJUST_PENALTY)\n"
            "         + sum((t, d)$(t_ha(t) and (dis_ini(d, t) ge 0)),\n"
            "                                    dis_TEPO.l(t, d)*2*ESS_ADJUST_PENALTY)\n"
            "         + sum((t, d)$(t_ha(t) and (ch_ini(d, t) gt 0)),\n"
            "                                    dis_TEPO_SC.l(t, d)*3*ESS_ADJUST_PENALTY)\n"
            "         + sum((t, d)$(t_ha(t) and (dis_ini(d, t) gt 0)),\n"
            "                                    ch_TEPO_SD.l(t, d)*3*ESS_ADJUST_PENALTY)\n"
            "         + sum((t, d)$(t_ha(t) and (dis_ini(d, t) gt 0)),\n"
            "                                    ch_TEPO.l(t, d)*6*ESS_ADJUST_PENALTY)\n"
            "         + sum((t, d)$(t_ha(t) and (ch_ini(d, t) gt 0)),\n"
            "                                    dis_TEPO.l(t, d)*6*ESS_ADJUST_PENALTY) + eps;\n\n"
            "M_cong_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) + eps - l_max(l) ge 0)) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) + eps - l_max(l) ge 0)\n"
            "                               and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(t_ha(t) and (M_cong_aux(t, l) gt 0.5)) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_CR.modelstat;\n"
            "sst = TEPO_CR.solvestat;\n\n"
            "power_flow_out(t, l)$(t_ha(t)) = pf.l(t, l)$(t_ha(t))*s_base + eps;\n\n"
            "power_output_out(t, i)$(t_ha(t)) = (gbis(t, i)$(t_ha(t))\n"
            "                                  + deltag_plus.l(t, i)$(t_ha(t))\n"
            "                                  - deltag_minus.l(t, i)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_solar_out(r, t)$(t_ha(t)) = (slack_solar_bis(r, t)$(t_ha(t))\n"
            "                                 + slack_solar_plus.l(t, r)$(t_ha(t))\n"
            "                                 - slack_solar_minus.l(t, r)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_wind_out(w, t)$(t_ha(t)) = (slack_wind_bis(w, t)$(t_ha(t))\n"
            "                                + slack_wind_plus.l(t, w)$(t_ha(t))\n"
            "                                - slack_wind_minus.l(t, w)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_fixed_out(f, t)$(t_ha(t)) = (slack_fixed_bis(f, t)$(t_ha(t))\n"
            "                                 + slack_fixed_plus.l(t, f)$(t_ha(t))\n"
            "                                 - slack_fixed_minus.l(t, f)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t)$(t_ha(t)), slack_solar_out(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t)$(t_ha(t)), slack_wind_out(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t)$(t_ha(t)), slack_fixed_out(f, t))*s_base + eps;\n\n"
        )
    else:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                      + sum(b, (deltag_lin_plus.l(t, i, b)\n"
            "                              + deltag_lin_minus.l(t, i, b))*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r), slack_solar_plus.l(t, r)\n"
            "                       + slack_solar_minus.l(t, r))*penalty_pf\n"
            "           + sum((t, w), slack_wind_plus.l(t, w)\n"
            "                       + slack_wind_minus.l(t, w))*penalty_pf\n"
            "           + sum((f, t), slack_fixed_plus.l(t, f)\n"
            "                       + slack_fixed_minus.l(t, f))*penalty_pf + eps;\n\n"
            "ess_cost = sum((t, d), ch_total.l(t, d)\n"
            "                     + dis_total.l(t, d))*ESS_ADJUST_PENALTY + eps;\n\n"
            "time_elapsed = timeElapsed;\n\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) ge 0) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) ge 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) gt 0.5) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_CR.modelstat;\n"
            "sst = TEPO_CR.solvestat;\n\n"
            "power_flow_out(t, l) = pf.l(t, l)*s_base + eps;\n\n"
            "power_output_out(t, i) = (gbis(t, i)\n"
            "                        + deltag_plus.l(t, i)\n"
            "                        - deltag_minus.l(t, i))*s_base + eps;\n\n"
            "slack_solar_out(r, t) = (slack_solar_bis(r, t)\n"
            "                       + slack_solar_plus.l(t, r)\n"
            "                       - slack_solar_minus.l(t, r))*s_base + eps;\n\n"
            "slack_wind_out(w, t) = (slack_wind_bis(w, t)\n"
            "                      + slack_wind_plus.l(t, w)\n"
            "                      - slack_wind_minus.l(t, w))*s_base + eps;\n\n"
            "slack_fixed_out(f, t) = (slack_fixed_bis(f, t)\n"
            "                       + slack_fixed_plus.l(t, f)\n"
            "                       - slack_fixed_minus.l(t, f))*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t), slack_solar_out(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t), slack_wind_out(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t), slack_fixed_out(f, t))*s_base + eps;\n\n"
        )

    unload_path = path_dict['data_path']

    unload_str = (
        "** Generating the output file\n\n"
        "file cr1_gdxout;\n"
        "put cr1_gdxout\n"
    )

    unload_str += "put_utility 'gdxout' / '"
    unload_str += unload_path + "TEPO_CR1_day':0 N:1:0 '_1ES.gdx':0;\n\n"

    unload_str += (
        "execute_unload\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    ess_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux,\n"
        "    M_cong_snpd_aux,\n"
        "    flow_cong_output,\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out,\n"
        "    power_output_out,\n"
        "    slack_solar_out,\n"
        "    slack_wind_out,\n"
        "    slack_fixed_out,\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total\n"
        ";"
    )

    cf_list[0].write(param_str)
    cf_list[0].write(output_eq_str)
    cf_list[0].write(unload_str)

    # end output_unload_cf1


def output_unload_cf2(file_list, hour_ahead, path_dict):

    cf_list = file_list[1:3]

    param_str = (
        "parameters\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    ess_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux(t, l),\n"
        "    M_cong_snpd_aux(t, l),\n"
        "    flow_cong_output(l, t),\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out(t, l),\n"
        "    power_output_out(t, i),\n"
        "    slack_solar_out(r, t),\n"
        "    slack_wind_out(w, t),\n"
        "    slack_fixed_out(f, t),\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total,\n"
        "    slack_pbal_out(s, t)\n"
        ";\n\n"
    )

    output_eq_str = "** Output equations\n\n"

    if hour_ahead:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i)$(t_ha(t)), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                              + sum(b, (deltag_lin_plus.l(t, i, b)\n"
            "                                      + deltag_lin_minus.l(t, i, b))*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r)$(t_ha(t)), slack_solar_plus.l(t, r)\n"
            "                                 + slack_solar_minus.l(t, r))*penalty_pf\n"
            "           + sum((t, w)$(t_ha(t)), slack_wind_plus.l(t, w)\n"
            "                                 + slack_wind_minus.l(t, w))*penalty_pf\n"
            "           + sum((f, t)$(t_ha(t)), slack_fixed_plus.l(t, f)\n"
            "                                 + slack_fixed_minus.l(t, f))*penalty_pf\n"
            "           + sum((s, t)$(t_ha(t)), slack_pbal.l(s, t))*INFEASIBLE_PENALTY + eps;\n\n"
            "ess_cost = sum((t, d)$(t_ha(t) and (ch_ini(d, t) ge 0)),\n"
            "                                    ch_TEPO.l(t, d)*C_ch(d, t))\n"
            "         + sum((t, d)$(t_ha(t) and (dis_ini(d, t) ge 0)),\n"
            "                                    dis_TEPO.l(t, d)*C_dis(d, t))\n"
            "         + sum((t, d)$(t_ha(t) and (ch_ini(d, t) gt 0)),\n"
            "                                    dis_TEPO_SC.l(t, d)*C_SC(d, t))\n"
            "         + sum((t, d)$(t_ha(t) and (dis_ini(d, t) gt 0)),\n"
            "                                    ch_TEPO_SD.l(t, d)*C_SD(d, t))\n"
            "         + sum((t, d)$(t_ha(t) and (dis_ini(d, t) gt 0)),\n"
            "                                    ch_TEPO.l(t, d)*P_ch(d, t))\n"
            "         + sum((t, d)$(t_ha(t) and (ch_ini(d, t) gt 0)),\n"
            "                                    dis_TEPO.l(t, d)*P_dis(d, t)) + eps;\n\n"
            "M_cong_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) + eps - l_max(l) ge 0)) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$(t_ha(t) and (abs(pf.l(t, l)) + eps - l_max(l) ge 0)\n"
            "                               and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(t_ha(t) and (M_cong_aux(t, l) gt 0.5)) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_CR.modelstat;\n"
            "sst = TEPO_CR.solvestat;\n\n"
            "power_flow_out(t, l)$(t_ha(t)) = pf.l(t, l)$(t_ha(t))*s_base + eps;\n\n"
            "power_output_out(t, i)$(t_ha(t)) = (gbis(t, i)$(t_ha(t))\n"
            "                                  + deltag_plus.l(t, i)$(t_ha(t))\n"
            "                                  - deltag_minus.l(t, i)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_solar_out(r, t)$(t_ha(t)) = (slack_solar_bis(r, t)$(t_ha(t))\n"
            "                                 + slack_solar_plus.l(t, r)$(t_ha(t))\n"
            "                                 - slack_solar_minus.l(t, r)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_wind_out(w, t)$(t_ha(t)) = (slack_wind_bis(w, t)$(t_ha(t))\n"
            "                                + slack_wind_plus.l(t, w)$(t_ha(t))\n"
            "                                - slack_wind_minus.l(t, w)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_fixed_out(f, t)$(t_ha(t)) = (slack_fixed_bis(f, t)$(t_ha(t))\n"
            "                                 + slack_fixed_plus.l(t, f)$(t_ha(t))\n"
            "                                 - slack_fixed_minus.l(t, f)$(t_ha(t)))*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t)$(t_ha(t)), slack_solar_out(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t)$(t_ha(t)), slack_wind_out(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t)$(t_ha(t)), slack_fixed_out(f, t))*s_base + eps;\n\n"
            "slack_pbal_out(s, t)$(t_ha(t)) = slack_pbal.l(s, t)$(t_ha(t))*s_base + eps;\n\n"
        )
    else:
        output_eq_str += (
            "total_cost = obj.L;\n\n"
            "generation_cost = sum((t, i), suc_sw(i)*y.l(t, i) + a(i)*v.l(t, i)\n"
            "                      + sum(b, (deltag_lin_plus.l(t, i, b)\n"
            "                              + deltag_lin_minus.l(t, i, b))*k(i, b))) + eps;\n\n"
            "slack_cost = sum((t, r), slack_solar_plus.l(t, r)\n"
            "                       + slack_solar_minus.l(t, r))*penalty_pf\n"
            "           + sum((t, w), slack_wind_plus.l(t, w)\n"
            "                       + slack_wind_minus.l(t, w))*penalty_pf\n"
            "           + sum((f, t), slack_fixed_plus.l(t, f)\n"
            "                       + slack_fixed_minus.l(t, f))*penalty_pf\n"
            "           + sum((s, t), slack_pbal.l(s, t))*INFEASIBLE_PENALTY + eps;\n\n"
            "ess_cost = sum((t, d)$(ch_ini(d, t) ge 0),\n"
            "                       ch_TEPO.l(t, d)*C_ch(d, t))\n"
            "         + sum((t, d)$(dis_ini(d, t) ge 0),\n"
            "                       dis_TEPO.l(t, d)*C_dis(d, t))\n"
            "         + sum((t, d)$(ch_ini(d, t) gt 0),\n"
            "                       dis_TEPO_SC.l(t, d)*C_SC(d, t))\n"
            "         + sum((t, d)$(dis_ini(d, t) gt 0),\n"
            "                       ch_TEPO_SD.l(t, d)*C_SD(d, t))\n"
            "         + sum((t, d)$(dis_ini(d, t) gt 0),\n"
            "                       ch_TEPO.l(t, d)*P_ch(d, t))\n"
            "         + sum((t, d)$(ch_ini(d, t) gt 0),\n"
            "                       dis_TEPO.l(t, d)*P_dis(d, t)) + eps;\n\n"
            "time_elapsed = timeElapsed;\n\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) ge 0) = 1 + eps;\n"
            "M_cong_aux(t, l)$(abs(pf.l(t, l)) + eps - l_max(l) lt 0) = 0 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) ge 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 1 + eps;\n\n"
            "M_cong_snpd_aux(t, l)$((abs(pf.l(t, l)) + eps - l_max(l) lt 0)\n"
            "                       and (snpd_lines_map(l) eq 1)) = 0 + eps;\n\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) gt 0.5) = pf.l(t, l)*s_base + eps;\n"
            "flow_cong_output(l, t)$(M_cong_aux(t, l) le 0.5) = 0 + eps;\n\n"
            "mst = TEPO_CR.modelstat;\n"
            "sst = TEPO_CR.solvestat;\n\n"
            "power_flow_out(t, l) = pf.l(t, l)*s_base + eps;\n\n"
            "power_output_out(t, i) = (gbis(t, i)\n"
            "                        + deltag_plus.l(t, i)\n"
            "                        - deltag_minus.l(t, i))*s_base + eps;\n\n"
            "slack_solar_out(r, t) = (slack_solar_bis(r, t)\n"
            "                       + slack_solar_plus.l(t, r)\n"
            "                       - slack_solar_minus.l(t, r))*s_base + eps;\n\n"
            "slack_wind_out(w, t) = (slack_wind_bis(w, t)\n"
            "                      + slack_wind_plus.l(t, w)\n"
            "                      - slack_wind_minus.l(t, w))*s_base + eps;\n\n"
            "slack_fixed_out(f, t) = (slack_fixed_bis(f, t)\n"
            "                       + slack_fixed_plus.l(t, f)\n"
            "                       - slack_fixed_minus.l(t, f))*s_base + eps;\n\n"
            "slack_solar_out_total = sum((r, t), slack_solar_out(r, t))*s_base + eps;\n"
            "slack_wind_out_total = sum((w, t), slack_wind_out(w, t))*s_base + eps;\n"
            "slack_fixed_out_total = sum((f, t), slack_fixed_out(f, t))*s_base + eps;\n\n"
            "slack_pbal_out(s, t) = slack_pbal.l(s, t)*s_base + eps;\n\n"
        )

    unload_path = path_dict['data_path']

    unload_str = (
        "** Generating the output file\n\n"
        "file cr1_gdxout;\n"
        "put cr1_gdxout\n"
    )

    unload_str += "put_utility 'gdxout' / '"
    unload_str += unload_path + "TEPO_CR1_day':0 N:1:0 '_1ES.gdx':0;\n\n"

    unload_str += (
        "execute_unload\n"
        "    total_cost,\n"
        "    generation_cost,\n"
        "    slack_cost,\n"
        "    ess_cost,\n"
        "    time_elapsed,\n"
        "    M_cong_aux,\n"
        "    M_cong_snpd_aux,\n"
        "    flow_cong_output,\n"
        "    mst,\n"
        "    sst,\n"
        "    power_flow_out,\n"
        "    power_output_out,\n"
        "    slack_solar_out,\n"
        "    slack_wind_out,\n"
        "    slack_fixed_out,\n"
        "    slack_solar_out_total,\n"
        "    slack_wind_out_total,\n"
        "    slack_fixed_out_total,\n"
        "    slack_pbal_out\n"
        ";"
    )

    cf_list[1].write(param_str)
    cf_list[1].write(output_eq_str)
    cf_list[1].write(unload_str)

    # end output_unload_cf1
