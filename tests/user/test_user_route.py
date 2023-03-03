from src.database.entity.entities import EntitiesRbac

user = [
    {
        "num_seqe_usua": 1,
        "dat_hor_atui": "2023-02-27T09:22:29",
        "nom_orig_usua": "GO",
        "idef_user": "PHRaulino",
        "groups": [],
        "policies": [],
    }
]


def test_user_route(client, rds_credentials_mock):
    entities = EntitiesRbac()

    print(entities)

    response = client.get("users")

    assert response.json() == user
