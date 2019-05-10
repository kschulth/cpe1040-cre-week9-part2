from microbit import *
import utime

# screens
screen_id = 0
screens = {0: 'bits', 1: 'value'}
page_id = 0
pages = {0: 'type', 1: 'scroll'}
type_id = 0
types = {0: 'U', 1: 'I', 2: 'F', 3: 'C'}
scrolled_value = 2.134
value_funs = {}
scrolled = False
hold_b = False

# holds
hold_ms = 2000
blink_ms = 500
scroll_ms = 1000

# bits
bit_list = []
current_bit = 0
bit_on = 5
cursor_on = 9
led_arrary_side = 5
max_array_bits = led_arrary_side * led_arrary_side
max_bits = 32


# display
def bit_image():
    global bit_list
    global bit_string
    global current_bit
    global bit_on

    num_bits = len(bit_list)
    show_bits = []

    if num_bits >= max_array_bits:
        show_bits.extend([b for b in bit_list[max_array_bits:]])
    else:
        show_bits.extend([b for b in bit_list])
    show_bits.append(current_bit)
    show_bits.extend([0 for _ in range(max_array_bits - len(show_bits))])
    bit_string = ''.join([str(bit_on) if b == 1 else '0' for b in show_bits])
    img_string = ':'.join([bit_string[0:5], bit_string[5:10], bit_string[10:15], bit_string[20:]])
    return Image(img_string)


# controls

def toggle_screen():
    global screen_id
    global screens
    global bit_list

    screen_id = (screen_id + 1) % 2
    if screens[screen_id] == 'bits':
        bit_list.clear()


def action_b_press():
    global bit_list
    global current_list
    global pages
    global page_id
    global max_bits
    global types
    global type_id
    global value_funs
    global scrolled
    global scroll_value
    global current_bit
    global show_bits

    if screens[screen_id] == 'bits':
        if len(bit_list) < max_bits:
            bit_list.append(current_bit)
            current_bit = 0
        if len(bit_list) == max_bits:
            toggle_screen()
    elif screens[screen_id] == 'value':
        page_id = (page_id + 1) % 2
        if pages[page_id] == 'scroll':
            bit_string_list = [str(b) for b in bit_list]
            if len(bit_string_list) < max_bits:
                bit_string_list.extend(['0' for _ in range(25 - len(show_bits))])
            bit_string = ''.join(bit_string_list)
            value_funs[types[type_id]](bit_string)
            scrolled = False


def action_a_press():
    global bit_list
    global current_bit
    global type_id
    global types
    global scrolled
    global pages
    global page_id

    if screens[screen_id] == 'bits':
        if len(bit_list) < max_bits:
            current_bit = (current_bit + 1) % 2
    elif screens[screen_id] == 'value':
        if pages[page_id] == 'type':
            scrolled = False


def show():
    global screen_id
    global screens
    global page_id
    global pages
    global type_id
    global types
    global scroll_ms
    global scrolled
    global bit_image

    if screens[screen_id] == 'bits':
        display.show(bit_image())
    elif screens[screen_id] == 'value':
        if pages[page_id] == 'type':
            display.show(types[type_id])
        elif pages[page_id] == 'scroll':
            if not scroll:
                scrolled = True
                display.scroll(scroll_value, wait=False)


def bit_pattern_value_unsigned(bit_string):
    global scroll_value
    scroll_value = int(bit_string, 2)


def bit_pattern_value_signed(bit_string):
    global scroll_value
    scroll_value = '?'


def bit_pattern_value_floating(bit_string):
    global scroll_value
    scroll_value = '?'


def bit_pattern_value_ascii(bit_string):
    global scroll_value
    scroll_value = '?'


value_funs[types[0]] = bit_pattern_value_unsigned
value_funs[types[1]] = bit_pattern_value_signed
value_funs[types[2]] = bit_pattern_value_floating
value_funs[types[3]] = bit_pattern_value_ascii

# main loop
while True:
    show()
    if button_b.is_pressed():
        start_ms = utime.ticks_ms()
        while True:
            if not button_b.is_pressed():
                break
            if utime.ticks_diff(utime.ticks_ms(), start_ms) >= hold_ms:
                hold_b = True
                toggle_screen()
    if button_a.is_pressed():
        action_a_press()

    elif button_b.was_pressed():
        if hold_b:
            hold_b = False
        else:
            action_b_press()
