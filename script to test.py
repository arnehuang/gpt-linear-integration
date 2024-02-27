import os

import dotenv

from api.functions.transcript_classifier import transcript_classifier
from api.managers.linear_manager import LinearManager
from api.managers.openai_manager import OpenAIManager

dotenv.load_dotenv()

feature_input_text = "you should make the button red because it's hard to see when I use dark mode"
bug_input_text = "I can't press submit because the page never validates my address"

print(transcript_classifier(feature_input_text, OpenAIManager()))
print(transcript_classifier(bug_input_text, OpenAIManager()))

L = LinearManager()
projects = L.projects()
print(L.states(), L.teams(), projects)
prediction = "bug"
title = f"New {prediction} ticket from customer conversation"
description = f"""This ticket was created based on the following customer service conversation: 
    ```
    {bug_input_text}
    ```
"""
ret = L.create_issue(title,
                     description,
                     os.getenv("LINEAR_BUG_LABEL_UUID"),
                     os.getenv("LINEAR_PROJECT_ID"),
                     os.getenv("LINEAR_STATE_ID"),
                     os.getenv("LINEAR_TEAM_ID"),
                     )
