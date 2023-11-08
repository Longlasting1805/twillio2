from django.shortcuts import render

# Create your views here.

import json
import requests
from django.http import JsonResponse
from twilio.twiml.voice_response import Dial, Gather, Play, Pause, Record, Redirect, Stream


def handle_incoming_call(request):
    # Retrieve user's workout plan from the request body
    user_workout_plan = json.loads(request.body.decode('utf-8'))['workoutPlan']

    # Initialize Twiml response
    response = Dial()

    # Process workout plan and generate Twiml prompts
    for exercise in user_workout_plan:
        exercise_name = exercise['name']
        exercise_sets = exercise['sets']
        exercise_reps = exercise['reps']

        # Provide instructions for each exercise
        response.append(Play(audio_url='https://demo.twilio.com/docs/voice/tutorial/audio-prompts.xml#exercise-start-prompt'))
        response.append(Play(audio=exercise_name))
        response.append(Play(audio="Perform {} sets of {} repetitions each.".format(exercise_sets, exercise_reps)))

        # Provide guidance during each set
        for set_number in range(exercise_sets):
            response.append(Play(audio="Set number {}. Start.".format(set_number + 1)))
            for rep_number in range(exercise_reps):
                response.append(Play(audio="Rep number {}.".format(rep_number + 1)))
                response.append(Pause(length=1))  # Pause for exercise execution
            response.append(Play(audio="Set complete."))

        # Provide a rest prompt after each exercise
        response.append(Play(audio="Rest for 30 seconds."))
        response.append(Pause(length=30))

    # Conclude the workout session
    response.append(Play(audio="Workout complete. Congratulations!"))

    # Return the Twiml response
    return JsonResponse({'twiml': str(response)})