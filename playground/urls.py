from django.urls import path
from . import views

# urlpatterns is a list of URL pattern objects that Django matches in order.
# Each entry maps a route to a view or to another URLconf via include().
# Explanation:
#   - Django tests patterns top-to-bottom and stops at the first match.
#   - Use path() for simple, readable routes and re_path() for regex-based routes.
#   - Use include() to delegate URL handling to an app's urls.py.
# Usage examples:
#   path('hello/', views.hello_view, name='hello')         # direct view
#   path('blog/', include('blog.urls'))                    # include app URLconf
#   re_path(r'^items/(?P<pk>\d+)/$', views.item_detail)    # regex route
urlpatterns = [
    path('hello/', views.say_hello),
]