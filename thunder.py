import math
import matplotlib.pyplot as plt


def run():
    std_atm = [(0, 101325, 15), (1000, 89880, 8.50), (2000, 79500, 2.00), (3000, 70012, -4.49), (4000, 61660, -10.98)]  # list of tuples: (height, pressure, temperature)
    atm_w_density = []  # (height, pressure, temperature, density, sp_sound)
    atm_height_list = []  # height
    t_base = 4000   # (base  of cumulonimbus, assumed to be source of lightning, 200 m to 4000 m)
    atm_w_density = build_atm_w_density(std_atm)
    atm_height_list = build_atm_height_list(std_atm)
    start_i = get_start_idx(t_base, atm_height_list)
    graph_list = []
    for andx in range(0, 40):
        s_angle = 2 * andx
        angle = s_angle
        curr_y = t_base
        curr_x = 0
        indx = start_i
        x_list = []
        y_list = []
        while indx > 0 and angle < 90:
            next_i = indx - 1
            next_y = atm_height_list[next_i]
            next_x = get_next_x(curr_x, curr_y, angle, next_y)

            x_list.append(next_x)
            y_list.append(next_y)
            next_angle = get_next_angle(angle, indx, atm_w_density)
            curr_x = next_x
            curr_y = next_y
            indx = next_i
            angle = next_angle

            # end loop for angle
        graph_item = [s_angle, x_list, y_list]
        graph_list.append(graph_item)
    print_graph_list(graph_list)


def get_start_idx(height, std_atm_height_list):
    return std_atm_height_list.index(height)


def get_next_x(curr_x, curr_y, angle, next_y):
    rangle = math.radians(angle)
    delta_y = curr_y - next_y
    delta_x = delta_y * math.tan(rangle)
    next_x = curr_x + delta_x
    return next_x


def get_next_angle(angle, indx, atm_w_density):
    next_i = indx - 1
    tempC1 = atm_w_density[indx][2]
    pressure1 = atm_w_density[indx][1]
    density1 = get_density(pressure1, tempC1)
    v1 = get_speed_sound(pressure1, density1)
    tempC2 = atm_w_density[next_i][2]
    pressure2 = atm_w_density[next_i][1]
    density2 = get_density(pressure2, tempC2)
    v2 = get_speed_sound(pressure2, density2)
    next_angle = get_refraction(angle, v1, v2)
    return next_angle


def build_atm_w_density(in_atm):
    new_atm_list = []
    for indx in range(len(in_atm)):
        height = in_atm[indx][0]
        pressure = in_atm[indx][1]
        tempC = in_atm[indx][2]
        density = get_density(pressure, tempC)
        c_dry = get_speed_sound(pressure, density)
        atm_item = (height, pressure, tempC, density, c_dry)
        new_atm_list.append(atm_item)
    return new_atm_list


def build_atm_height_list(in_atm):
    new_atm_list = []
    for indx in range(len(in_atm)):
        height = in_atm[indx][0]
        new_atm_list.append(height)
    return new_atm_list


def get_density(pressure, temperature):  # assumes dry air
    tempK = temperature + 273.15
    Rconst = 287.05
    density = pressure / (Rconst * tempK)
    return density


def get_speed_sound(pressure, density):
    kappa = 1.402
    sound = math.sqrt(kappa * pressure / density)
    return sound


def get_refraction(dangle1, v1, v2):
    rangle1 = math.radians(dangle1)
    expr = math.sin(rangle1) * v2 / v1
    if expr > 1:
        dangle2 = 90
    else:
        rangle2 = math.asin(expr)
        dangle2 = math.degrees(rangle2)
    return dangle2


def print_graph_list(graph_list):
    len_iter = len(graph_list[0][1])
    for indx in range(len_iter):
        print(str(graph_list[indx][0]) + ',', end='', flush=True)
        for andx in range(len(graph_list)):
            try:
                print(str(graph_list[andx][indx]) + ',', end='', flush=True)
            except IndexError:
                print(',', end='', flush=True)
        print('/r/n')


if __name__ == '__main__':
    run()
