import versso as v

my_project_name = "web-analytics"
quick_client = v.get_qs_client_from_session("default", "us-east-1")
prod_analysis = v.get_prod_analysis_payload()

response = v.analysis_describe(analysis_payload=prod_analysis, quicksight_client=quick_client)

print(response)
