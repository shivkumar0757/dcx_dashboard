from cryptography.fernet import Fernet
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UpdateTokenForm
from .models import UserProfile
from .services.coindcx_api_price_fetcher import  CoinDCXAPIPriceFetcher
from .service import fetch_positions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PositionSerializer
import logging
from decouple import config

from .services.coindcx_api_price_fetcher import CoinDCXAPIPriceFetcher

logger = logging.getLogger(__name__)
ENCRYPTION_KEY = config('ENCRYPTION_KEY')
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            api_key = form.cleaned_data.get('api_key')
            api_secret = form.cleaned_data.get('api_secret')
            user_profile = UserProfile(user=user)
            fernet = Fernet(ENCRYPTION_KEY)
            user_profile.encrypted_api_key = fernet.encrypt(api_key.encode())
            user_profile.encrypted_api_secret = fernet.encrypt(api_secret.encode())
            user_profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'positions/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'positions/login.html', {'form': form})

# @login_required
# def dashboard_view(request):
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         # Redirect to a page where the user can add their API key and secret
#         return redirect('update-token')
#     context = {
#         'username': request.user.username,
#     }
#     return render(request, 'positions/dashboard.html', context)

@login_required
def update_token_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UpdateTokenForm(request.POST)
        if form.is_valid():
            api_key = form.cleaned_data.get('api_key')
            api_secret = form.cleaned_data.get('api_secret')
            user_profile.set_api_key(api_key)
            user_profile.set_api_secret(api_secret)
            user_profile.save()
            return redirect('dashboard')
    else:
        form = UpdateTokenForm(initial={
            'api_key': user_profile.get_api_key(),
            'api_secret': user_profile.get_api_secret()
        })
    return render(request, 'positions/update_token.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class PositionListView(APIView):
    def get(self, request, format=None):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            api_key = user_profile.get_api_key()
            logger.info('Keys reveived')
            api_secret = user_profile.get_api_secret()
            positions = fetch_positions(api_key, api_secret)
            positions = [pos for pos in positions if pos['active_pos'] != 0]
            # print(positions)
            logger.info('Positions fetched')
            # Account information
            total_position_size = 0
            total_pnl = 0
            total_invested = 0
            current_account_balance = 0
            for position in positions:

                pair = position['pair']
                position['mark_price'] = CoinDCXAPIPriceFetcher.get_price(pair=pair)

                # print(position['pair'])
                position['updated_at'] = position['updated_at'] // 1000  # Convert to seconds
                pnl = (position['mark_price'] - position['avg_price']) * position['active_pos']
                position['pnl'] = pnl
                if int(position['locked_margin']) != 0:
                    roe = (pnl / position['locked_margin']) * 100
                else:
                    roe = 0
                position['roe'] = roe
                # Account Information
                total_position_size += position['active_pos'] * position['mark_price']
                total_pnl += pnl
                total_invested += position['locked_margin']
                current_account_balance = total_invested + total_pnl
            logger.info('Positions processed')
            serializer = PositionSerializer(positions, many=True)
            print(serializer.data)
            return Response({'positions': serializer.data, 'total_position_size': total_position_size,
                             'total_pnl': total_pnl, 'total_invested':total_invested, 'current_account_balance':current_account_balance }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in PositionListView: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def dashboard_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Redirect to a page where the user can add their API key and secret
        return redirect('update-token')
    context = {
        'username': request.user.username,
    }
    return render(request, 'positions/dashboard.html', context)