import json
import base64

from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from django.template import loader
from django.middleware.csrf import get_token

import cv2

from alpr_django_project.classvhdet import VehicleDetection

from .forms import RTSPURLForm
from .models import RTSPUrlModel


def generate(detector,video_path):
    frame_index=0
    cap = cv2.VideoCapture(video_path)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break
        if frame.shape[0] == 0:
            print("Skipping frame with zero height.")
            continue

        if frame.shape[1] == 0:
            print("Skipping frame with zero width.")
            continue
        if frame_index % 5 == 0:
                
            # Convert the frame to JPEG format
            for frame, detected_word in detector.process_video(frame):
                
                _, jpeg = cv2.imencode('.jpg', frame)
                frame_bytes = jpeg.tobytes()
                frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')
                data = {
                    'image': frame_base64,  # Convert the frame to a list
                    'word': detected_word
                }
                yield f'data: {json.dumps(data)}\n\n'
        frame_index+=1

    print("Releasing Video")
    cap.release()

def main_app(request):
    context = dict()
    if request.method == "GET":
        form = RTSPURLForm()
    elif request.method == "POST":
        form = RTSPURLForm(request.POST)
        if form.is_valid():
            rtsp_url = form.save()
            context['rtsp_url_id'] = rtsp_url.id
    context['form'] = form
    return render(request,'main.html',context=context)

def mask_feed(request,rtsp_url_id):
    instance = RTSPUrlModel.objects.get(pk=rtsp_url_id)
    detector=VehicleDetection()
    video_path=instance.url
    response = StreamingHttpResponse(generate(detector, video_path), content_type="text/event-stream")
    print("streaming started")
    return response  
    # return render(request, 'mask_feed.html', response_data)    
