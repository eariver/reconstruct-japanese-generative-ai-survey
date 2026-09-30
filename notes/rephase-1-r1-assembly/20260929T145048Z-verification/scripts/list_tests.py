import re, os
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
for path in ["tests/test_survey_weekly_mechanical_refresh_v2.py", "tests/test_survey_publication_revalidation_v2.py", "tests/test_survey_reader_surface_gate_v2.py", "tests/test_survey_gate_cli_persisted_review_v2.py"]:
    fp = os.path.join(DST, path)
    with open(fp) as f:
        content = f.read()
    names = re.findall(r"def (test_[A-Za-z0-9_]+)", content)
    print(path, len(names))
    for n in names:
        print("  ", n)
