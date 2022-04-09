from django.urls import reverse



def test_view_add_item_for_user(client, db):
    url = reverse('home:add_item')

    response = client.get(url)

    assert response.status_code == 200


