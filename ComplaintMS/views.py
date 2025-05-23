
from django.http import HttpResponseRedirect

import random

from django.contrib.auth.models import User

# A dictionary to store OTPs temporarily
otp_storage = {}

from django.contrib.auth import login as auth_login

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from django.core.mail import EmailMessage

from django.urls import reverse

  # Ensure this is present

from django.db.models import Count, Q



import matplotlib
matplotlib.use('Agg')



import tempfile
import matplotlib.pyplot as plt
from textblob import TextBlob

from django.http import HttpResponse
from .forms import UserRegisterForm,ProfileUpdateForm,UserProfileform,ComplaintForm,UserProfileUpdateform,statusupdate

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

#page loading.
def index(request):
    return render(request,"ComplaintMS/home.html")

def aboutus(request):
    return render(request,"ComplaintMS/aboutus.html")

def login(request):
    return render(request,"ComplaintMS/login.html")

def signin(request):
    return render(request,"ComplaintMS/signin.html")

#get the count of all the submitted complaints,solved,unsolved.
def counter(request):
        total=Complaint.objects.all().count()
        unsolved=Complaint.objects.all().exclude(status='1').count()
        solved=Complaint.objects.all().exclude(Q(status='3') | Q(status='2')).count()
        dataset=Complaint.objects.values('Type_of_complaint').annotate(total=Count('status'),solved=Count('status', filter=Q(status='1')),
                  notsolved=Count('status', filter=Q(status='3')),inprogress=Count('status',filter=Q(status='2'))).order_by('Type_of_complaint')
        args={'total':total,'unsolved':unsolved,'solved':solved,'dataset':dataset,}
        return render(request,"ComplaintMS/counter.html",args)

#changepassword for grievancemember.
def change_password_g(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password_g')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password_g.html', {
        'form': form
    })
    return render(request,"ComplaintMS/change_password_g.html")

#registration page.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form=UserProfileform(request.POST)
        if form.is_valid() and profile_form.is_valid() :

            new_user=form.save()
            profile=profile_form.save(commit=False)
            if profile.user_id is None:
                profile.user_id=new_user.id
            profile.save()
            messages.add_message(request,messages.SUCCESS, f' Registered Successfully ')
            return redirect('/login/')
    else:
        form = UserRegisterForm()
        profile_form=UserProfileform()

    context={'form': form,'profile_form':profile_form }
    return render(request, 'ComplaintMS/register.html',context )
import csv
from django.http import HttpResponse
from .models import Profile

