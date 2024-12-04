from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule
import csv
import io
import pandas as pd


def create_edit_view(request, pk=None):
    if request.method == 'POST' and not request.FILES:
        schedule = {}

        for key in request.POST.keys():
            if '_' in key and key not in ['class_name', 'school_name', 'region_name', 'school_shift']:
                split_key = key.split("_")

                if split_key[0] not in schedule.keys():
                    schedule[split_key[0]] = [request.POST[key] if request.POST[key] else "-"]
                else:
                    schedule[split_key[0]].append(request.POST[key] if request.POST[key] else "-")

        for key in schedule.keys():
            sorted_value = []
            start, end = 0, 4

            for _ in range(len(schedule[key]) // 4):
                sorted_value.append(schedule[key][start:end])
                start += 4
                end += 4

            schedule[key] = sorted_value

        if pk:
            Schedule.objects.filter(pk=pk).update(
                creator=request.user,
                schedule=schedule,
                class_name=request.POST["class_name"],
                school_shift=request.POST["school_shift"],
                school_name=request.POST["school_name"],
                region_name=request.POST["region_name"],
            )

            schedule_obj = Schedule.objects.get(pk=pk)
        else:
            schedule_obj = Schedule.objects.create(
                creator=request.user,
                schedule=schedule,
                class_name=request.POST["class_name"],
                school_shift=request.POST["school_shift"],
                school_name=request.POST["school_name"],
                region_name=request.POST["region_name"],
            )

        return redirect("schedules:detail", schedule_obj.pk)
    else:
        if pk:
            schedule = get_object_or_404(Schedule, pk=pk)

            context = {
                "updated": schedule.updated,
                "class_name": schedule.class_name,
                "school_shift": schedule.school_shift,
                "school_name": schedule.school_name,
                "region_name": schedule.region_name,
                "schedule": schedule.schedule,
            }

            return render(request, 'schedules/edit.html', context=context)
        elif 'file' in request.FILES:
            if request.FILES['file'].name[-4:] == '.csv':
                file = request.FILES['file'].read().decode('utf-8')

                schedule = {
                    "ПОНЕДЕЛЬНИК": [],
                    "ВТОРНИК": [],
                    "СРЕДА": [],
                    "ЧЕТВЕРГ": [],
                    "ПЯТНИЦА": [],
                    "СУББОТА": []
                }

                excel_data = list(csv.DictReader(io.StringIO(file)))

                for i in range(0, len(excel_data), 8):
                    for field in excel_data[i:i+8]:
                        if list(field.values())[0].isnumeric():
                            if i == 0:
                                schedule["ПОНЕДЕЛЬНИК"].append(list(field.values())[1:])
                            elif i == 8:
                                schedule["ВТОРНИК"].append(list(field.values())[1:])
                            elif i == 16:
                                schedule["СРЕДА"].append(list(field.values())[1:])
                            elif i == 24:
                                schedule["ЧЕТВЕРГ"].append(list(field.values())[1:])
                            elif i == 32:
                                schedule["ПЯТНИЦА"].append(list(field.values())[1:])
                            elif i == 40:
                                schedule["СУББОТА"].append(list(field.values())[1:])

                return render(request, 'schedules/edit.html', context={"schedule": schedule})

            context = {
                "format_error": True,
                "weekdays": ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА"]
            }

            return render(request, 'schedules/create.html', context=context)
        else:
            context = {
                "weekdays": ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА"]
            }

            return render(request, 'schedules/create.html', context=context)


def detail_view(request, pk):
    schedule = Schedule.objects.get(pk=pk)

    if "delete_submit" in request.POST:
        schedule.delete()
        return render(request, 'schedules/delete_success.html')

    if 'search' in request.GET:
        schedules = search_view(Schedule.objects.all(), request.GET.get('search', ''))

    context = {
        "updated": schedule.updated,
        "class_name": schedule.class_name,
        "school_shift": schedule.school_shift,
        "school_name": schedule.school_name,
        "region_name": schedule.region_name,
        "schedule": schedule.schedule,
        "schedule_pk": pk,
    }

    return render(request, 'schedules/detail.html', context=context)


def list_view(request):
    schedules = Schedule.objects.all()

    if request.GET.get('search', ''):
        schedule = search_view(schedules, request.GET['search'])

    context = {'schedules': schedules}

    if request.user.is_authenticated:
        user_schedules = schedules.filter(creator=request.user)
        other_schedules = schedules.exclude(creator=request.user)

        context = {
            'user_schedules': user_schedules,
            'schedules': other_schedules,
        }

    return render(request, 'schedules/list.html', context=context)


def search_view(schedules, search_data):
    return schedules.get(pk=search_data)
