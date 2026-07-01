from boto3 import Session


def build_client_from_profile(region: str, profile_name: str):
    qs_session = Session(profile_name=profile_name)
    qs_client = qs_session.client(service_name="quicksight", region_name=region)

    return qs_client