from versso.aws.quicksight.account.factory import build_client_from_profile


def get_qs_client_from_session(profile_name: str, region: str):
    return build_client_from_profile(profile_name=profile_name,
                                     region=region)
