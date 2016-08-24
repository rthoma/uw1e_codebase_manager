# Congestion relief problem

import optdef

###############################################################################
# Constraints                                                                 #
###############################################################################

def write_cost_function(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    for handle in file_list:
        handle.write(79*'*' + '\n')
        handle.write('*** CONSTRAINTS' + 63*' ' + '*\n')
        handle.write(79*'*' + '\n\n')

    cost = optdef.Constraint()
    cost.hour_ahead = hour_ahead
    cost.num_indent = 4
    cost.name = 'cost'
    cost.comment = 'Objective function'
    cost.operator = 'e'
    cost.lhs = 'obj'

    # UC Models

    cost.rhs = "sum((t, i)"
    cost.rhs += cost.hour_ahead*"$(t_ha(t))" + ', '
    cost.rhs += "suc_sw(i)*y(t, i) + a(i)*v(t, i)\n"
    cost.rhs += 16*' ' + "+ sum(b, g_lin(t, i, b)*k(i, b)))\n"

    sum_list = [
        ("sum((t, r)", "slack_solar(r, t))*VoRS\n"),
        ("sum((t, w)", "slack_wind(w, t))*VoRS\n"),
        ("sum((t, f)", "slack_fixed(f, t))*VoFS\n")
    ]

    for sum_tuple in sum_list:
        cost.rhs += 10*' ' + '+ ' + sum_tuple[0]
        cost.rhs += cost.hour_ahead*"$(t_ha(t))" + ', ' + sum_tuple[1]

    cost.write_constraint(uc_list[0])

    sum_list_extra = [
        ("sum((t, s)", "slack_pbal(s, t))*INFEASIBLE_PENALTY\n"),
        ("sum((t, l)", "slack_flow(l, t))*INFEASIBLE_PENALTY\n")
    ]

    for sum_tuple in sum_list_extra:
        cost.rhs += 10*' ' + '+ ' + sum_tuple[0]
        cost.rhs += cost.hour_ahead*"$(t_ha(t))" + ', ' + sum_tuple[1]

    cost.write_constraint(uc_list[1])

    # CF Model 1

    cost_cf_rhs_stub = "sum((t, i)"
    cost_cf_rhs_stub += cost.hour_ahead*"$(t_ha(t))" + ', '
    cost_cf_rhs_stub += "suc_sw(i)*y(t, i) + a(i)*v(t, i)\n"
    cost_cf_rhs_stub += (14 + cost.hour_ahead*10)*' '
    cost_cf_rhs_stub += "+ sum(b, (deltag_lin_plus(t, i, b)\n"
    cost_cf_rhs_stub += (22 + cost.hour_ahead*10)*' '
    cost_cf_rhs_stub += "+ deltag_lin_minus(t, i, b))*k(i, b)))\n"

    slack_sum_list = [
        ("sum((t, r)", "slack_solar_plus(t, r)",
                       "slack_solar_minus(t, r))*penalty_pf"),
        ("sum((t, w)", "slack_wind_plus(t, w)",
                       "slack_wind_minus(t, w))*penalty_pf"),
        ("sum((f, t)", "slack_fixed_plus(t, f)",
                       "slack_fixed_minus(t, f))*penalty_pf")
    ]

    for sum_tuple in slack_sum_list:
        cost_cf_rhs_stub += 10*' ' + '+ ' + sum_tuple[0]
        cost_cf_rhs_stub += cost.hour_ahead*'$(t_ha(t))'
        cost_cf_rhs_stub += ', ' + sum_tuple[1] + '\n'
        cost_cf_rhs_stub += (22 + 10*cost.hour_ahead)*' '
        cost_cf_rhs_stub += '+ ' + sum_tuple[2] + '\n'

    cost.rhs = cost_cf_rhs_stub

    if not cost.hour_ahead:
        cost.rhs += 10*' ' + "+ sum((t, d), ch_total(t, d)\n"
        cost.rhs += (22 + 10*cost.hour_ahead)*' '
        cost.rhs += "+ dis_total(t, d))*ESS_ADJUST_PENALTY\n"

        cost.write_constraint(cf_list[0])

        # end DA_CF_Model

    else:
        cost_dict = {
            'ch_TEPO_cost': '2*ESS_ADJUST_PENALTY',
            'dis_TEPO_cost': '2*ESS_ADJUST_PENALTY',
            'SC_TEPO_cost': '3*ESS_ADJUST_PENALTY',
            'SD_TEPO_cost': '3*ESS_ADJUST_PENALTY',
            'ch_TEPO_penalty': '6*ESS_ADJUST_PENALTY',
            'dis_TEPO_penalty': '6*ESS_ADJUST_PENALTY'
        }

        ess_sum_list = [
            ("sum((t, d)", "(ch_ini(d, t) ge 0)",
                           "ch_TEPO(t, d)*" + cost_dict['ch_TEPO_cost']),
            ("sum((t, d)", "(dis_ini(d, t) ge 0)",
                           "dis_TEPO(t, d)*" + cost_dict['dis_TEPO_cost']),
            ("sum((t, d)", "(ch_ini(d, t) gt 0)",
                           "dis_TEPO_SC(t, d)*" + cost_dict['SC_TEPO_cost']),
            ("sum((t, d)", "(dis_ini(d, t) gt 0)",
                           "ch_TEPO_SD(t, d)*" + cost_dict['SD_TEPO_cost']),
            ("sum((t, d)", "(dis_ini(d, t) gt 0)",
                           "ch_TEPO(t, d)*" + cost_dict['ch_TEPO_penalty']),
            ("sum((t, d)", "(ch_ini(d, t) gt 0)",
                           "dis_TEPO(t, d)*" + cost_dict['dis_TEPO_penalty'])
        ]

        for sum_elem in ess_sum_list:
            cost.rhs += 10*' ' + '+ ' + sum_elem[0]
            cost.rhs += '$' + '(t_ha(t) and ' + sum_elem[1] + '),\n'
            cost.rhs += (24 + 13*cost.hour_ahead)*' ' + sum_elem[2] + ')\n'

        cost.write_constraint(cf_list[0])

        # end HA_CF_Model

    # CF Model 2

    cost.rhs = cost_cf_rhs_stub

    cost_dict = {
        'ch_TEPO_cost': 'C_ch(d, t)',
        'dis_TEPO_cost': 'C_dis(d, t)',
        'SC_TEPO_cost': 'C_SC(d, t)',
        'SD_TEPO_cost': 'C_SD(d, t)',
        'ch_TEPO_penalty': 'P_ch(d, t)',
        'dis_TEPO_penalty': 'P_dis(d, t)'
    }

    ess_sum_list = [
        ("sum((t, d)", "(ch_ini(d, t) ge 0)",
                       "ch_TEPO(t, d)*" + cost_dict['ch_TEPO_cost']),
        ("sum((t, d)", "(dis_ini(d, t) ge 0)",
                       "dis_TEPO(t, d)*" + cost_dict['dis_TEPO_cost']),
        ("sum((t, d)", "(ch_ini(d, t) gt 0)",
                       "dis_TEPO_SC(t, d)*" + cost_dict['SC_TEPO_cost']),
        ("sum((t, d)", "(dis_ini(d, t) gt 0)",
                       "ch_TEPO_SD(t, d)*" + cost_dict['SD_TEPO_cost']),
        ("sum((t, d)", "(dis_ini(d, t) gt 0)",
                       "ch_TEPO(t, d)*" + cost_dict['ch_TEPO_penalty']),
        ("sum((t, d)", "(ch_ini(d, t) gt 0)",
                       "dis_TEPO(t, d)*" + cost_dict['dis_TEPO_penalty'])
    ]

    for sum_elem in ess_sum_list:
        cost.rhs += 10*' ' + '+ ' + sum_elem[0]

        if cost.hour_ahead:
            cost.rhs += '$' + '(t_ha(t) and ' + sum_elem[1] + '),\n'
        else:
            cost.rhs += '$' + sum_elem[1] + ',\n'

        cost.rhs += (24 + 13*cost.hour_ahead)*' ' + sum_elem[2] + ')\n'

    cost.rhs += 10*' ' + "+ sum((s, t)" + cost.hour_ahead*'$(t_ha(t))'
    cost.rhs += ", slack_pbal(s, t))*INFEASIBLE_PENALTY\n"

    cost.write_constraint(cf_list[1])

    # end write_cost_function


def write_bin_set10(file_list, hour_ahead):

    bin_set10 = optdef.Constraint()
    bin_set10.hour_ahead = hour_ahead
    bin_set10.name = 'bin_set10'
    bin_set10.comment = ("Binary logic for the first period of "
                         "the optimization horizon")
    bin_set10.domain = '(t, i)'

    bin_set10.domain_modifier = "(ord(t) eq "
    if hour_ahead:
        bin_set10.domain_modifier += "hour" + ')'
    else:
        bin_set10.domain_modifier += "1" + ')'

    bin_set10.lhs = 'y(t, i) - z(t, i)'
    bin_set10.rhs = 'v(t, i) - onoff_t0(i)'
    bin_set10.operator = 'e'

    for handle in file_list:
        bin_set10.write_constraint(handle)

    # end write_bin_set10


def write_bin_set1(file_list, hour_ahead):

    bin_set1 = optdef.Constraint()
    bin_set1.hour_ahead = hour_ahead
    bin_set1.name = 'bin_set1'
    bin_set1.comment = "Binary logic for all periods except the first"
    bin_set1.domain = '(t, i)'

    bin_set1.domain_modifier = "(ord(t) gt "
    if hour_ahead:
        bin_set1.domain_modifier += "hour" + ')'
    else:
        bin_set1.domain_modifier += "1" + ')'

    bin_set1.lhs = 'y(t, i) - z(t, i)'
    bin_set1.rhs = 'v(t, i) - v(t-1, i)'
    bin_set1.operator = 'e'

    for handle in file_list:
        bin_set1.write_constraint(handle)

    # end write_bin_set1


def write_bin_set2(file_list, hour_ahead):

    bin_set2 = optdef.Constraint()
    bin_set2.hour_ahead = hour_ahead
    bin_set2.name = 'bin_set2'
    bin_set2.comment = "Prevent simultaneous start-up and shutdown"
    bin_set2.domain = '(t, i)'
    bin_set2.lhs = 'y(t, i) + z(t, i)'
    bin_set2.rhs = '1'
    bin_set2.operator = 'l'

    for handle in file_list:
        bin_set2.write_constraint(handle)

    # end write_bin_set2


def write_gen_sum(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    gen_sum = optdef.Constraint()
    gen_sum.hour_ahead = hour_ahead
    gen_sum.name = 'gen_sum'
    gen_sum.comment = "Total power output as the sum of the blocks"
    gen_sum.domain = '(t, i)'
    gen_sum.lhs = 'g(t, i)'
    gen_sum.rhs = 'sum(b, g_lin(t, i, b))'
    gen_sum.operator = 'e'

    # Definition for UC models

    for uc_handle in uc_list:
        gen_sum.write_constraint(uc_handle)

    gen_sum.lhs = ("gbis(t, i)\n"
                   "      + deltag_plus(t, i)\n"
                   "      - deltag_minus(t, i)")

    gen_sum.rhs = "sum(b, glin_bis(t, i, b)\n"
    gen_sum.rhs += 36*' ' + "+ deltag_lin_plus(t, i, b)\n"
    gen_sum.rhs += 36*' ' + "- deltag_lin_minus(t, i, b))"

    # Definition for CF models

    for cf_handle in cf_list:
        gen_sum.write_constraint(cf_handle)

    # end write_gen_sum


def write_gen_min(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    gen_min = optdef.Constraint()
    gen_min.hour_ahead = hour_ahead
    gen_min.name = 'gen_min'
    gen_min.comment = ("Minimum bound for the power output of "
                       "conventional thermal units")
    gen_min.domain = '(t, i)'
    gen_min.lhs = 'g(t, i)'
    gen_min.rhs = 'g_min(i)*v(t, i)'
    gen_min.operator = 'g'

    # Definition for UC models

    for uc_handle in uc_list:
        gen_min.write_constraint(uc_handle)

    # Definition for CF models

    gen_min.lhs = ("gbis(t, i)\n"
                   "      + deltag_plus(t, i)\n"
                   "      - deltag_minus(t, i)")

    for cf_handle in cf_list:
        gen_min.write_constraint(cf_handle)

    # end write_gen_min


def write_block_output(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    block_output = optdef.Constraint()
    block_output.hour_ahead = hour_ahead
    block_output.name = 'block_output'
    block_output.comment = ("Maximum bounds for the power output "
                            "of each block")
    block_output.domain = '(t, i, b)'
    block_output.lhs = 'g_lin(t, i, b)'
    block_output.rhs = "g_max(i, b)*v(t, i)"
    block_output.operator = 'l'

    # Definition for UC models

    for uc_handle in uc_list:
        block_output.write_constraint(uc_handle)

    block_output.lhs = ("glin_bis(t, i, b)\n"
                        "      + deltag_lin_plus(t, i, b)\n"
                        "      - deltag_lin_minus(t, i, b)")

    # Definition for CF models

    for cf_handle in cf_list:
        block_output.write_constraint(cf_handle)

    # end write_block_output


def write_min_updown_1(file_list, hour_ahead):

    min_updown_1 = optdef.Constraint()
    min_updown_1.hour_ahead = hour_ahead
    min_updown_1.name = 'min_updown_1'
    min_updown_1.comment = ("Initial conditions for the minimum "
                            "up and down time constraints")
    min_updown_1.domain = '(t, i)'
    min_updown_1.domain_modifier = "((L_up_min(i) + L_down_min(i) gt 0)\n"
    min_updown_1.domain_modifier += 8*' ' + 'and '
    min_updown_1.domain_modifier += "(ord(t) le L_up_min(i) + L_down_min(i)))"
    min_updown_1.lhs = 8*' ' + 'v(t, i)'
    min_updown_1.rhs = 'onoff_t0(i)'
    min_updown_1.operator = 'e'

    for handle in file_list:
        min_updown_1.write_constraint(handle)

    # end write_min_updown_1


def write_min_updown_2(file_list, hour_ahead):

    min_updown_2 = optdef.Constraint()
    min_updown_2.hour_ahead = hour_ahead
    min_updown_2.name = 'min_updown_2'
    min_updown_2.comment = ("Minimum up time constraints "
                            "for the rest of the periods")
    min_updown_2.domain = '(t, i)'
    min_updown_2.domain_modifier = '(ord(t) gt L_up_min(i))'
    min_updown_2.lhs = "sum(tt$((ord(tt) ge ord(t) - g_up(i) + 1)\n"
    min_updown_2.lhs += 16*' ' + "and (ord(tt) le ord(t))), y(tt, i))"
    min_updown_2.rhs = 'v(t, i)'
    min_updown_2.operator = 'l'

    for handle in file_list:
        min_updown_2.write_constraint(handle)

    # end write_min_updown_2


def write_min_updown_3(file_list, hour_ahead):

    min_updown_3 = optdef.Constraint()
    min_updown_3.hour_ahead = hour_ahead
    min_updown_3.name = 'min_updown_3'
    min_updown_3.comment = ("Minimum down time constraints "
                            "for the rest of the periods")
    min_updown_3.domain = '(t, i)'
    min_updown_3.domain_modifier = '(ord(t) gt L_down_min(i))'
    min_updown_3.lhs = "sum(tt$((ord(tt) ge ord(t) - g_down(i) + 1)\n"
    min_updown_3.lhs += 16*' ' + "and (ord(tt) le ord(t))), z(tt, i))"
    min_updown_3.rhs = '1 - v(t, i)'
    min_updown_3.operator = 'l'

    for handle in file_list:
        min_updown_3.write_constraint(handle)

    # end write min_updown_3


def write_ramp_limit_min_1(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    ramp_limit_min_1 = optdef.Constraint()
    ramp_limit_min_1.hour_ahead = hour_ahead
    ramp_limit_min_1.name = 'ramp_limit_min_1'
    ramp_limit_min_1.comment = "Ramp down constraints for the initial period"
    ramp_limit_min_1.domain = '(t, i)'

    ramp_limit_min_1.domain_modifier = "(ord(t) eq "
    if hour_ahead:
        ramp_limit_min_1.domain_modifier += "hour" + ')'
    else:
        ramp_limit_min_1.domain_modifier += "1" + ')'

    ramp_limit_min_1.lhs = '-ramp_down(i)'
    ramp_limit_min_1.rhs = "g(t, i) - g_0(i)"
    ramp_limit_min_1.operator = 'l'

    for uc_handle in uc_list:
        ramp_limit_min_1.write_constraint(uc_handle)

    ramp_limit_min_1.rhs = "(gbis(t, i)\n"
    ramp_limit_min_1.rhs += 25*' ' + "+ deltag_plus(t, i)\n"
    ramp_limit_min_1.rhs += 25*' ' + "- deltag_minus(t, i)) - g_0(i)"

    for cf_handle in cf_list:
        ramp_limit_min_1.write_constraint(cf_handle)

    # end write_ramp_limit_min_1


def write_ramp_limit_min(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    ramp_limit_min = optdef.Constraint()
    ramp_limit_min.hour_ahead = hour_ahead
    ramp_limit_min.name = 'ramp_limit_min'
    ramp_limit_min.comment = ("Ramp down constraints for "
                              "all periods except the first")
    ramp_limit_min.domain = '(t, i)'

    ramp_limit_min.domain_modifier = "(ord(t) gt "
    if hour_ahead:
        ramp_limit_min.domain_modifier += "hour" + ')'
    else:
        ramp_limit_min.domain_modifier += "1" + ')'

    ramp_limit_min.lhs = '-ramp_down(i)'
    ramp_limit_min.rhs = 'g(t, i) - g(t-1, i)'
    ramp_limit_min.operator = 'l'

    # Definition for UC models

    for uc_handle in uc_list:
        ramp_limit_min.write_constraint(uc_handle)

    ramp_limit_min.rhs = '(gbis(t, i)\n'
    ramp_limit_min.rhs += 25*' ' + '+ deltag_plus(t, i)\n'
    ramp_limit_min.rhs += 25*' ' + '- deltag_minus(t, i)) - (gbis(t-1, i)\n'
    ramp_limit_min.rhs += 48*' ' + '+ deltag_plus(t-1, i)\n'
    ramp_limit_min.rhs += 48*' ' + '- deltag_minus(t-1, i))'

    # Definition for CF models

    for cf_handle in cf_list:
        ramp_limit_min.write_constraint(cf_handle)

    # end ramp_limit_min


def write_ramp_limit_max_1(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    ramp_limit_max_1 = optdef.Constraint()
    ramp_limit_max_1.hour_ahead = hour_ahead
    ramp_limit_max_1.name = 'ramp_limit_max_1'
    ramp_limit_max_1.comment = "Ramp up constraints for the initial period"
    ramp_limit_max_1.domain = '(t, i)'

    ramp_limit_max_1.domain_modifier = "(ord(t) eq "
    if hour_ahead:
        ramp_limit_max_1.domain_modifier += "hour" + ')'
    else:
        ramp_limit_max_1.domain_modifier += "1" + ')'

    ramp_limit_max_1.lhs = 'ramp_up(i)'
    ramp_limit_max_1.rhs = "g(t, i) - g_0(i)"
    ramp_limit_max_1.operator = 'g'

    for uc_handle in uc_list:
        ramp_limit_max_1.write_constraint(uc_handle)

    ramp_limit_max_1.rhs = "(gbis(t, i)\n"
    ramp_limit_max_1.rhs += 22*' ' + "+ deltag_plus(t, i)\n"
    ramp_limit_max_1.rhs += 22*' ' + "- deltag_minus(t, i)) - g_0(i)"

    for cf_handle in cf_list:
        ramp_limit_max_1.write_constraint(cf_handle)

    # end write_ramp_limit_max_1


def write_ramp_limit_max(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    ramp_limit_max = optdef.Constraint()
    ramp_limit_max.hour_ahead = hour_ahead
    ramp_limit_max.name = 'ramp_limit_max'
    ramp_limit_max.comment = ("Ramp up constraints for "
                              "all periods except the first")
    ramp_limit_max.domain = '(t, i)'

    ramp_limit_max.domain_modifier = "(ord(t) gt "
    if hour_ahead:
        ramp_limit_max.domain_modifier += "hour" + ')'
    else:
        ramp_limit_max.domain_modifier += "1" + ')'

    ramp_limit_max.lhs = 'ramp_up(i)'
    ramp_limit_max.rhs = 'g(t, i) - g(t-1, i)'
    ramp_limit_max.operator = 'g'

    # Definition for UC models

    for uc_handle in uc_list:
        ramp_limit_max.write_constraint(uc_handle)

    ramp_limit_max.rhs = '(gbis(t, i)\n'
    ramp_limit_max.rhs += 22*' ' + '+ deltag_plus(t, i)\n'
    ramp_limit_max.rhs += 22*' ' + '- deltag_minus(t, i)) - (gbis(t-1, i)\n'
    ramp_limit_max.rhs += 45*' ' + '+ deltag_plus(t-1, i)\n'
    ramp_limit_max.rhs += 45*' ' + '- deltag_minus(t-1, i))'

    # Definition for CF models

    for cf_handle in cf_list:
        ramp_limit_max.write_constraint(cf_handle)

    # end ramp_limit_max


def write_power_balance(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    power_balance = optdef.Constraint()
    power_balance.hour_ahead = hour_ahead
    power_balance.num_indent = 4
    power_balance.name = 'power_balance'
    power_balance.comment = "Nodal power balance equations"
    power_balance.domain = '(t, s)'
    power_balance.lhs = 'demand(s, t)'

    if hour_ahead:
        power_balance.lhs += (
            "\n        + sum(d$(storage_map(d) eq ord(s)),\n"
            "                 ch_day(d, t) - dis_day(d, t))"
        )

    power_balance.rhs = \
        ("\n          sum(i$(gen_map(i) eq ord(s)), g(t, i))\n"
         "        + sum(f$(fix_map(f) eq ord(s)), fix_deterministic(f, t)\n"
         "                                      - slack_fixed(f, t))\n"
         "        + sum(r$(sol_map(r) eq ord(s)), sol_deterministic(t, r)\n"
         "                                      - slack_solar(r, t))\n"
         "        + sum(w$(win_map(w) eq ord(s)), wind_deterministic(t, w)\n"
         "                                      - slack_wind(w, t))\n"
         "        - sum(l$(line_map(l, 'from') eq ord(s)), pf(t, l))\n"
         "        + sum(l$(line_map(l, 'to') eq ord(s)), pf(t, l))\n")
    power_balance.operator = 'e'

    power_balance.write_constraint(uc_list[0])

    power_balance.lhs = (
        "demand(s, t) - slack_pbal(s, t)\n"
        "        + sum(d$(storage_map(d) eq ord(s)), p_ext2(d, t))"
    )

    power_balance.write_constraint(uc_list[1])

    power_balance.lhs = (
        "demand(s, t)\n"
        "        + sum(d$(storage_map(d) eq ord(s)),\n"
        "                 ch_total(t, d) - dis_total(t, d))"
    )

    power_balance.rhs = \
        ("\n          sum(i$(gen_map(i) eq ord(s)), gbis(t, i)\n"
         "                                      + deltag_plus(t, i)\n"
         "                                      - deltag_minus(t, i))\n"
         "        + sum(f$(fix_map(f) eq ord(s)), fix_deterministic(f, t)\n"
         "                                      - slack_fixed_bis(f, t)\n"
         "                                      - slack_fixed_plus(t, f)\n"
         "                                      + slack_fixed_minus(t, f))\n"
         "        + sum(r$(sol_map(r) eq ord(s)), sol_deterministic(t, r)\n"
         "                                      - slack_solar_bis(r, t)\n"
         "                                      - slack_solar_plus(t, r)\n"
         "                                      + slack_solar_minus(t, r))\n"
         "        + sum(w$(win_map(w) eq ord(s)), wind_deterministic(t, w)\n"
         "                                      - slack_wind_bis(w, t)\n"
         "                                      - slack_wind_plus(t, w)\n"
         "                                      + slack_wind_minus(t, w))\n"
         "        - sum(l$(line_map(l, 'from') eq ord(s)), pf(t, l))\n"
         "        + sum(l$(line_map(l, 'to') eq ord(s)), pf(t, l))\n")

    power_balance.write_constraint(cf_list[0])

    power_balance.lhs = (
        "demand(s, t) - slack_pbal(s, t)\n"
        "        + sum(d$(storage_map(d) eq ord(s)),\n"
        "                 ch_total(t, d) - dis_total(t, d))"
    )

    power_balance.write_constraint(cf_list[1])

    # end write_power_balance


def write_line_flow(file_list, hour_ahead):

    line_flow = optdef.Constraint()
    line_flow.hour_ahead = hour_ahead
    line_flow.name = 'line_flow'
    line_flow.comment = ("Definition of the line flows "
                         "in terms of the voltage phase angles")
    line_flow.domain = '(t, l)'
    line_flow.lhs = 'pf(t, l)'
    line_flow.rhs = "(sum(s$(line_map(l, 'from') eq ord(s)), theta(t, s))\n"
    line_flow.rhs += 20*' '
    line_flow.rhs += "- sum(s$(line_map(l, 'to') eq ord(s)), theta(t, s)))\n"
    line_flow.rhs += 20*' ' + "* admittance(l)"
    line_flow.operator = 'e'

    for handle in file_list:
        line_flow.write_constraint(handle)

    # end write_line_flow


def write_line_capacity_min(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    line_capacity_min = optdef.Constraint()
    line_capacity_min.hour_ahead = hour_ahead
    line_capacity_min.comment = "NO LINE FLOW LIMITS IN UC STAGE 1\n"

    line_capacity_min.write_comment(uc_list[0])

    line_capacity_min.name = 'line_capacity_min'
    line_capacity_min.comment = "Transmission capacity constraint"
    line_capacity_min.domain = '(t, l)'
    line_capacity_min.lhs = 'pf(t, l)'
    line_capacity_min.rhs = '-l_max(l)'
    line_capacity_min.operator = 'g'

    for cf_handle in cf_list:
        line_capacity_min.write_constraint(cf_handle)

    line_capacity_min.rhs += ' - slack_flow(l, t)'

    line_capacity_min.write_constraint(uc_list[1])

    # end write_line_capacity_min


def write_line_capacity_max(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    line_capacity_max = optdef.Constraint()
    line_capacity_max.hour_ahead = hour_ahead
    line_capacity_max.name = 'line_capacity_max'
    line_capacity_max.comment = "Transmission capacity constraint"
    line_capacity_max.domain = '(t, l)'
    line_capacity_max.lhs = 'pf(t, l)'
    line_capacity_max.rhs = 'l_max(l)'
    line_capacity_max.operator = 'l'

    for cf_handle in cf_list:
        line_capacity_max.write_constraint(cf_handle)

    line_capacity_max.rhs += ' + slack_flow(l, t)'

    line_capacity_max.write_constraint(uc_list[1])

    # end write_line_capacity_max


def write_voltage_angles_min(file_list, hour_ahead):

    voltage_angles_min = optdef.Constraint()
    voltage_angles_min.hour_ahead = hour_ahead
    voltage_angles_min.name = 'voltage_angles_min'
    voltage_angles_min.comment = "Minimum voltage phase angle limits"
    voltage_angles_min.domain = '(t, s)'
    voltage_angles_min.lhs = 'theta(t, s)'
    voltage_angles_min.rhs = '-pi'
    voltage_angles_min.operator = 'g'

    for handle in file_list:
        voltage_angles_min.write_constraint(handle)

    # end write_voltage_angles_min


def write_voltage_angles_max(file_list, hour_ahead):

    voltage_angles_max = optdef.Constraint()
    voltage_angles_max.hour_ahead = hour_ahead
    voltage_angles_max.name = 'voltage_angles_max'
    voltage_angles_max.comment = "Maximum voltage phase angle limits"
    voltage_angles_max.domain = '(t, s)'
    voltage_angles_max.lhs = 'theta(t, s)'
    voltage_angles_max.rhs = 'pi'
    voltage_angles_max.operator = 'l'

    for handle in file_list:
        voltage_angles_max.write_constraint(handle)

    # end write_voltage_angles_max


def write_slack_solar(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    slack_solar = optdef.Constraint()
    slack_solar.hour_ahead = hour_ahead
    slack_solar.name = 'slack_solar_constr'
    slack_solar.comment = "Maximum spillage for solar generation"
    slack_solar.domain = "(t, r)"
    slack_solar.lhs = "sol_deterministic(t, r)"
    slack_solar.rhs = "slack_solar(r, t)"
    slack_solar.operator = 'g'

    for uc_handle in uc_list:
        slack_solar.write_constraint(uc_handle)

    slack_solar.rhs = "slack_solar_bis(r, t)\n"
    slack_solar.rhs += 34*' ' + "+ slack_solar_plus(t, r)\n"
    slack_solar.rhs += 34*' ' + "- slack_solar_minus(t, r)"

    slack_solar_min = optdef.Constraint()
    slack_solar_min.hour_ahead = hour_ahead
    slack_solar_min.name = 'slack_solar_constr2'
    slack_solar_min.comment = "Minimum spillage for solar generation"
    slack_solar_min.domain = "(t, r)"
    slack_solar_min.lhs = '0'
    slack_solar_min.operator = 'l'

    slack_solar_min.rhs = "slack_solar_bis(r, t)\n"
    slack_solar_min.rhs += 12*' ' + "+ slack_solar_plus(t, r)\n"
    slack_solar_min.rhs += 12*' ' + "- slack_solar_minus(t, r)"

    for cf_handle in cf_list:
        slack_solar.write_constraint(cf_handle)
        slack_solar_min.write_constraint(cf_handle)

    # end write_slack_solar


def write_slack_wind(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    slack_wind = optdef.Constraint()
    slack_wind.hour_ahead = hour_ahead
    slack_wind.name = 'slack_wind_constr'
    slack_wind.comment = "Maximum spillage for wind generation"
    slack_wind.domain = '(t, w)'
    slack_wind.lhs = 'wind_deterministic(t, w)'
    slack_wind.rhs = 'slack_wind(w, t)'
    slack_wind.operator = 'g'

    for uc_handle in uc_list:
        slack_wind.write_constraint(uc_handle)

    slack_wind.rhs = "slack_wind_bis(w, t)\n"
    slack_wind.rhs += 35*' ' + "+ slack_wind_plus(t, w)\n"
    slack_wind.rhs += 35*' ' + "- slack_wind_minus(t, w)"

    slack_wind_min = optdef.Constraint()
    slack_wind_min.hour_ahead = hour_ahead
    slack_wind_min.name = 'slack_wind_constr2'
    slack_wind_min.comment = "Minimum spillage for wind generation"
    slack_wind_min.domain = '(t, w)'
    slack_wind_min.lhs = '0'
    slack_wind_min.operator = 'l'

    slack_wind_min.rhs = "slack_wind_bis(w, t)\n"
    slack_wind_min.rhs += 12*' ' + "+ slack_wind_plus(t, w)\n"
    slack_wind_min.rhs += 12*' ' + "- slack_wind_minus(t, w)"

    for cf_handle in cf_list:
        slack_wind.write_constraint(cf_handle)
        slack_wind_min.write_constraint(cf_handle)

    # end write_slack_wind


def write_slack_fixed(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    slack_fixed = optdef.Constraint()
    slack_fixed.hour_ahead = hour_ahead
    slack_fixed.name = 'slack_fixed_constr'
    slack_fixed.comment = "Maximum spillage for fixed resources"
    slack_fixed.domain = '(t, f)'
    slack_fixed.lhs = "fix_deterministic(f, t)"
    slack_fixed.rhs = "slack_fixed(f, t)"
    slack_fixed.operator = 'g'

    for uc_handle in uc_list:
        slack_fixed.write_constraint(uc_handle)

    slack_fixed.rhs = "slack_fixed_bis(f, t)\n"
    slack_fixed.rhs += 34*' ' + "+ slack_fixed_plus(t, f)\n"
    slack_fixed.rhs += 34*' ' + "- slack_fixed_minus(t, f)"

    slack_fixed_min = optdef.Constraint()
    slack_fixed_min.hour_ahead = hour_ahead
    slack_fixed_min.name = 'slack_fixed_constr2'
    slack_fixed_min.comment = "Minimum spillage for fixed resources"
    slack_fixed_min.domain = '(t, f)'
    slack_fixed_min.lhs = '0'
    slack_fixed_min.operator = 'l'

    slack_fixed_min.rhs = "slack_fixed_bis(f, t)\n"
    slack_fixed_min.rhs += 12*' ' + "+ slack_fixed_plus(t, f)\n"
    slack_fixed_min.rhs += 12*' ' + "- slack_fixed_minus(t, f)"

    for cf_handle in cf_list:
        slack_fixed.write_constraint(cf_handle)
        slack_fixed_min.write_constraint(cf_handle)

    # end write_slack_fixed


def write_eq_ch_total(file_list, hour_ahead):

    cf_list = file_list[1:3]

    eq_ch_total = optdef.Constraint()
    eq_ch_total.hour_ahead = hour_ahead
    eq_ch_total.name = 'eq_ch_total'
    eq_ch_total.comment = "Energy storage total charge calculation"
    eq_ch_total.domain = '(t, d)'
    eq_ch_total.lhs = "ch_total(t, d)"
    eq_ch_total.rhs = "ch_ini(d, t) + ch_TEPO(t, d) - dis_TEPO_SC(t, d)"
    eq_ch_total.operator = 'e'

    for cf_handle in cf_list:
        eq_ch_total.write_constraint(cf_handle)

    # end write_eq_ch_total


def write_eq_dis_total(file_list, hour_ahead):

    cf_list = file_list[1:3]

    eq_dis_total = optdef.Constraint()
    eq_dis_total.hour_ahead = hour_ahead
    eq_dis_total.name = 'eq_dis_total'
    eq_dis_total.comment = "Energy storage total discharge calculation"
    eq_dis_total.domain = '(t, d)'
    eq_dis_total.lhs = "dis_total(t, d)"
    eq_dis_total.rhs = "dis_ini(d, t) + dis_TEPO(t, d) - ch_TEPO_SD(t, d)"
    eq_dis_total.operator = 'e'

    for cf_handle in cf_list:
        eq_dis_total.write_constraint(cf_handle)

    # end write_eq_dis_total


def write_ch_total_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    ch_total_limit = optdef.Constraint()
    ch_total_limit.hour_ahead = hour_ahead
    ch_total_limit.name = 'ch_total_limit'
    ch_total_limit.comment = "Energy storage charging limit"
    ch_total_limit.domain = '(t, d)'
    ch_total_limit.lhs = "ch_total(t, d)"
    ch_total_limit.rhs = "ES_power_max(d)*v_ch(t, d)"
    ch_total_limit.operator = 'l'

    for cf_handle in cf_list:
        ch_total_limit.write_constraint(cf_handle)

    # end write_ch_total_limit


def write_dis_total_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    dis_total_limit = optdef.Constraint()
    dis_total_limit.hour_ahead = hour_ahead
    dis_total_limit.name = 'dis_total_limit'
    dis_total_limit.comment = "Energy storage discharging limit"
    dis_total_limit.domain = '(t, d)'
    dis_total_limit.lhs = "dis_total(t, d)"
    dis_total_limit.rhs = "ES_power_max(d)*(1 - v_ch(t, d))"
    dis_total_limit.operator = 'l'

    for cf_handle in cf_list:
        dis_total_limit.write_constraint(cf_handle)

    # end write_dis_total_limit


def write_ch_TEPO_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    ch_TEPO_limit = optdef.Constraint()
    ch_TEPO_limit.hour_ahead = hour_ahead
    ch_TEPO_limit.name = 'ch_TEPO_limit'
    ch_TEPO_limit.comment = "TEPO charging limit"
    ch_TEPO_limit.domain = '(t, d)'
    ch_TEPO_limit.lhs = "ch_TEPO(t, d)"
    ch_TEPO_limit.rhs = "Bound_ch(t, d)*y_ch(t, d)"
    ch_TEPO_limit.operator = 'l'

    for cf_handle in cf_list:
        ch_TEPO_limit.write_constraint(cf_handle)

    # end write_ch_TEPO_limit


def write_dis_SC_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    dis_SC_limit = optdef.Constraint()
    dis_SC_limit.hour_ahead = hour_ahead
    dis_SC_limit.name = 'dis_SC_limit'
    dis_SC_limit.comment = "TEPO stop charging limit"
    dis_SC_limit.domain = '(t, d)'
    dis_SC_limit.lhs = "dis_TEPO_SC(t, d)"
    dis_SC_limit.rhs = "Bound_SC(t, d)*(1 - y_ch(t, d))"
    dis_SC_limit.operator = 'l'

    for cf_handle in cf_list:
        dis_SC_limit.write_constraint(cf_handle)

    # end write_dis_SC_limit


def write_dis_TEPO_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    dis_TEPO_limit = optdef.Constraint()
    dis_TEPO_limit.hour_ahead = hour_ahead
    dis_TEPO_limit.name = 'dis_TEPO_limit'
    dis_TEPO_limit.comment = "TEPO discharging limit"
    dis_TEPO_limit.domain = '(t, d)'
    dis_TEPO_limit.lhs = "dis_TEPO(t, d)"
    dis_TEPO_limit.rhs = "Bound_dis(t, d)*z_ch(t, d)"
    dis_TEPO_limit.operator = 'l'

    for cf_handle in cf_list:
        dis_TEPO_limit.write_constraint(cf_handle)

    # end write_dis_TEPO_limit


def write_ch_SD_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    ch_SD_limit = optdef.Constraint()
    ch_SD_limit.hour_ahead = hour_ahead
    ch_SD_limit.name = 'ch_SD_limit'
    ch_SD_limit.comment = "TEPO stop discharging limit"
    ch_SD_limit.domain = '(t, d)'
    ch_SD_limit.lhs = "ch_TEPO_SD(t, d)"
    ch_SD_limit.rhs = "Bound_SD(t, d)*(1 - z_ch(t, d))"
    ch_SD_limit.operator = 'l'

    for cf_handle in cf_list:
        ch_SD_limit.write_constraint(cf_handle)

    # end write_ch_SD_limit


def write_eq_storage_init(file_list, hour_ahead):

    uc_list = file_list[0:4:3]
    cf_list = file_list[1:3]

    eq_storage_init = optdef.Constraint()
    eq_storage_init.hour_ahead = hour_ahead
    eq_storage_init.comment = "NO ENERGY STORAGE CONSTRAINTS IN UC STAGES\n"

    for uc_handle in uc_list:
        eq_storage_init.write_comment(uc_handle)

    eq_storage_init.name = 'eq_storage_init'
    eq_storage_init.comment = ("Initial energy storage "
                               "state of charge trajectory")
    eq_storage_init.domain = '(t, d)'
    eq_storage_init.domain_modifier = '(ord(t) eq 1)'
    eq_storage_init.lhs = "soc(t, d)"
    eq_storage_init.rhs = "E_initial(d) + ch_total(t, d)*alef_ch(d)\n"
    eq_storage_init.rhs += 35*' ' + "- dis_total(t, d)/alef_dis(d)"
    eq_storage_init.operator = 'e'

    for cf_handle in cf_list:
        eq_storage_init.write_constraint(cf_handle)

    # end write_eq_storage_init


def write_eq_storage(file_list, hour_ahead):

    cf_list = file_list[1:3]

    eq_storage = optdef.Constraint()
    eq_storage.hour_ahead = hour_ahead
    eq_storage.name = 'eq_storage'
    eq_storage.comment = ("Energy storage state of charge "
                          "trajectory in periods greater than 1")
    eq_storage.domain = '(t, d)'
    eq_storage.domain_modifier = '(ord(t) gt 1)'
    eq_storage.lhs = "soc(t, d)"
    eq_storage.rhs = "soc(t-1, d) + ch_total(t, d)*alef_ch(d)\n"
    eq_storage.rhs += 34*' ' + "- dis_total(t, d)/alef_dis(d)"
    eq_storage.operator = 'e'

    for cf_handle in cf_list:
        eq_storage.write_constraint(cf_handle)

    # end write_eq_storage


def write_soc_limit(file_list, hour_ahead):

    cf_list = file_list[1:3]

    soc_limit = optdef.Constraint()
    soc_limit.hour_ahead = hour_ahead
    soc_limit.name = 'soc_limit'
    soc_limit.comment = "Energy storage state of charge limit"
    soc_limit.domain = '(t, d)'
    soc_limit.lhs = "soc(t, d)"
    soc_limit.rhs = "Emax(d)"
    soc_limit.operator = 'l'

    for cf_handle in cf_list:
        soc_limit.write_constraint(cf_handle)

    # end write_soc_limit


def write_eq_soc_final(file_list, hour_ahead):

    cf_list = file_list[1:3]

    eq_soc_final = optdef.Constraint()
    eq_soc_final.hour_ahead = hour_ahead
    eq_soc_final.name = 'eq_soc_final'
    eq_soc_final.comment = "Final enery storage state of charge"
    eq_soc_final.domain = '(t, d)'
    eq_soc_final.domain_modifier = "(ord(t) eq card(t))"
    eq_soc_final.lhs = 'soc(t, d)'
    eq_soc_final.rhs = 'E_final(d)'
    eq_soc_final.operator = 'e'

    for cf_handle in cf_list:
        eq_soc_final.write_constraint(cf_handle)

    # end write_eq_soc_final
