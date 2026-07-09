from boto3 import Session


def build_client(profile_name: str, region: str):
    session: Session = Session(profile_name=profile_name)

    return session.client(
        service_name="quicksight",
        region_name=region
    )
