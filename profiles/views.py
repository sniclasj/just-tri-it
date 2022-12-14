from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from .forms import SellerStatusForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import Order

# Create your views here.


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(Profile, athlete=request.user)

    if request.method == 'POST':
        forma = ProfileForm(request.POST, instance=profile)
        if forma.is_valid():
            forma.save()
            messages.success(request, 'Profile updated successfully')

    forma = ProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'forma': forma,
        'orders': orders,
    }

    return render(request, template, context)


def profile_admin(request):

    profiles = Profile.objects.all()

    context = {
        'profiles': profiles,
    }

    """A view to return the profile_admin page"""
    return render(request, 'profiles/profile_admin.html', context)


@login_required
def edit_seller_status(request, profile_id):
    """ Edit a profile's seller status """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == 'POST':
        formb = SellerStatusForm(request.POST, instance=profile)
        if formb.is_valid():
            if request.POST.get("is_seller"):
                is_seller = True
            else:
                is_seller = False
            profile.is_seller = is_seller
            profile.save()
            messages.success(
                request, 'Successfully updated profile seller status!')
            return redirect(reverse('profile_admin'))
        else:
            messages.error(
                request, 'Update error. Please ensure the form is valid.')
    else:
        formb = SellerStatusForm(instance=profile)
        messages.info(request, f'You are editing {profile.athlete}')

    template = 'profiles/edit_seller_status.html'
    context = {
        'formb': formb,
        'profile': profile,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
