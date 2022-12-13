
#  MK3 params and limits
MK3_preamble = "M73 P0 R743\n" \
               "M73 Q0 S748\n" \
               "M201 X1000 Y50 Z200 E5000 ; sets maximum accelerations, mm/sec^2\n" \
               "M203 X200 Y20 Z12 E120 ; sets maximum feedrates, mm / sec\n" \
               "M204 P1250 R1250 T1250 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2\n" \
               "M205 X8.00 Y1.00 Z0.40 E4.50 ; sets the jerk limits, mm/sec\n" \
               "M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec\n" \
               "M107\n" \
               ";TYPE:Custom\n" \
               "M862.3 P ""MK3S"" ; printer model check\n" \
               "M862.1 P0.4 ; nozzle diameter check\n" \
               "M115 U3.10.1 ; tell printer latest fw version\n" \
               "G90 ; use absolute coordinates\n" \
               "G1 Z0.2 F720\n" \
               "G28 W ; home all without mesh bed level\n" \
               "G1 Z0.2 F720\n" \
               "G1 Y-3 F1000 ; go outside print area" \
               "G1 Y-3 F1000 ; go outside print area\n" \
               "; Don't change E values below. Excessive value can damage the printer.\n" \
               "M907 E430 ; set extruder motor current\n" \
               "G21 ; set units to millimeters\n" \
               "G90 ; use absolute coordinates\n" \
               "M83 ; use relative distances for extrusion\n"

MK3_max_x = 250  # mm
MK3_max_y = 220  # mm
MK3_max_z = 220

# sensor mounting offsets (add to pos to get desired sensor pos)
MK3_sensor_x_offset = -28.75
MK3_sensor_y_offset = 44.5

# setup
# grid increment values in mm
x_grid = 2
y_grid = 2
z_set = 200
x_start = 90
y_start = 45

# window setup
part_low_bound_x = 100
part_low_bound_y = 35

beam_size = 20
perim_offset = 10

# part params
part_x_width = 100
part_y_width = 100

# window calc
x_min = part_low_bound_x - beam_size - perim_offset + MK3_sensor_x_offset
x_max = part_low_bound_x + beam_size + perim_offset + part_x_width + MK3_sensor_x_offset

y_min = part_low_bound_y - beam_size - perim_offset + MK3_sensor_y_offset
y_max = part_low_bound_y + part_y_width + beam_size + perim_offset + MK3_sensor_y_offset


def g_code_gen():
    meas_time = 1000

    gc = ""
    gc = gc + MK3_preamble  # add preamble
    gc = gc + "G1 Z" + str(z_set) + "\n"  # move Z to constant height

    # gc = gc + meas_point(meas_time)
    # add_output_point(x=x_start, y=y_start, z=z_set)

    gc = pop_grid(gc=gc, x_inc=x_grid, y_inc=y_grid, meas_time=meas_time, x_max=x_max, y_max=y_max, x_start=x_min, y_start=y_min)

    with open('sensor.gcode', 'w') as f:
        f.write(gc)

    return


def pop_grid(gc, x_inc, y_inc, meas_time, x_max, y_max, x_start, y_start):

    right = True

    x = x_start
    y = y_start
    gc = gc + move_code(x=x, y=y, z=z_set)  # add x move
    gc = gc + meas_point(meas_time)
    add_output_point(x=x, y=y)

    while y <= y_max:
        print(y)
        if right:
            while x <= x_max:
                x = x + x_inc
                gc = gc + move_code(x=x, z=z_set)  # add x move
                gc = gc + meas_point(meas_time)
                add_output_point(x=x, y=y)

                if x == x_max:  # reaches end of y
                    y = y + y_inc

                    if y <= y_max:
                        gc = gc + move_code(y=y, z=z_set)
                        gc = gc + meas_point(meas_time)
                        add_output_point(x=x, y=y)
                    right = not right  # negate bool ( go other direction)
                    break
        else:
            while x >= x_start:
                x = x - x_inc

                gc = gc + move_code(x=x, z=z_set)  # add x move
                gc = gc + meas_point(meas_time)
                add_output_point(x=x, y=y)

                if x == x_start:  # reaches end of y
                    y = y + y_inc

                    if y <= y_max:
                        gc = gc + move_code(y=y, z=z_set)
                        gc = gc + meas_point(meas_time)
                        add_output_point(x=x, y=y)
                    right = not right  # negate bool ( go other direction)
                    break

    return gc


def meas_point(meas_time):

    meas_code = "G4 S0 ;Wait for move to finish\n" \
                "M42 S255 P73 ;Trigger\n" \
                "G4 P" + str(meas_time) + ";Wait for wait time 200ms\n" \
                "M42 S0 P73 ;Untrigger\n"

    return meas_code


def move_code(x=None, y=None, z=None):

    move = "G1"
    if x != None:
        move = move + " X" + str(x)

    if y != None:
        move = move + " Y" + str(y)

    if z != None:
        move = move + " Z" + str(z)

    move = move + "\n"

    return move


def add_output_point(x, y):
    point_str = str(x) + "," + str(y) + "\n"

    with open('sensor.txt', 'a') as f:
        f.write(point_str)

    return


def main():
    g_code_gen()
    return


if __name__ == "__main__":
    main()
