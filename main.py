from versso import AnalysisPayload, pull, update, promote # type: ignore[import-not-found]

beta_analysis_id = "ef425854-09e9-40f7-985d-6d6ad56d969f"
prod_analysis_id = "5c2f585e-09c4-446a-93eb-22977277e1db"
aws_account_id = "679432970382"


beta_analysis = AnalysisPayload(id=beta_analysis_id, aws_account_id=aws_account_id, name="beta-analysis")
prod_analysis = AnalysisPayload(id=prod_analysis_id, aws_account_id=aws_account_id, name="prod-analysis")

response = promote(beta=beta_analysis, prod=prod_analysis)

print(response)
