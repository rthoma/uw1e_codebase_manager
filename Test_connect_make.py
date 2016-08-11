import sys
import os
sys.path.append(os.getcwd())
import infun
import headfun
import optfun
import footfun

hour_ahead = False
read_flag = False
read_subdir = 'Data\\'

uc1_str = 'UC_model'
cf1_str = 'CF_model'
cf2_str = 'CF_model2'
uc2_str = 'UC_model2'

if hour_ahead:
    uc1_str = 'a_HA_' + uc1_str + '_4hour_TH.gms'
    cf1_str = 'a_HA_' + cf1_str + '_4hour_TH.gms'
    cf2_str = 'a_HA_' + cf2_str + '_4hour_TH.gms'
    uc2_str = 'a_HA_' + uc2_str + '_4hour_TH.gms'
else:
    uc1_str = 'a_DA_' + uc1_str + '.gms'
    cf1_str = 'a_DA_' + cf1_str + '.gms'
    cf2_str = 'a_DA_' + cf2_str + '.gms'
    uc2_str = 'a_DA_' + uc2_str + '.gms'

uc1 = open(uc1_str, 'w')
cf1 = open(cf1_str, 'w')
cf2 = open(cf2_str, 'w')
uc2 = open(uc2_str, 'w')

file_list = [uc1, cf1, cf2, uc2]

day_path = 'C:\\BPA_project\\Test_connect_DA_auto\\'
hour_path = 'C:\\BPA_project\\Test_connect_HA_ok\\'

data_subdir_ext = 'Data\\'
depo_subdir_ext = 'DEPO\\'

if hour_ahead:
    base_path = hour_path
else:
    base_path = day_path

path_dict = {
    'base_path': base_path,
    'data_path': base_path + data_subdir_ext,
    'depo_path': base_path + depo_subdir_ext,
    'day_path' : day_path,
    'day_data_path': day_path + data_subdir_ext,
    'day_depo_path': day_path + depo_subdir_ext,
    'hour_path': hour_path,
    'hour_data_path': hour_path + data_subdir_ext,
    'hour_depo_path': hour_path + depo_subdir_ext,
}

input_file = open('a_input_data' + hour_ahead*'_4hour_TH' + '.gms', 'w')

input_spec = {
    'read_flag': read_flag,
    'read_subdir': read_subdir,
    'data_path': path_dict['data_path'],
    'bpa_sys_file': 'Input_Data_WECC2024_BPA_Apr13.xlsx',
    'fixed_data_file': 'BPA_fixed_load_Apr13.xlsx',
    'ess_data_file': 'ES_data.xlsx'
}

num_demand_groups = 0

for handle in file_list:
    handle.write('** ' + handle.name + '\n\n')
#    handle.write("** ;; Local variables:\n")
#    handle.write("** ;; mode: gams\n")
#    handle.write("** ;; eval: (delete-trailing-whitespace)\n")
#    handle.write("** ;; End:\n\n")

###############################################################################
# Input data file                                                             #
###############################################################################

infun.input_sets(input_file, hour_ahead)
infun.input_generator_data(input_file, hour_ahead, input_spec)
infun.input_line_data(input_file, hour_ahead, input_spec)
infun.input_demand_data(input_file, hour_ahead, input_spec, num_demand_groups)
infun.input_wind_data(input_file, hour_ahead, input_spec)
infun.input_solar_data(input_file, hour_ahead, input_spec)
infun.input_fixed_data(input_file, hour_ahead, input_spec)
infun.input_scalars(input_file, hour_ahead, input_spec, path_dict)
infun.input_parameters(input_file, hour_ahead)
infun.input_storage_data(input_file, hour_ahead, input_spec, path_dict)
infun.input_initial_conditions(input_file, hour_ahead, input_spec, path_dict)
infun.input_time_horizon_logic(input_file, hour_ahead)

###############################################################################
# Header                                                                      #
###############################################################################

