from versso.quicksight.dataset._payload import DatasetPayload
from versso.quicksight.setup._context import Context
from versso.quicksight.dataset._service import Dataset


def build_dataset(dataset_payload: DatasetPayload, context: Context, client) -> Dataset:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :return: A populated AnalysisPayload data structure instance.
    """
    return Dataset(
        dataset_payload=dataset_payload,
        context=context,
        quicksight_client=client
    )
