from .models import Criterion, Rubric

DEFAULT_RUBRIC = Rubric(
    name="general_llm_response_quality", version="1.0",
    criteria=(
        Criterion("correctness", 0.35, "Factual and technical correctness; no material errors."),
        Criterion("instruction_adherence", 0.25, "Follows explicit user constraints and requested format."),
        Criterion("completeness", 0.15, "Addresses the important parts of the request without critical omissions."),
        Criterion("relevance", 0.15, "Stays focused on information needed to answer the request."),
        Criterion("clarity", 0.10, "Communicates in a concise, structured, easy-to-act-on way."),
    ),
)
DEFAULT_RUBRIC.validate()