def download_registered_users(request):
    """
    View to generate and download all registered users' data as a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registered_users.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Username', 'Email', 'School', 'Contact Number', 'Type of User', 'Branch'])

    # Write data rows
    profiles = Profile.objects.select_related('user')  # Optimize query
    for profile in profiles:
        writer.writerow([
            profile.user.username,
            profile.user.email,
            profile.School,
            profile.contactnumber,
            profile.type_user,
            profile.Branch
        ])

    return response

#login based on user.
def login_redirect(request):
    if request.user.profile.type_user=='student':
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/counter/')

def send_otp(email):
    try:
        # Generate OTP
        otp = random.randint(100000, 999999)
        otp_storage[email] = otp

        # Send OTP email
        subject = "Your One-Time Password (OTP) for Verification"
        message = "Please use the following OTP for verification."  # Fallback text for non-HTML email clients
        html_message = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        .email-container {{
                            font-family: Arial, sans-serif;
                            max-width: 500px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #ffffff;
                            border-radius: 8px;
                            border: 1px solid #e0e0e0;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }}
                        .header {{
                            padding: 20px;
                            background-color: #4CAF50;
                            border-radius: 8px 8px 0 0;
                        }}
                        .header img {{
                            max-width: 100px;
                        }}
                        .header h2 {{
                            color: white;
                            font-size: 22px;
                            margin: 10px 0;
                        }}
                        .body-content {{
                            padding: 20px;
                            color: #333;
                        }}
                        .otp {{
                            font-size: 32px;
                            font-weight: bold;
                            color: #4CAF50;
                            background-color: #f1f8e9;
                            border-radius: 8px;
                            padding: 10px;
                            margin: 20px 0;
                            display: inline-block;
                            letter-spacing: 4px;
                        }}
                        .message {{
                            font-size: 16px;
                            color: #555;
                            line-height: 1.6;
                        }}
                        .footer {{
                            font-size: 12px;
                            color: #999;
                            padding: 20px;
                            border-top: 1px solid #e0e0e0;
                            margin-top: 20px;
                        }}
                        .copyright {{
                            text-align: center;
                            color: #999;
                            margin-top: 10px;
                            font-size: 12px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://i.ibb.co/svwHBWv/logo0.png" alt="Logo" />
                            <h2>Welcome to GEyan Portal</h2>
                        </div>
                        <div class="body-content">
                            <p class="message">Hello User!</p>
                            <p class="message">Thank you for using our service. To complete your verification, please use the following One-Time Password (OTP):</p>
                            <div class="otp">{otp}</div>
                            <p class="message">This code is valid for the next 10 minutes. For security reasons, please do not share it with anyone.</p>
                            <p class="message">Once verified, you’ll be able to access your account and explore all our features.</p>
                        </div>
                        <div class="footer">
                            <div class="copyright">
                                © Copyright 2024, All Rights Reserved by Graphic Era
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                """
        send_mail(
            subject=subject,
            message=message,  # Plain-text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,  # HTML content
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False



otp_storage = {}

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        # Step 1: If email is provided, generate and send OTP
        if email and not otp:
            try:
                user = User.objects.get(email=email)

                # Send OTP
                if send_otp(email):
                    messages.success(request, "An OTP has been sent to your registered email address.")
                    return render(request, "ComplaintMS/login.html", {"email": email})
                else:
                    messages.error(request, "Failed to send OTP. Please try again.")
            except User.DoesNotExist:
                messages.error(request, "Email is not registered.")
                return render(request, "ComplaintMS/login.html")

        # Step 2: If OTP is provided, validate it
        elif email and otp:
            stored_otp = otp_storage.get(email)
            if stored_otp and str(stored_otp) == otp:
                try:
                    user = User.objects.get(email=email)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth_login(request, user)
                    del otp_storage[email]  # Clear OTP after successful login
                    return redirect("dashboard")  # Replace with your redirect view
                except User.DoesNotExist:
                    messages.error(request, "User does not exist.")
            else:
                messages.error(request, "Invalid OTP.")
            return render(request, "ComplaintMS/login.html", {"email": email})

    return render(request, "ComplaintMS/login.html")



@login_required
def dashboard(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_update_form = UserProfileUpdateform(request.POST, instance=request.user.profile)
        if p_form.is_valid() and profile_update_form.is_valid():
            user = p_form.save()
            profile = profile_update_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.add_message(request, messages.SUCCESS, f'Updated Successfully')
            return render(request, 'ComplaintMS/dashboard.html', )
    else:
        p_form = ProfileUpdateForm(instance=request.user)
        profile_update_form = UserProfileUpdateform(instance=request.user.profile)
    context = {
        'p_form': p_form,
        'profile_update_form': profile_update_form
    }
    return render(request, 'ComplaintMS/dashboard.html', context)

#change password for user.

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password.html', {
        'form': form
    })





#complaints handling and submission section.
@login_required
def complaints(request):
    if request.method == 'POST':

        complaint_form = ComplaintForm(request.POST)
        if complaint_form.is_valid():
            instance = complaint_form.save(commit=False)
            instance.user = request.user
            #        mail=request.user.email
            #        print(mail)
            #        send_mail('Hi Complaint has been Received', 'Thank you for letting us know of your concern, Have a Cookie while we explore into this matter.  Dont Reply to this mail', 'testerpython13@gmail.com', [mail],fail_silently=False)
            instance.save()

            messages.add_message(request, messages.SUCCESS, f'Your Questions has been registered!')
            return render(request, 'ComplaintMS/comptotal.html', )
    else:

        complaint_form = ComplaintForm(request.POST)
    context = {'complaint_form': complaint_form, }
    return render(request, 'ComplaintMS/comptotal.html', context)
        

@login_required
def list(request):
    c=Complaint.objects.filter(user=request.user).exclude(status='1')
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'c':c,'result':result}
    return render(request,'ComplaintMS/Complaints.html',args)
@login_required
def slist(request):
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'result':result}
    return render(request,'ComplaintMS/solvedcomplaint.html',args)


@login_required
def certificate(request):

    return render(request,'ComplaintMS/certificate.html')

@login_required
def heat(request):

    return render(request,'ComplaintMS/heat.html')

@login_required
  # Ensure email settings are configured in settings.py
