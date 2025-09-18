from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.utils import timezone
from datetime import datetime, time,timedelta,date
from django.contrib.auth.models import User
from .models import Appointment
from django.utils.timezone import now
from django.db.models import Q



# --- Assign consultation time function ---
def assign_consultation_time(appointment):
    # Ensure time_slot is valid
    if not appointment.time_slot:
        appointment.time_slot = 'morning'

    slot_start, slot_end = Appointment.slot_timings()[appointment.time_slot]
    start_datetime = datetime.combine(appointment.appointment_date, slot_start)
    consult_duration = Appointment.consultation_time_map().get(appointment.specialist, 15)

    existing_appointments = Appointment.objects.filter(
        appointment_date=appointment.appointment_date,
        time_slot=appointment.time_slot,
        specialist=appointment.specialist
    ).order_by("consultation_time")

    if existing_appointments.exists():
        last_appointment = existing_appointments.last()
        last_time = last_appointment.consultation_time or slot_start
        next_time = datetime.combine(appointment.appointment_date, last_time) + timedelta(minutes=consult_duration)
    else:
        next_time = start_datetime

    if next_time.time() >= slot_end:
        raise ValueError("No slots available for this doctor in this session")

    appointment.consultation_time = next_time.time()
    return appointment


def home(request):
    if request.method == "POST":
        if not request.session.get('user_id'):
            messages.error(request, "You must login first to book an appointment!")
            return redirect('login_view')

        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = CustomUser.objects.get(id=request.session['user_id'])

            # --- ASSIGN CONSULTATION TIME LOGIC ---
            slot_start, slot_end = Appointment.slot_timings()[appointment.time_slot]
            duration_minutes = Appointment.consultation_time_map()[appointment.specialist]

            # Get existing appointments for same date, slot, and specialist
            existing_appointments = Appointment.objects.filter(
                appointment_date=appointment.appointment_date,
                time_slot=appointment.time_slot,
                specialist=appointment.specialist
            ).order_by('consultation_time')

            if not existing_appointments:
                next_time = slot_start
            else:
                last_appt = existing_appointments.last()
                if last_appt.consultation_time:
                    last_time = last_appt.consultation_time
                else:
                    last_time = slot_start  # fallback if None
                # Add specialist consultation duration
                last_datetime = datetime.combine(date.today(), last_time)
                next_datetime = last_datetime + timedelta(minutes=duration_minutes)
                next_time = next_datetime.time()

            # Check if next_time exceeds slot_end
            if next_time > slot_end:
                messages.error(request, "No more slots available for this time slot.")
                return redirect('appointment_list')

            appointment.consultation_time = next_time
            appointment.save()
            messages.success(request, f"Appointment booked successfully at {next_time.strftime('%H:%M')}!")
            return redirect("appointment_list")
    else:
        form = AppointmentForm()

    return render(request, "index.html", {"form": form, 'show_home': True, 'show_navbar': True})

def staff(request):
    if request.method == "POST":
        if not request.session.get('staff_id'):
            messages.error(request, "You must login first to book an appointment!")
            return redirect('staff_login')

        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = CustomUser.objects.get(id=request.session['user_id'])

            # --- ASSIGN CONSULTATION TIME LOGIC ---
            slot_start, slot_end = Appointment.slot_timings()[appointment.time_slot]
            duration_minutes = Appointment.consultation_time_map()[appointment.specialist]

            # Get existing appointments for same date, slot, and specialist
            existing_appointments = Appointment.objects.filter(
                appointment_date=appointment.appointment_date,
                time_slot=appointment.time_slot,
                specialist=appointment.specialist
            ).order_by('consultation_time')

            if not existing_appointments:
                next_time = slot_start
            else:
                last_appt = existing_appointments.last()
                if last_appt.consultation_time:
                    last_time = last_appt.consultation_time
                else:
                    last_time = slot_start  # fallback if None
                # Add specialist consultation duration
                last_datetime = datetime.combine(date.today(), last_time)
                next_datetime = last_datetime + timedelta(minutes=duration_minutes)
                next_time = next_datetime.time()

            # Check if next_time exceeds slot_end
            if next_time > slot_end:
                messages.error(request, "No more slots available for this time slot.")
                return redirect('today_appointments')

            appointment.consultation_time = next_time
            appointment.save()
            messages.success(request, f"Appointment booked successfully at {next_time.strftime('%H:%M')}!")
            return redirect("today_appointments")
    else:
        form = AppointmentForm()

    return render(request, "index.html", {"form": form, 'show_staff': True, 'show_nav': True})





def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created! Please login.")
            return redirect('login_view')
        else:
            # errors will handled by template popup
            pass
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form,'show_navbar':True})



def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(mobile=mobile)
            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('home')
            else:
                messages.error(request, "Incorrect password!")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found!")
    return render(request, 'login.html', {'form': form,'show_navbar':True})




def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('login_view')