headfun.head_options(file_list, hour_ahead)
headfun.head_inputs(file_list, hour_ahead, path_dict)
headfun.head_bounds(file_list, hour_ahead, path_dict)
headfun.head_variables(file_list, hour_ahead)
headfun.head_positive_variables(file_list, hour_ahead)
headfun.head_binary_variables(file_list, hour_ahead)
headfun.head_equations(file_list, hour_ahead)
headfun.head_aliases(file_list, hour_ahead)

###############################################################################
# Constraints                                                                 #
###############################################################################

# Objective function
optfun.write_cost_function(file_list, hour_ahead)

# --------------------------------------------------------------------------- #
# Generation constraints

# Binary constraints
optfun.write_bin_set10(file_list, hour_ahead)
optfun.write_bin_set1(file_list, hour_ahead)
optfun.write_bin_set2(file_list, hour_ahead)

# Minimum up and down time constraints
optfun.write_min_updown_1(file_list, hour_ahead)
optfun.write_min_updown_2(file_list, hour_ahead)
optfun.write_min_updown_3(file_list, hour_ahead)

# Generation constraints for each block
optfun.write_gen_sum(file_list, hour_ahead)
optfun.write_gen_min(file_list, hour_ahead)
optfun.write_block_output(file_list, hour_ahead)

# Ramp rate limit constraints
optfun.write_ramp_limit_min_1(file_list, hour_ahead)
optfun.write_ramp_limit_min(file_list, hour_ahead)
optfun.write_ramp_limit_max_1(file_list, hour_ahead)
optfun.write_ramp_limit_max(file_list, hour_ahead)

# --------------------------------------------------------------------------- #
# Nodal power balance and transmission constraints

# Nodal power balance constraint and line flow calculation
optfun.write_power_balance(file_list, hour_ahead)
optfun.write_line_flow(file_list, hour_ahead)

# Voltage angle bounds and line flow limits
optfun.write_voltage_angles_min(file_list, hour_ahead)
optfun.write_voltage_angles_max(file_list, hour_ahead)
optfun.write_line_capacity_min(file_list, hour_ahead)
optfun.write_line_capacity_max(file_list, hour_ahead)

# Generation slack constraints
optfun.write_slack_solar(file_list, hour_ahead)
optfun.write_slack_wind(file_list, hour_ahead)
optfun.write_slack_fixed(file_list, hour_ahead)

# --------------------------------------------------------------------------- #
# Energy storage model constraints

# Maximum charge and discharge constraints
optfun.write_eq_ch_total(file_list, hour_ahead)
optfun.write_eq_dis_total(file_list, hour_ahead)
optfun.write_ch_total_limit(file_list, hour_ahead)
optfun.write_dis_total_limit(file_list, hour_ahead)

# CF Model 2, Stage 3
optfun.write_ch_SD_limit(file_list, hour_ahead)
optfun.write_dis_SC_limit(file_list, hour_ahead)
optfun.write_ch_TEPO_limit(file_list, hour_ahead)
optfun.write_dis_TEPO_limit(file_list, hour_ahead)

# State of charge constraints
optfun.write_eq_storage_init(file_list, hour_ahead)
optfun.write_eq_storage(file_list, hour_ahead)
optfun.write_soc_limit(file_list, hour_ahead)
optfun.write_eq_soc_final(file_list, hour_ahead)

###############################################################################
# Footer                                                                      #
###############################################################################

# UC Model 1, Stage 1

footfun.foot_solver_call(file_list, hour_ahead)
footfun.foot_conventional_generators(file_list, hour_ahead, path_dict)
footfun.foot_power_blocks(file_list, hour_ahead, path_dict)
footfun.foot_slack_spillage(file_list, hour_ahead, path_dict)
footfun.foot_line_flows(file_list, hour_ahead, path_dict)

# CF stages
footfun.foot_congestion_forecast(file_list, hour_ahead, path_dict)
footfun.foot_cf1_tepo_depo_exchange(file_list, hour_ahead, path_dict)
footfun.foot_cf2_tepo_depo_exchange(file_list, hour_ahead, path_dict)

# --------------------------------------------------------------------------- #
# Kill file handles

input_file.close()

for handle in file_list:
    handle.close()
