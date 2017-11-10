"""Dashborad views."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from scheduler.models import BookingRecord, Session
from account.models import User, Student
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail

# def MybookingsView(request):
#    #model = scheduler
#    record = student.BookingRecord_set.all
#    #template_name = 'my_bookings.html'
#    #context_object_name = 'mybookings'
#    return render(request, 'my_bookings.html', {'record': record})

class MybookingsView(generic.ListView):
    model = BookingRecord
    template_name = 'my_bookings.html'
    context_object_name = 'my_booking_records'

    def get_context_data(self, **kwargs):
        context = super(MybookingsView, self).get_context_data(**kwargs)
        #print datetime.now()
        if self.request.session['username'] is None:
            context['records'] = None
            return context
        else:
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
            usr = get_object_or_404(Student, user=user)
            context['records'] = usr.bookingrecord_set.all()
            #print usr.wallet_balance
            return context

    def post(self, request, **kwargs):
        print(request)
        bkRecord_id = self.request.POST.get('booking_id', '')
        bkrc = BookingRecord.objects.filter(id=bkRecord_id).first()
        sess = Session.objects.get(bookingrecord=bkrc)
        one_day_from_now = timezone.now() + timedelta(hours=24)
        if one_day_from_now < sess.start_time:
            sess.status = Session.BOOKABLE
            sess.save()  # save is needed for functioning  - Jiayao
            refund = bkrc.transaction.amount
            usrn = self.request.session['username']
            user = User.objects.get(username=usrn)
            usr = get_object_or_404(Student, user=user)
            #print usr.wallet_balance
            usr.wallet_balance += refund
            usr.save()
            #print "refund!" + str(refund)
            #print usr.wallet_balance
            bkrc.status = BookingRecord.CANCELED
            #print bkrc.status
            bkrc.save()
            tut = bkrc.tutor
            send_mail('Session Canceled', 'Please check on Tutoria, your session has been canceled.', 'nonereplay@hola-inc.top', [usr.email, tut.email], False)
            return redirect('dashboard/mybookings/')
        else:
            return HttpResponse("This session is within 24 hours and can't be canceled!")
