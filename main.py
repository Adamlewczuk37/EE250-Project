from flask import Flask
from flask import request
import pathlib
import json

app = Flask(__name__)
thisdir = pathlib.Path(__file__).parent.absolute()

@app.route('/input_receiver', methods=['POST'])
def add_route():
    entry = request.get_json()

    temp = []
    try:
        temp = json.loads(thisdir.joinpath('input.json').read_text())
    except FileNotFoundError:
        temp = []

    temp.append(entry)
    print(temp)

    string = temp[0]
    chunks = string.split(' ')
    hh_thresh = int(chunks[0])
    lh_thresh = int(chunks[1])
    lac_thresh = int(chunks[2])
    hac_thresh = int(chunks[3])
    temperature = int(chunks[4])

    if len(past_vals) == 0:
        past_vals[0] = temperature
        val = temperature
    elif len(past_vals) == 1:
        past_vals[1] = temperature
        val = temperature + past_vals[0] / 2
    else:
        val = temperature + past_vals[0] + past_vals[1] / 3
        past_vals[0] =  past_vals[1]
        past_vals[1] = temperature
    
    if val <= hh_thresh:
        print("Cold: high heating on")
    elif (val > hh_thresh) and (val <= lh_thresh):
        print("Cool: low heating on")
    elif (val > lh_thresh) and (val <= lac_thresh):
        print("Good temperature: no heating control")
    elif (val > lac_thresh) and (val <= hac_thresh):
        print("Warm: low ac on")
    else:
        print("Hot: high ac on")

    temp = []



if __name__ == '__main__':
    app.run(port=5000, debug=True)