from django.conf.urls import url
from .views import idea, idea_create
from .views import idea_register_candidate, idea_register, idea_unregister, idea_unregister_candidate
from .views import idea_candidates, idea_participants, idea_candidate_approval
from .views import idea_completed, idea_open, idea_rate, idea_scores_criteria
from .views import idea_validate, idea_draft_list


urlpatterns = [
    url(r'^(?P<idea_id>\d+)/$', idea, name='idea'),
    url(r'^(?P<idea_id>\d+)/completed/$', idea_completed, name='idea_completed'),
    url(r'^(?P<idea_id>\d+)/open/$', idea_open, name='idea_open'),
    url(r'^(?P<idea_id>\d+)/register/$', idea_register, name='idea_register'),
    url(r'^(?P<idea_id>\d+)/register/candidate/$', idea_register_candidate, name='idea_register_candidate'),
    url(r'^(?P<idea_id>\d+)/unregister/$', idea_unregister, name='idea_unregister'),
    url(r'^(?P<idea_id>\d+)/unregister/candidate/$', idea_unregister_candidate, name='idea_unregister_candidate'),
    url(r'^(?P<idea_id>\d+)/validation/switch/$', idea_validate, name='idea_validate'),
    url(r'^(?P<idea_id>\d+)/candidates/$', idea_candidates, name='idea_candidates'),
    url(r'^(?P<idea_id>\d+)/candidate/approval/switch/$', idea_candidate_approval, name='idea_candidate_approval'),
    url(r'^(?P<idea_id>\d+)/participants/$', idea_participants, name='idea_participants'),
    url(r'^(?P<idea_id>\d+)/rate/$', idea_rate, name='idea_rate'),
    # url(r'^(?P<idea_id>\d+)/vote/$', idea_vote, name='idea_vote'),
    url(r'^create/$', idea_create, name='idea_create'),
    url(r'^rate/category/list/$', idea_scores_criteria, name='idea_scores_criteria'),
    url(r'^draft/event/(?P<event_id>\d+)/list/$', idea_draft_list, name='idea_draft_list'),
]
