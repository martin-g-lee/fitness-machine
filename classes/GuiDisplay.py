import PySimpleGUI as sg


sg.theme('Dark')

title_font = ('Helvetica', 24)
text_font = ('Helvetica', 18)
default_text_color = 'white'
low_text_color = 'red'
low_out_of_bound = 0.9

layout = [
    [sg.Text('Cadence',font=title_font)],
    [sg.Text('Now  :',font=text_font), sg.Text(key ='current_cadence_text',font=text_font, text_color=default_text_color)],
    [sg.Text('Want :',font=text_font), sg.Text(key ='target_cadence_text',font=text_font)],
    [sg.Text('_' * 20)],
    
    [sg.Text('Power',font=title_font)],
    [sg.Text('Now  :',font=text_font), sg.Text(key ='current_power_text',font=text_font, text_color=default_text_color)],
    [sg.Text('Want :',font=text_font), sg.Text(key ='target_power_text',font=text_font)],
    [sg.Text('_' * 20)],
    
    [sg.Text('Heart',font=title_font)],
    [sg.Text('Now  :',font=text_font), sg.Text(key ='current_heart_text',font=text_font, text_color=default_text_color)],
    [sg.Text('Want :',font=text_font), sg.Text(key ='target_heart_text',font=text_font)],
    [sg.Text('_' * 20)],
    
    [sg.Text('Segment',font=title_font)],
    [sg.Text('Description  :',font=text_font), sg.Text(key ='current_segment_text',font=text_font)],
    [sg.Text('Segment Time  :',font=text_font), sg.Text(key ='segment_time_text',font=text_font)],
    [sg.Text('Next Up  :',font=text_font), sg.Text(key ='next_segment_text',font=text_font)],
    [sg.Text('_' * 20)],
    [sg.Button('Go'), sg.Button('Quit')]
]