def appointment_list(request):
    if not request.session.get('user_id'):
        messages.error(request, "You must login first to view appointments!")
        return redirect('login_view')

    appointments = Appointment.objects.filter(
        patient_id=request.session['user_id']
    ).order_by('-appointment_date', '-created_at')

    now = timezone.localtime()

    for appt in appointments:
        # Ensure time_slot exists
        if not appt.time_slot:
            appt.cancellable = False
            continue

        # Get slot end time from model method
        slot_start, slot_end = Appointment.slot_timings().get(appt.time_slot, (None, None))
        if not slot_end:
            appt.cancellable = False
            continue

        # Cutoff datetime is slot end
        cutoff = timezone.make_aware(
            datetime.combine(appt.appointment_date, slot_end),
            timezone.get_current_timezone()
        )
        appt.cancellable = now < cutoff

    return render(request, "appointment_list.html", {
        "appointments": appointments,
        "show_navbar": True,
        "specialist_choices": Appointment.DOCTOR_CHOICES
    })



def cancel_appointment(request, appointment_id):
    if not request.session.get('user_id'):
        messages.error(request, "You must login first to cancel appointments!")
        return redirect('login_view')

    appointment = get_object_or_404(Appointment, id=appointment_id, patient_id=request.session['user_id'])

    now = timezone.localtime()
    if appointment.time_slot == "Morning":
        cutoff_time = time(8, 0)
    else:
        cutoff_time = time(17, 0)

    cutoff = timezone.make_aware(
        datetime.combine(appointment.appointment_date, cutoff_time),
        timezone.get_current_timezone()
    )

    if now < cutoff:
        appointment.delete()
        messages.success(request, "Appointment cancelled successfully.")
    else:
        messages.error(request, "You cannot cancel past appointments.")

    return redirect('appointment_list')






def appointment_records(request):
    search = request.GET.get('search', '').strip()
    specialist = request.GET.get('specialist', '').strip()
    appointments = Appointment.objects.all().order_by('-created_at')

    if search:
        appointments = appointments.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search)
        )

    if specialist:
        appointments = appointments.filter(specialist=specialist)

    context = {
        "appointments": appointments,
        "search": search,
        "specialist": specialist,
        "specialist_choices": Appointment.DOCTOR_CHOICES,  # 👈 for dropdown
        "show_nav": True,
    }
    return render(request, "appointment_records.html", context)





# --- Today appointments view ---
def today_appointments(request):
    if not request.session.get('staff_id'):
        messages.error(request, "You must login first to book an appointment!")
        return redirect('staff_login')

    # POST: Add new appointment
    if request.method == "POST" and "name" in request.POST:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.staff = StaffUser.objects.get(id=request.session['staff_id'])
            try:
                appointment = assign_consultation_time(appointment)
                appointment.save()
                messages.success(
                    request,
                    f"Appointment booked successfully! Consultation time: {appointment.consultation_time.strftime('%I:%M %p')}"
                )
                return redirect("today_appointments")
            except ValueError as e:
                messages.error(request, str(e))
                return redirect("today_appointments")
    else:
        form = AppointmentForm()

    # GET: Filter & Search
    today = now().date()
    search = request.GET.get('search', '')
    specialist = request.GET.get('specialist', '')

    appointments = Appointment.objects.filter(appointment_date=today, status="pending")
    if search:
        appointments = appointments.filter(Q(name__icontains=search) | Q(phone__icontains=search))
    if specialist:
        appointments = appointments.filter(specialist=specialist)

    # POST: Update visit status
    if request.method == "POST" and "appointment_id" in request.POST:
        appointment_id = request.POST.get("appointment_id")
        action = request.POST.get("action") 
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = action
        appointment.save()
        return redirect("today_appointments")

    return render(request, "today_appointment.html", {
        "appointments": appointments,
        "search": search,
        "specialist": specialist,
        "specialist_choices": Appointment.DOCTOR_CHOICES,
        "form": form,
        "show_nav": True,
    })


def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.set_password(form.cleaned_data['password'])  
            staff.save()
            messages.success(request, "Account created! Please login.")
            return redirect('staff_login')
        else:
            # errors will handled by template popup
            pass
    else:
        form = StaffRegisterForm()
    return render(request, 'staff_register.html', {'form': form,'show_nav':True})


def staff_login(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        try:
            staff = StaffUser.objects.get(mobile=mobile)
            if staff.check_password(password):
                request.session['staff_id'] = staff.id
                request.session['staff_name'] = staff.name
                return redirect('today_appointments')
            else:
                messages.error(request, "Incorrect password!")
        except StaffUser.DoesNotExist:
            messages.error(request, "Staff not found!")

    form = StaffLoginForm()
    return render(request, "staff_login.html", {"form": form,'show_nav':True})


def staff_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('staff_login')



def staff_account(request): 
    staff_id = request.session.get('staff_id')
    if not staff_id:
        messages.error(request, "Please Login!")
        return redirect('staff_login')

    staff = StaffUser.objects.get(id=staff_id)

    if request.method == 'POST':
        # get values from form
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        # update staff object
        staff.name = name
        staff.mobile = mobile
        if password:   
            staff.set_password(password)
        staff.save()
        messages.success(request, "Updated successfully!")
        return redirect('staff_account')

    return render(request, 'staff_account.html', {'staff': staff, 'show_nav': True})




def user_account(request): 
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please Login!")
        return redirect('user_login')

    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        # get values from form
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        # update staff object
        user.name = name
        user.mobile = mobile
        if password:  
            user.set_password(password)
        user.save()
        messages.success(request, "Updated successfully!")
        return redirect('user_account')
    
    return render(request, 'user_account.html', {'user': user, 'show_navbar': True})