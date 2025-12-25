from celery import shared_task
import time
import uuid

from .models import ResearchSession, ResearchStep, UploadedDocument, CostUsage


@shared_task
def run_research_task(session_id, parent_summary=None):
    session = ResearchSession.objects.get(id=session_id)

    # Mark session as running
    session.status = "RUNNING"

    # Generate a trace_id manually (LangSmith will still trace automatically)
    session.trace_id = str(uuid.uuid4())
    session.save()

    total_tokens = 0

    # If continuing from parent research
    if parent_summary:
        ResearchStep.objects.create(
            session=session,
            step_name="Building on previous research",
            output=parent_summary
        )
        total_tokens += 5

    # STEP 1 — Handle uploaded documents
    documents = UploadedDocument.objects.filter(session=session)

    if documents.exists():
        ResearchStep.objects.create(
            session=session,
            step_name="Reading uploaded documents",
            output=f"{documents.count()} document(s) found"
        )
        total_tokens += 10

        for doc in documents:
            ResearchStep.objects.create(
                session=session,
                step_name="Extracting content",
                output=f"Read file: {doc.file.name}"
            )
            total_tokens += 10
            time.sleep(1)
    else:
        ResearchStep.objects.create(
            session=session,
            step_name="No documents found",
            output="Proceeding without documents"
        )
        total_tokens += 5

    # STEP 2 — Simulated research steps
    steps = [
        "Understanding the research question",
        "Identifying key topics",
        "Analyzing information",
        "Summarizing findings",
        "Finalizing response",
    ]

    for step in steps:
        ResearchStep.objects.create(
            session=session,
            step_name=step,
            output=f"Completed: {step}"
        )
        total_tokens += 10
        time.sleep(1)

    # Save cost
    cost_usd = total_tokens * 0.0005
    CostUsage.objects.update_or_create(
        session=session,
        defaults={
            "total_tokens": total_tokens,
            "total_cost_usd": cost_usd,
        },
    )

    # Mark session completed
    session.status = "COMPLETED"
    session.save()
