from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import DocumentForm
from .models import Document, WorkOut
from django.utils.text import slugify
import re
import datetime
import os
from GLC import settings

import ast
from django.utils.encoding import smart_text
from decimal import Decimal
import json
from io import StringIO

import csv
from django.contrib.auth.decorators import login_required


def home_redirect(request):
    return redirect('home/')


def home(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            upload = request.FILES['data']

            boat_name = ''
            date = ''
            session_type = ''
            speed_input = ''
            total_distance = ''

            distance_from_start = []
            split = []
            speed = []
            distance_per_stroke = []
            elapsed_time = []
            stroke_rate = []

            csvf = StringIO(upload.read().decode())
            reader = csv.reader(csvf, delimiter=',')

            row_counter = 0
            for row in reader:
                if row_counter == 2:
                    boat_name = row[5]
                elif row_counter == 3:
                    s = row[1]
                    date, start_time = s.split(' ')
                elif row_counter == 4:
                    session_type = row[1]
                elif row_counter == 6:
                    speed_input = row[1]

                elif row_counter == 15:
                    total_time = row[3]
                    avg_stroke_rate = row[8]
                    if speed_input == 'Impeller':
                        total_distance = row[2]
                        avg_split = row[6]
                        avg_speed = row[7]
                    else:
                        total_distance = row[1]
                        avg_split = row[4]
                        avg_speed = row[5]

                elif row_counter > 30:

                    elapsed_time.append(row[3])
                    stroke_rate.append(row[8])

                    if speed_input == 'Impeller':
                        distance_from_start.append(row[2])
                        split.append(row[6])
                        speed.append(row[7])
                        distance_per_stroke.append(row[11])
                    else:
                        distance_from_start.append(row[1])
                        split.append(row[4])
                        speed.append(row[5])
                        distance_per_stroke.append(row[10])

                row_counter += 1

            workout = WorkOut.objects.create()

            workout.distance_from_start = json.dumps(distance_from_start)
            workout.split = json.dumps(split)
            workout.speed = json.dumps(speed)
            workout.distance_per_stroke = json.dumps(distance_per_stroke)
            workout.stroke_rate = json.dumps(stroke_rate)
            workout.elapsed_time = json.dumps(elapsed_time)
            workout.total_distance = total_distance

            workout.total_time = total_time
            workout.avg_stroke_rate = avg_stroke_rate
            workout.avg_split = avg_split
            workout.avg_speed = avg_speed

            workout.boat = boat_name
            workout.date = date
            workout.time = start_time
            workout.session_type = session_type
            workout.speed_input = speed_input
            workout.slug = slugify(boat_name + str(workout.id))
            workout.save()

            return redirect('data')
    else:
        form = DocumentForm()
    return render(request, 'home.html', {'form': form})


@login_required
def data(request):
    all_workouts = WorkOut.objects.all()

    return render(request, "data.html", {'all_workouts': all_workouts})


@login_required
def graph(request, **kwargs):
    piece = get_object_or_404(WorkOut, slug=kwargs.get('slug'))

    elapsed_time = ast.literal_eval(piece.elapsed_time)
    stroke_rate = ast.literal_eval(piece.stroke_rate)
    split = ast.literal_eval(piece.split)
    speed = ast.literal_eval(piece.speed)
    distance_per_stroke = ast.literal_eval(piece.distance_per_stroke)
    distance_from_start = ast.literal_eval(piece.distance_from_start)

    per_stroke_data = zip(*[elapsed_time, stroke_rate, split, speed, distance_per_stroke, distance_from_start])

    return render(request, "graph.html", {'piece': piece, 'per_stroke_data': per_stroke_data})


def parse_time(time):
    h, m, s, mm = re.split('[:.]', time)
    h = (int(h) * 3600000)
    m = (int(m) * 60000)
    s = (int(s) * 1000)
    mm = (int(mm) * 100)
    milliseconds = h + m + s + mm

    return milliseconds


def json_data_split_elp(request, **kwargs):
    piece = get_object_or_404(WorkOut, slug=kwargs.get('slug'))

    elapsed_time = ast.literal_eval(piece.elapsed_time)
    split = ast.literal_eval(piece.split)

    elp = [parse_time(i) for i in elapsed_time]
    split = [parse_time(i) for i in split]

    split_elp_dataset = [list(a) for a in zip(elp, split)]

    false = None  # to allow usage of JS 'false' without escaping quotations
    true = None  # to allow usage of JS 'false' without escaping quotations
    datetime = None

    # TODO show time data on Y axis too- currently in milliseconds
    chart = {
        "title": {
            "text": "Split / Elapsed Time",
        },

        "rangeSelector": {
            "enabled": false,
        },
        "yAxis": [{
            "title": {
                "text": 'Split /500m',
            },
            'type': 'datetime',
            'tooltipValueFormat': '{value: %M:%S}',
            "labels": {
                "format": '{value: %M:%S}',
            },
            "opposite": false

        }],
        "xAxis": {
            "title": {
                "enabled": true,
                "text": 'Elapsed Time',
            },
            "labels": {
                "format": '{value: %M:%S}',
            },
        },
        "credits": {
            "enabled": false
        },
        "exporting": false,
        "tooltip": {
            "xDateFormat": '%M:%S',
        },
        "series": [
            {
                "name": "Split",
                "data": split_elp_dataset,
                "type": 'spline',
                "showInNavigator": "true"

            }
        ]
    }
    return JsonResponse(chart)


def json_data_dps_elp(request, **kwargs):
    piece = get_object_or_404(WorkOut, slug=kwargs.get('slug'))

    elapsed_time = ast.literal_eval(piece.elapsed_time)
    distance_per_stroke = ast.literal_eval(piece.distance_per_stroke)

    elp = [parse_time(i) for i in elapsed_time]
    distance_per_stroke = [float(i) for i in distance_per_stroke]

    dps_elp_dataset = [list(a) for a in zip(elp, distance_per_stroke)]

    false = None  # to allow usage of JS 'false' without escaping quotations
    true = None

    chart = {
        "title": {
            "text": "Distance Per Stroke / Elapsed Time"
        },
        "rangeSelector": {
            "enabled": false,
        },
        "yAxis": [{
            "title": {
                "text": 'Distance',
            },
            "labels": {
                "format": '{value} m',
            },
            "opposite": false
        }],
        "xAxis": {
            "title": {
                "enabled": true,
                "text": 'Elapsed Time',
            },
            "labels": {
                "format": '{value: %M:%S}',
            },
        },
        "credits": {
            "enabled": false
        },
        "exporting": false,
        "tooltip": {
            "xDateFormat": '%M:%S',
            "valueSuffix": " meters"
        },
        "series": [
            {
                "name": "Distance Per Stroke",
                "data": dps_elp_dataset,
                "type": 'spline',
                "showInNavigator": "true"

            }
        ]
    }
    return JsonResponse(chart)


def json_data_SR_DfS(request, **kwargs):
    piece = get_object_or_404(WorkOut, slug=kwargs.get('slug'))

    stroke_rate = ast.literal_eval(piece.stroke_rate)
    distance_from_start = ast.literal_eval(piece.distance_from_start)

    dfs = [float(i) for i in distance_from_start]
    sr = [float(i) for i in stroke_rate]
    SR_DfS_dataset = [list(a) for a in zip(dfs, sr)]

    false = None  # to allow usage of JS 'false' without escaping quotations
    true = None

    chart = {
        "title": {
            "text": "Stroke Rate / Distance From Start"
        },

        "yAxis": [{
            "title": {
                "text": 'Stroke Rate',
            },
            "labels": {
                "format": '{value}',

            },
            "opposite": false
        }],
        "xAxis": {
            "title": {
                "enabled": true,
                "text": 'Distance from Start',
            }
        },
        "tooltip": {
            "valueSuffix": " SpM"
        },

        "credits": {
            "enabled": false
        },
        "exporting": false,
        "legend": {
            'enabled': false
        },
        "series": [
            {
                "name": "Stroke Rate",
                "data": SR_DfS_dataset,
                "type": 'spline',
                "showInNavigator": "true"

            }
        ]
    }
    return JsonResponse(chart)


def json_data_dps_dfs(request, **kwargs):
    piece = get_object_or_404(WorkOut, slug=kwargs.get('slug'))

    distance_per_stroke = ast.literal_eval(piece.distance_per_stroke)
    distance_from_start = ast.literal_eval(piece.distance_from_start)

    dfs = [float(i) for i in distance_from_start]
    dps = [float(i) for i in distance_per_stroke]
    dps_dfs_dataset = [list(a) for a in zip(dfs, dps)]
    false = None  # to allow usage of JS 'false' without escaping quotations
    true = None
    chart = {
        "title": {
            "text": "Distance Per Stroke / Distance From Start"
        },
        "rangeSelector": {
            "selected": "1",
        },

        "yAxis": [{
            "title": {
                "text": 'Distance',
            },
            "labels": {
                "format": '{value} m',
            },
        }],
        "xAxis": {
            "title": {
                "enabled": true,
                "text": 'Distance from Start',
            }
        },
        "tooltip": {
            "valueSuffix": " m"
        },
        "legend": {
            'enabled': false
        },
        "credits": {
            "enabled": false
        },
        "exporting": false,
        "series": [
            {
                "name": "Distance Per Stroke",
                "data": dps_dfs_dataset,
                "type": 'spline',
                "showInNavigator": "true"

            }
        ]
    }
    return JsonResponse(chart)
