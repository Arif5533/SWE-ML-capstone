from app.services.summarizer import analyze_meeting

SAMPLE = \"\"\"[00:00] Alice: Let's kick off. Q3 goal is to launch the beta on Oct 1.
[00:10] Bob: I'll finalize the onboarding screens by Friday.
[00:20] Carol: We still need legal to review the new ToS.
[00:30] Bob: I can ping Legal today. Also, set up a retrospective for the last sprint.
[00:45] Alice: Assign the retro to Carol, due next Wednesday.
[01:00] Carol: Noted. I'll prepare the agenda and invite the team.
[01:15] Alice: Risks: infra cost spikes. Action: Bob to evaluate reserved instances.
[01:30] Bob: Got it, I will run a cost analysis and share by Monday.
\"\"\"

def test_pipeline_runs():
    summary, tasks = analyze_meeting(SAMPLE)
    assert isinstance(summary, str) and len(summary) > 0
    assert isinstance(tasks, list) and len(tasks) >= 1
