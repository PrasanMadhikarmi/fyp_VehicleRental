import base64
from django.shortcuts import redirect, render

from accounts.models import VehicleRegistration
from accounts.models import UserVerificationStatus
from datetime import datetime
from services.forms import BookingForm
from django.utils import timezone

from services.models import CustomerPayment, bookInstantly
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import request
import requests as req
import xml.etree.ElementTree as ET

# Create your views here.


def index(request):
    return render(request, 'services/services.html')


def vehicleDisplay(request):
    context = {}
    if request.method == 'POST':
        location = request.POST.get('location')
        from_date = request.POST.get('from')
        until_date = request.POST.get('until')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        user_vehicles = VehicleRegistration.objects.filter(
            isVerified=True, available=True)

        if user_vehicles.exists():
            # Filter vehicles based on form data
            user_vehicles = user_vehicles.filter(
                location__icontains=location,
                category=category,
                subcategory=subcategory
            )

            print(user_vehicles)

            context = {
                'user_vehicles': user_vehicles,
                'category': category
            }
        else:
            context = {
                'no_results': True
            }

        return render(request, "services/display.html", context)

    return render(request, "services/display.html", context)


def detail(request, car_id):
    car_pk = VehicleRegistration.objects.get(pk=car_id)
    if request.user.is_authenticated:
        # User is logged in, fetch UserVerificationStatus
        user_verification_status = UserVerificationStatus.objects.get(
            user=request.user)
    else:
        # User is not logged in, set a default value
        user_verification_status = {}

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Set additional fields before saving the form
            form.instance.user_id = request.user  # Assign the current user
            vehicle_instance = get_object_or_404(
                VehicleRegistration, pk=car_id)
            form.instance.vehicle_id = vehicle_instance  # Assign the vehicle
            form.save()

            messages.success(
                request, 'Booking successful. We will send you a confirmation email.')
            booking_instance = form.save()  # Assuming you're using a ModelForm

            print(
                f"Pick Date: {booking_instance.pickDate}, Pick Time: {booking_instance.pickTime}")
            print(
                f"Drop Date: {booking_instance.dropDate}, Drop Time: {booking_instance.dropTime}")

            pick_datetime = datetime.combine(
                booking_instance.pickDate, booking_instance.pickTime)
            drop_datetime = datetime.combine(
                booking_instance.dropDate, booking_instance.dropTime)

            print(pick_datetime)
            print(drop_datetime)

            # Calculate duration using timedelta
            duration = drop_datetime - pick_datetime
            duration_hours = duration.total_seconds() // 3600
            print(duration_hours)

            # Calculate total price based on the price per day
            price_per_day = booking_instance.vehicle_id.price
            total_price = (duration_hours // 24) * \
                price_per_day  # Assuming a day has 24 hours

            # Save the duration and total price to the booking instance
            booking_instance.booking_duration = duration_hours
            booking_instance.total_price = total_price
            print(f"Duration Hours: {duration_hours}")
            print(f"Price Per Day: {price_per_day}")
            print(f"Total Price: {total_price}")

            # Save the updated booking instance
            booking_instance.save()
            # Get the booking ID
            # Adjust this based on your actual model structure
            booking_id = booking_instance.id

            send_confirmation_email(
                email=booking_instance.user_id.email,
                booking_id=booking_id,
                subject='Booking Confirmation',
                booking_details=booking_instance  # Pass the actual booking instance
            )
            send_confirmation_email(
                email=booking_instance.vehicle_id.user.email,
                booking_id=booking_id,
                subject='New Booking Received',
                booking_details=booking_instance  # Pass the actual booking instance
            )
        else:
            print("Form errors:", form.errors)
    else:
        form = BookingForm()

    context = {
        'car_pk': car_pk,
        'form': form,
        'check_verify': user_verification_status
    }

    return render(request, 'services/detail.html', context)


def send_confirmation_email(email, booking_id, subject, booking_details):
    to_email = email  # Assuming your form has an 'email' field

    if subject == 'Booking Confirmation':
        # Modify the email message to include booking details and ID
        email_message = f'Thank you for booking! Please make the payment through the my booking page.\n\nBooking ID: {booking_id}\nName: {booking_details.name}\nEmail: {booking_details.email}\nPhone: {booking_details.number}\nPickup Date: {booking_details.pickDate}\nPickup Time: {booking_details.pickTime}\nDrop Off Date: {booking_details.dropDate}\nDrop Off Time: {booking_details.dropTime}'
    elif subject == 'New Booking Received':
        email_message = f'You have received a new booking! Please accept and request the payment through the my booking request page.\n\nBooking ID: {booking_id}\nName: {booking_details.name}\nEmail: {booking_details.email}\nPhone: {booking_details.number}\nPickup Date: {booking_details.pickDate}\nPickup Time: {booking_details.pickTime}\nDrop Off Date: {booking_details.dropDate}\nDrop Off Time: {booking_details.dropTime}'
    elif subject == 'Payment received':
        email_message = f'You have received payment for booking Id {booking_id}! Please check the awaiting balance in your accounts page.\n\nBooking ID: {booking_id}\nName: {booking_details.name}\nEmail: {booking_details.email}\nPhone: {booking_details.number}\nPickup Date: {booking_details.pickDate}\nPickup Time: {booking_details.pickTime}\nDrop Off Date: {booking_details.dropDate}\nDrop Off Time: {booking_details.dropTime}'

    send_mail(subject, email_message, 'eliterental.helpline@gmail.com',
              [to_email], fail_silently=False)


def booking(request):
    current_user = request.user
    history = bookInstantly.objects.filter(user_id_id=current_user.id)

    context = {
        'history': history
    }
    return render(request, 'services/book.html', context)


def booking_request(request):
    history = bookInstantly.objects.filter(vehicle_id__user=request.user)
    custPay = CustomerPayment.objects.filter(
        booking_id__vehicle_id__user=request.user)

    # Calculate the fees for each payment in the view
    fees_list = []
    total_fees = 0
    total_pay = 0
    for payment in custPay:
        fees = payment.total_paid_amount - payment.vendor_payment
        total_pay += payment.vendor_payment
        fees_list.append({
            'booking_id': payment.booking_id_id,
            'fees': fees
        })
        total_fees += fees

    context = {
        'history': history,
        'custPay': custPay,
        'fees_list': fees_list,
        'total_fees': total_fees,
        'total_pay': total_pay
    }
    return render(request, 'services/book_request.html', context)


def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(bookInstantly, id=booking_id)
    # Check if the booking status is "Processing" before allowing cancellation
    if booking.status == "Processing" or booking.status == 'Accepted':
        # Update the booking status to "Cancelled"
        booking.status = "Cancelled"
        booking.save()
        send_cancel_email(booking.vehicle_id.user.email,
                          booking.id, 'Booking Cancelled', booking)
        return redirect('services:booking')


def cancel_booking_by_vendor(request, booking_id):
    booking = get_object_or_404(bookInstantly, id=booking_id)

    # Update the booking status to "Cancelled"
    booking.status = "Cancelled"
    booking.save()

    vehicleInstance = VehicleRegistration.objects.get(id=booking.vehicle_id.id)
    vehicleInstance.available = True
    vehicleInstance.save()

    send_cancel_email(booking.email, booking.id,
                      f'Booking Cancelled by Vendor for booking Id {booking_id}', booking)
    return redirect('services:booking')


# Assuming your form has an 'email' field
def send_cancel_email(toemail, booking_id, subject, booking_details):
    email = toemail
    # Modify the email message to include booking details and ID
    email_message = f'Booking ID: {booking_id} has been cancelled! \nName: {booking_details.name}\nEmail: {booking_details.email}\nPhone: {booking_details.number}\nPickup Date: {booking_details.pickDate}\nPickup Time: {booking_details.pickTime}\nDrop Off Date: {booking_details.dropDate}\nDrop Off Time: {booking_details.dropTime}'

    send_mail(subject, email_message, 'eliterental.helpline@gmail.com',
              [email], fail_silently=False)


def payment_success(request, booking_id):

    bookInstance = bookInstantly.objects.get(id=booking_id)
    bookInstance.status = "Paid"
    bookInstance.save()

    if bookInstance.vehicle_id.category == 'car':
        commission_percentage = 10
    elif bookInstance.vehicle_id.category == 'bike':
        commission_percentage = 8
    elif bookInstance.vehicle_id.category == 'bicycle':
        commission_percentage = 5
    else:
        commission_percentage = 0

    commission = (bookInstance.total_price * commission_percentage) / 100
    vendor_payment = bookInstance.total_price - commission

    payment_instance = CustomerPayment.objects.create(
        user_id=request.user,
        booking_id=bookInstance,
        payment_date=timezone.now(),
        total_paid_amount=bookInstance.total_price,
        payment_method='Esewa',
        commission_per=commission_percentage,
        vendor_payment=vendor_payment,
    )

    payment_instance.save()

    send_confirmation_email(
        email=bookInstance.vehicle_id.user.email,
        booking_id=booking_id,
        subject=f'Payment received',
        booking_details=bookInstance  # Pass the actual booking instance
    )

    return render(request, 'services/payment_success.htm')


def payment_failed(request):
    return render(request, 'services/failed_payment.htm')

# accepts


def request_payment(request, booking_id):
    bookInstance = bookInstantly.objects.get(id=booking_id)
    bookInstance.status = "Accepted"
    bookInstance.save()

    vehicleInstance = VehicleRegistration.objects.get(
        id=bookInstance.vehicle_id.id)
    vehicleInstance.available = False
    vehicleInstance.save()

    send_payment_request_email(bookInstance.user_id.email, booking_id,
                               f'Payment Requested for Booking Id {booking_id}', bookInstance)

    return render(request, 'services/requested_payment.html')


def send_payment_request_email(email, booking_id, subject, booking_details):
    to_email = email  # Assuming your form has an 'email' field

    # Modify the email message to include booking details and ID
    email_message = f'Booking ID: {booking_id} has requested payment! \nName: {booking_details.name}\nEmail: {booking_details.email}\nPhone: {booking_details.number}\nPickup Date: {booking_details.pickDate}\nPickup Time: {booking_details.pickTime}\nDrop Off Date: {booking_details.dropDate}\nDrop Off Time: {booking_details.dropTime}'

    send_mail(subject, email_message, 'eliterental.helpline@gmail.com',
              [to_email], fail_silently=False)