def allcomplaints(request):
    c = Complaint.objects.all().exclude(status='1')
    comp = request.GET.get("search")
    drop = request.GET.get("drop")

    if drop:
        c = c.filter(Q(Type_of_complaint__icontains=drop))
    if comp:
        c = c.filter(Q(Type_of_complaint__icontains=comp) | Q(Description__icontains=comp) | Q(Subject__icontains=comp))

    if request.method == 'POST':
        if 'cid2' in request.POST:  # For updating status
            cid = request.POST.get('cid2')
            uid = request.POST.get('uid')
            project = Complaint.objects.get(id=cid)
            forms = statusupdate(request.POST, instance=project)
            if forms.is_valid():
                obj = forms.save(commit=False)
                mail = User.objects.filter(id=uid)
                for i in mail:
                    m = i.email
                obj.save()
                messages.success(request, 'The changes have been updated!')
                return HttpResponseRedirect(reverse('allcomplaints'))
        elif 'cid_reply' in request.POST:  # For adding replies
            cid = request.POST.get('cid_reply')
            reply = request.POST.get('reply')

            # Update the reply in the database
            Complaint.objects.filter(id=cid).update(reply=reply)

            # Send HTML email notification to the user
            complaint = Complaint.objects.get(id=cid)
            user_email = complaint.user.email  # Assuming Complaint has a ForeignKey to User
            # subject = "Update from GEyan Project"
            from_email = settings.DEFAULT_FROM_EMAIL  # Ensure this is set in your settings.py

            # Create the email body with HTML
            subject = "Update from GEyan Project !"
            message_body = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <style>
                            .email-container {{
                                font-family: Arial, sans-serif;
                                max-width: 500px;
                                margin: 0 auto;
                                padding: 20px;
                                background-color: #ffffff;
                                border-radius: 8px;
                                border: 1px solid #e0e0e0;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                text-align: center;
                            }}
                            .header {{
                                padding: 20px;
                                background-color: #4CAF50;
                                border-radius: 8px 8px 0 0;
                            }}
                            .header img {{
                                max-width: 100px;

                            }}
                            .header h2 {{
                                color: white;
                                font-size: 22px;
                                margin: 10px 0;
                            }}
                            .body-content {{
                                padding: 20px;
                                color: #333;
                            }}
                            .otp {{
                                font-size: 32px;
                                font-weight: bold;
                                color: #4CAF50;
                                background-color: #f1f8e9;
                                border-radius: 8px;
                                padding: 10px;
                                margin: 20px 0;
                                display: inline-block;
                                letter-spacing: 4px;
                            }}
                            .message {{
                                font-size: 16px;
                                color: #555;
                                line-height: 1.6;
                            }}
                            .footer {{
                                font-size: 12px;
                                color: #999;
                                padding: 20px;
                                border-top: 1px solid #e0e0e0;
                                margin-top: 20px;
                            }}
                            .footer-address {{
                                text-align: left;
                                font-size: 12px;
                                margin-top: 10px;
                                color: #666;
                                line-height: 1.4;
                            }}
                            .footer-address h4 {{
                                margin: 5px 0;
                                font-weight: bold;
                            }}
                            .footer-address p {{
                                margin: 0;
                            }}
                            .copyright {{
                                text-align: center;
                                color: #999;
                                margin-top: 10px;
                                font-size: 12px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="email-container">
                            <div class="header">
                                <img src="https://i.ibb.co/svwHBWv/logo0.png" alt="Logo" />
                                <h2>Update on your Questions </h2>
                            </div>
                            <div class="body-content">
                                <p class="message">Hello {complaint.user.first_name} </p>
                                <p>We wanted to inform you that your Questions  with the subject <strong>{complaint.Subject}</strong> has been reviewed, and a response has been added by the teacher.</p>
        <p>You can log in to your account to view the response and take any further actions if needed.</p>
        
                            </div>
                            <div class="footer">

                                <div class="copyright">
                                    © Copyright 2024, All Rights Reserved by Graphic Era Hill University 
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """

            # Send the email
            email = EmailMessage(subject, message_body, from_email, [user_email])
            email.content_subtype = "html"  # Mark the email content as HTML
            email.send()

            messages.success(request, 'Reply has been added successfully and the user has been notified via email!')
            return HttpResponseRedirect(reverse('allcomplaints'))

    else:
        forms = statusupdate()

    args = {'c': c, 'forms': forms, 'comp': comp}
    return render(request, 'ComplaintMS/allcomplaints.html', args)



@login_required
def solved(request):
        
        cid=request.POST.get('cid2')
        c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
               
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                print(cid)
                project = Complaint.objects.get(id=cid)
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The changes has been updated!')
                        return HttpResponseRedirect(reverse('solved'))
                else:
                        return render(request,'ComplaintMS/solved.html')
                 #testing

        else:
                forms=statusupdate()
        #c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/solved.html',args)

#allcomplaints pdf viewer.




def generate_sentiment_pie_chart(detail_string):
    # Analyze sentiment using TextBlob
    analysis = TextBlob(detail_string)
    polarity = analysis.sentiment.polarity

    # Initialize sentiment scores
    sentiment_scores = {"Positive": 0, "Neutral": 0, "Negative": 0}
    if polarity > 0.1:
        sentiment_scores["Positive"] = 100
    elif polarity < -0.1:
        sentiment_scores["Negative"] = 100
    else:
        sentiment_scores["Neutral"] = 100

    # Define labels, sizes, and colors for the pie chart
    labels = sentiment_scores.keys()
    sizes = sentiment_scores.values()
    colors = ['#4CAF50', '#FFC107', '#F44336']  # Green, Yellow, Red for sentiments
    explode = (0.1, 0, 0)  # Explode the Positive segment slightly

    # Create the pie chart
    plt.figure(figsize=(6, 6))  # Adjusted size for better appearance
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        explode=explode,
        shadow=True,  # Add shadow for depth effect
        textprops={'fontsize': 12}  # Adjust font size for clarity
    )

    # Add a legend outside the pie chart
    plt.legend(
        wedges,
        labels,
        title="Sentiment",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),  # Position legend to the right
        fontsize=10
    )

    # Title and adjustments
    plt.title("User Sentiment Analysis", fontsize=14, fontweight='bold')
    plt.tight_layout()  # Adjust layout to prevent clipping

    # Save the plot to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name, format='PNG', bbox_inches='tight')
    plt.close()

    return temp_file.name



from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame
from textwrap import wrap
import os
from datetime import datetime

def pdf_viewer(request):
    cid = request.POST.get('cid')
    uid = request.POST.get('uid')
    complaint = Complaint.objects.select_related('user').get(id=cid)
    user = complaint.user

    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    date_joined = user.date_joined

    details = Complaint.objects.filter(id=cid).values('Description')
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')

    detail_string = next(iter(details))['Description'] if details else "No description provided"
    detailsubject = next(iter(Subject))['Subject'] if Subject else "No subject provided"
    detailtype = next(iter(Type))['Type_of_complaint'] if Type else "No type provided"
    detailtime = next(iter(Issuedate))['Time'] if Issuedate else "No time provided"
    reply = Complaint.objects.filter(id=cid).values('reply').first()
    reply_text = reply['reply'] if reply and reply['reply'] else "No reply yet"
    complaint_types = {
        '1': "What career options are available based on my strengths and interests?",
        '0': "What are the essential skills required for success in specific fields or industries?",
        '2': "How do I choose the right stream (Science, Commerce, or Arts) for my future career goals?",
        '3': "What is the current job market like for fresh graduates, and which industries have the best job prospects?",
        '4': "Other"
    }
    detailtype = complaint_types.get(detailtype, detailtype)

    date_format = "%Y-%m-%d"
    current_date = datetime.strptime(str(datetime.now().date()), date_format)
    issue_date = datetime.strptime(str(detailtime), date_format)
    delta = current_date - issue_date

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=GEyan~Report_{cid}.pdf'

    p = canvas.Canvas(response, pagesize=A4)

    image_path = 'ComplaintMS/static/ComplaintMS/img/template.jpg'
    if os.path.exists(image_path):
        p.drawImage(image_path, 0, 0, width=595, height=842)

    pie_chart_path = generate_sentiment_pie_chart(detail_string)
    p.drawImage(pie_chart_path, 450, 710, width=120, height=110)

    p.setFont("Helvetica", 10)
    p.drawString(150, 620, f"{first_name} {last_name} ({email})")
    p.drawString(150, 591, str(detailtype))
    p.drawString(100, 564, str(detailtime))
    p.drawString(130, 519, str(detailsubject))
    p.drawString(120, 265, str(reply_text))

    # Wrap the description text
    wrapped_text = wrap(detail_string, width=70)  # Adjust width as needed
    y_position = 415
    line_height = 15
    for line in wrapped_text:
        if y_position < 50:  # Prevent overlapping footer
            p.showPage()
            y_position = 800
        p.drawString(120, y_position, line)
        y_position -= line_height

    p.showPage()
    p.save()

    if os.path.exists(pie_chart_path):
        os.remove(pie_chart_path)

    return response





def reply_to_complaint(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('cid2')
        reply_message = request.POST.get(
            'reply_message')  # Assuming you have a field in your form named 'reply_message'

        # Fetch the complaint by ID and update the response
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.reply = reply_message  # Assuming you have a 'reply' field in your Complaint model
        complaint.status = 2  # Mark as replied (example)
        complaint.save()

        messages.success(request, 'Reply sent successfully.')
        return redirect('allcomplaints')  # Redirect to all complaints page

    return redirect('allcomplaints')
#complaints pdf view.


from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint
from .forms import ReplyForm



from django.shortcuts import render
from .models import Complaint

def all_complaints_view(request):
    complaints = Complaint.objects.all()  # Retrieve complaints
    return render(request, 'AllComplaints.html', {'complaints': complaints})


# Add these imports to your existing views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
import json


# Add these new models (you'll need to create these in models.py)
# from .models import CareerRoadmap, CareerTalk, Resource, AptitudeTest, Seminar, SuccessStory

# Career Roadmaps View
@login_required
def career_roadmaps(request):
    """Display stream-wise career roadmaps"""

    # Roadmap data structure - standardized with 'top_institutions'
    roadmaps = {
        'science': {
            'title': 'Science Stream Career Roadmap',
            'paths': [
                {
                    'career': 'Engineering',
                    'after_10th': ['Choose PCM (Physics, Chemistry, Math)', 'Focus on JEE preparation',
                                   'Join coaching if needed'],
                    'after_12th': ['Appear for JEE Main/Advanced', 'Apply to NITs, IITs, State colleges',
                                   'Consider private colleges as backup'],
                    'timeline': '4 years B.Tech → Job/M.Tech → Specialization',
                    'top_institutions': ['IIT Delhi', 'IIT Bombay', 'NIT Trichy', 'BITS Pilani'],
                    'salary_range': '₹3-50 LPA'
                },
                {
                    'career': 'Medical',
                    'after_10th': ['Choose PCB (Physics, Chemistry, Biology)', 'Start NEET preparation',
                                   'Focus on NCERT thoroughly'],
                    'after_12th': ['Clear NEET exam', 'Counseling for MBBS seats', 'Consider AIIMS/JIPMER'],
                    'timeline': '5.5 years MBBS → 1 year Internship → PG/Practice',
                    'top_institutions': ['AIIMS Delhi', 'CMC Vellore', 'KGMU', 'MAMC Delhi'],
                    'salary_range': '₹5-100+ LPA'
                },
                {
                    'career': 'Research',
                    'after_10th': ['Choose PCM/PCB based on interest', 'Focus on conceptual understanding',
                                   'Participate in science fairs'],
                    'after_12th': ['B.Sc in chosen field', 'Maintain high GPA', 'Look for research opportunities'],
                    'timeline': '3 years B.Sc → 2 years M.Sc → PhD → Research positions',
                    'top_institutions': ['IISc Bangalore', 'IISERs', 'DU', 'JNU'],
                    'salary_range': '₹4-30 LPA'
                }
            ]
        },
        'commerce': {
            'title': 'Commerce Stream Career Roadmap',
            'paths': [
                {
                    'career': 'Chartered Accountancy (CA)',
                    'after_10th': ['Choose Commerce with Maths', 'Register for CA Foundation',
                                   'Focus on Accounts & Maths'],
                    'after_12th': ['Clear CA Foundation', 'Start CA Intermediate', 'Look for articleship'],
                    'timeline': 'Foundation → Intermediate → Articleship → Final → Practice',
                    'top_institutions': ['ICAI', 'Various coaching institutes'],
                    'salary_range': '₹6-80+ LPA'
                },
                {
                    'career': 'Company Secretary (CS)',
                    'after_10th': ['Commerce stream', 'Good in law subjects', 'Register for CS Foundation'],
                    'after_12th': ['CS Executive level', 'Training period', 'Professional course'],
                    'timeline': 'Foundation → Executive → Professional → Practice',
                    'top_institutions': ['ICSI', 'Various coaching centers'],
                    'salary_range': '₹4-50 LPA'
                },
                {
                    'career': 'MBA',
                    'after_10th': ['Commerce/Any stream', 'Focus on communication skills', 'Leadership activities'],
                    'after_12th': ['Any graduation', 'Work experience (optional)', 'CAT/XAT/GMAT preparation'],
                    'timeline': 'Graduation → Work experience → MBA → Management roles',
                    'top_institutions': ['IIM A/B/C', 'FMS Delhi', 'XLRI', 'ISB Hyderabad'],
                    'salary_range': '₹8-100+ LPA'
                }
            ]
        },
        'arts': {
            'title': 'Arts Stream Career Roadmap',
            'paths': [
                {
                    'career': 'UPSC (Civil Services)',
                    'after_10th': ['Arts with History/Political Science', 'Current affairs awareness',
                                   'Strong foundation in social subjects'],
                    'after_12th': ['Any graduation', 'Choose optional subject wisely', 'Start preparation early'],
                    'timeline': 'Graduation → UPSC Preparation → Prelims → Mains → Interview',
                    'top_institutions': ['Various coaching institutes', 'Self-study with good books'],
                    'salary_range': '₹7-30 LPA (with allowances)'
                },
                {
                    'career': 'Law',
                    'after_10th': ['Arts/Commerce/Science', 'Good in English & reasoning', 'Debate participation'],
                    'after_12th': ['CLAT preparation', 'Apply to NLUs', '5-year integrated course or 3-year LLB'],
                    'timeline': '5 years BA LLB or Graduation + 3 years LLB → Practice/Corporate',
                    'top_institutions': ['NLSIU Bangalore', 'NALSAR Hyderabad', 'NLU Delhi'],
                    'salary_range': '₹3-200+ LPA'
                },
                {
                    'career': 'Journalism & Mass Communication',
                    'after_10th': ['Arts with English', 'Creative writing skills', 'Stay updated with current affairs'],
                    'after_12th': ['Mass Communication course', 'Internships in media', 'Build portfolio'],
                    'timeline': '3 years graduation → Specialization → Media industry',
                    'top_institutions': ['IIMC Delhi', 'Jamia Millia', 'Xavier Institute'],
                    'salary_range': '₹2-50+ LPA'
                }
            ]
        }
    }

    selected_stream = request.GET.get('stream', 'science')
    context = {
        'roadmaps': roadmaps,
        'selected_stream': selected_stream,
        'current_roadmap': roadmaps.get(selected_stream, roadmaps['science'])
    }
    return render(request, 'ComplaintMS/career_roadmaps.html', context)


# Career Talks View
@login_required
def career_talks(request):
    """Display career talks and recorded sessions"""

    # Sample career talks data (replace with database queries)
    career_talks = [
        {
            'id': 1,
            'title': 'How to Crack JEE Advanced - IIT Alumni Talk',
            'speaker': 'Rahul Sharma (IIT Delhi, Software Engineer at Google)',
            'youtube_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual URLs
            'duration': '45 minutes',
            'category': 'Engineering',
            'date': '2024-01-15',
            'views': 1250
        },
        {
            'id': 2,
            'title': 'NEET Strategy and Medical Career Guidance',
            'speaker': 'Dr. Priya Patel (AIIMS Delhi)',
            'youtube_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            'duration': '60 minutes',
            'category': 'Medical',
            'date': '2024-01-20',
            'views': 980
        },
        {
            'id': 3,
            'title': 'CA Journey: From Student to Partner',
            'speaker': 'CA Amit Kumar (Partner at Deloitte)',
            'youtube_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            'duration': '40 minutes',
            'category': 'Commerce',
            'date': '2024-01-25',
            'views': 756
        },
        {
            'id': 4,
            'title': 'UPSC Success Strategy - IAS Officer Interview',
            'speaker': 'Ms. Anjali Singh (IAS 2019 Batch)',
            'youtube_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            'duration': '50 minutes',
            'category': 'Civil Services',
            'date': '2024-02-01',
            'views': 2100
        }
    ]

    category_filter = request.GET.get('category', 'all')
    if category_filter != 'all':
        career_talks = [talk for talk in career_talks if talk['category'].lower() == category_filter.lower()]

    context = {
        'career_talks': career_talks,
        'selected_category': category_filter,
        'categories': ['Engineering', 'Medical', 'Commerce', 'Civil Services', 'Arts', 'Management']
    }
    return render(request, 'ComplaintMS/career_talks.html', context)


# Resources View
@login_required
def resources(request):
    """Display downloadable resources"""

    resources = {
        'colleges': {
            'title': 'Top Colleges Lists',
            'items': [
                {'name': 'Top Engineering Colleges 2024', 'type': 'PDF', 'size': '2.5 MB', 'downloads': 1500},
                {'name': 'Medical Colleges Ranking', 'type': 'PDF', 'size': '1.8 MB', 'downloads': 1200},
                {'name': 'Commerce Colleges Guide', 'type': 'PDF', 'size': '1.2 MB', 'downloads': 800},
                {'name': 'Arts & Humanities Colleges', 'type': 'PDF', 'size': '1.5 MB', 'downloads': 600}
            ]
        },
        'scholarships': {
            'title': 'Scholarship Information',
            'items': [
                {'name': 'National Scholarship Portal Guide', 'type': 'PDF', 'size': '3.0 MB', 'downloads': 2000},
                {'name': 'Merit Scholarships List 2024', 'type': 'PDF', 'size': '2.2 MB', 'downloads': 1800},
                {'name': 'Minority Scholarships Guide', 'type': 'PDF', 'size': '1.6 MB', 'downloads': 900},
                {'name': 'International Scholarships', 'type': 'PDF', 'size': '2.8 MB', 'downloads': 1100}
            ]
        },
        'career_guides': {
            'title': 'Career Guidance PDFs',
            'items': [
                {'name': 'Complete Career Guide 2024', 'type': 'PDF', 'size': '5.0 MB', 'downloads': 3000},
                {'name': 'Interview Preparation Guide', 'type': 'PDF', 'size': '2.0 MB', 'downloads': 2500},
                {'name': 'Resume Building Templates', 'type': 'ZIP', 'size': '4.5 MB', 'downloads': 1900},
                {'name': 'Soft Skills Development', 'type': 'PDF', 'size': '1.8 MB', 'downloads': 1400}
            ]
        },
        'aptitude_tests': {
            'title': 'Aptitude Test Links',
            'items': [
                {'name': 'Career Aptitude Assessment', 'type': 'Link', 'url': '#',
                 'description': 'Comprehensive career assessment'},
                {'name': 'Personality Test for Career', 'type': 'Link', 'url': '#',
                 'description': 'Know your personality type'},
                {'name': 'Skills Assessment Test', 'type': 'Link', 'url': '#',
                 'description': 'Identify your strengths'},
                {'name': 'Interest Inventory Test', 'type': 'Link', 'url': '#',
                 'description': 'Discover your interests'}
            ]
        }
    }

    context = {'resources': resources}
    return render(request, 'ComplaintMS/resources.html', context)


# Career Aptitude Test View


# Upcoming Seminars View
@login_required
def upcoming_seminars(request):
    """Display upcoming seminars and events"""

    seminars = [
        {
            'id': 1,
            'title': 'Future of Artificial Intelligence Careers',
            'speaker': 'Dr. Rajesh Kumar (IIT Bombay)',
            'date': '2024-06-15',
            'time': '10:00 AM',
            'duration': '2 hours',
            'platform': 'Google Meet',
            'registration_link': '#',
            'description': 'Explore career opportunities in AI and Machine Learning',
            'category': 'Technology',
            'seats_available': 500,
            'registered': 234
        },
        {
            'id': 2,
            'title': 'Medical Career Beyond MBBS',
            'speaker': 'Team of AIIMS Doctors',
            'date': '2024-06-20',
            'time': '2:00 PM',
            'duration': '90 minutes',
            'platform': 'Zoom',
            'registration_link': '#',
            'description': 'Alternative medical career paths and specializations',
            'category': 'Medical',
            'seats_available': 300,
            'registered': 156
        },
        {
            'id': 3,
            'title': 'Digital Marketing Career Workshop',
            'speaker': 'Industry Experts Panel',
            'date': '2024-06-25',
            'time': '4:00 PM',
            'duration': '3 hours',
            'platform': 'Microsoft Teams',
            'registration_link': '#',
            'description': 'Hands-on workshop on digital marketing careers',
            'category': 'Marketing',
            'seats_available': 200,
            'registered': 89
        }
    ]

    context = {'seminars': seminars}
    return render(request, 'ComplaintMS/seminars.html', context)


# Success Stories View
@login_required
def success_stories(request):
    """Display alumni success stories"""

    stories = [
        {
            'id': 1,
            'name': 'Rohit Sharma',
            'current_position': 'Software Engineer at Google',
            'graduation_year': '2020',
            'stream': 'Computer Science Engineering',
            'journey': 'Started from a small town, cracked JEE Advanced, graduated from IIT Delhi, and now working at Google Mountain View.',
            'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
            'linkedin_url': '#',
            'tips': [
                'Consistency is key in preparation',
                'Never give up on your dreams',
                'Practice coding daily',
                'Build projects to showcase skills'
            ],
            'interview_video': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
        },
        {
            'id': 2,
            'name': 'Dr. Priya Mehta',
            'current_position': 'Cardiologist at Apollo Hospital',
            'graduation_year': '2018',
            'stream': 'MBBS, MD Cardiology',
            'journey': 'Cleared NEET in first attempt, completed MBBS from AIIMS Delhi, specialized in Cardiology, now serving patients.',
            'image': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&h=150&fit=crop&crop=face',
            'linkedin_url': '#',
            'tips': [
                'NCERT is your best friend for NEET',
                'Focus on understanding concepts',
                'Time management is crucial',
                'Stay updated with medical advancements'
            ],
            'interview_video': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
        },
        {
            'id': 3,
            'name': 'Ankit Agarwal',
            'current_position': 'IAS Officer (District Collector)',
            'graduation_year': '2019',
            'stream': 'Political Science',
            'journey': 'Graduated in Political Science, prepared for UPSC for 2 years, cleared in second attempt, now serving as District Collector.',
            'image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
            'linkedin_url': '#',
            'tips': [
                'Read newspapers daily',
                'Make concise notes',
                'Practice answer writing',
                'Stay motivated during preparation'
            ],
            'interview_video': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
        },
        {
            'id': 4,
            'name': 'Sneha Gupta',
            'current_position': 'Creative Director at Ogilvy',
            'graduation_year': '2021',
            'stream': 'Mass Communication',
            'journey': 'Studied Mass Communication, started as intern at local agency, worked hard, and now leading creative campaigns at Ogilvy.',
            'image': 'https://images.unsplash.com/photo-1494790108755-2616b612b17c?w=150&h=150&fit=crop&crop=face',
            'linkedin_url': '#',
            'tips': [
                'Build a strong portfolio',
                'Network with industry professionals',
                'Stay creative and innovative',
                'Learn digital marketing tools'
            ],
            'interview_video': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
        }
    ]

    # Filter by stream if requested
    stream_filter = request.GET.get('stream', 'all')
    if stream_filter != 'all':
        stories = [story for story in stories if stream_filter.lower() in story['stream'].lower()]

    context = {
        'stories': stories,
        'selected_stream': stream_filter,
        'streams': ['Engineering', 'Medical', 'Civil Services', 'Arts', 'Commerce', 'Management']
    }
    return render(request, 'ComplaintMS/success_stories.html', context)


# AJAX View for quick career suggestions
@login_required
def quick_career_suggestion(request):
    """AJAX endpoint for quick career suggestions"""
    if request.method == 'POST':
        interests = request.POST.getlist('interests[]')

        career_map = {
            'technology': ['Software Developer', 'Data Scientist', 'Cybersecurity Expert'],
            'medicine': ['Doctor', 'Nurse', 'Medical Researcher'],
            'business': ['MBA', 'Entrepreneur', 'Business Analyst'],
            'arts': ['Graphic Designer', 'Writer', 'Photographer'],
            'law': ['Lawyer', 'Judge', 'Legal Advisor'],
            'teaching': ['Professor', 'School Teacher', 'Corporate Trainer']
        }

        suggestions = []
        for interest in interests:
            if interest in career_map:
                suggestions.extend(career_map[interest])

        return JsonResponse({'suggestions': list(set(suggestions))})

    return JsonResponse({'error': 'Invalid request'})


# Resource Download View
@login_required
def download_resource(request, resource_id):
    """Handle resource downloads (you'll need to implement actual file serving)"""
    # This is a placeholder - implement actual file download logic
    # You can track downloads, check permissions, etc.

    # For now, just redirect to a placeholder
    messages.success(request, f'Resource {resource_id} download started!')
    return redirect('resources')


# Seminar Registration View
@login_required
def register_seminar(request, seminar_id):
    """Handle seminar registration"""
    if request.method == 'POST':
        # Add registration logic here
        # You can store registration in database

        messages.success(request, 'Successfully registered for the seminar!')
        return redirect('seminars')

    return redirect('seminars')