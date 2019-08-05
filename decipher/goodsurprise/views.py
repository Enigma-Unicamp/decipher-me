from django.shortcuts import render, redirect
from django.http import HttpResponse  
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

CHALLENGE_KEY = 'secomp{C0okieM0nst3r}'

class IndexView(TemplateView):

    # Redirect to the home page
    def dispatch(self, request, *args, **kwargs):
        return redirect('goodsurprise:login')


@method_decorator(csrf_exempt, name='dispatch')
class GoodSurpriseView(TemplateView):
    template_name = 'goodsurprise/login.html'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('id*127', 0)
        return response

    def post(self, request):
        try:
            if int(request.COOKIES['id*127']) == 30*127:
                return render(request, self.template_name, 
                              {'message': f'Here, have a cookie: {CHALLENGE_KEY}'})
        except:
            pass

        return render(request, self.template_name, {'error': 'Invalid username or password'},
                      status=403)
