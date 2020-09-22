from django.urls import path
from .views import (
	send_friend_request, 
	remove_friend,
	accept_friend_request,
	cancel_friend_request,
	cancel_sent_friend_request
	)

app_name = "relationships"
urlpatterns = [
    path("~freq/<uuid:id>/", send_friend_request, name="send_freq"),
	path("~frndremove/<uuid:id>/", cancel_sent_friend_request, name="cancel_sent_freq"),
	path("~frndremove/<uuid:id>/", remove_friend, name="remove_frnd"),
	path("~frndaccept/<uuid:id>/", accept_friend_request, name="accept_frnd"),
	path("~frndcancel/<uuid:id>/", cancel_friend_request, name="cancel_frnd"),
	#path("~frndlist/<uuid:id>/", relationship_list_view, name="relation_list"),
    
]