import json
import os

from flask import Blueprint, request

from api.core import create_response, logger
from api.functions.transcript_classifier import BUG, FEATURE, transcript_classifier, TRANSCRIPT_CLASSIFIER_TOOL
from api.managers.linear_manager import LinearManager
from api.managers.openai_manager import OpenAIManager

classifier_routes = Blueprint("classifier_routes", __name__)


@classifier_routes.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    logger.info("Data received: %s", data)
    if not data.get("input_text"):
        msg = "No input text provided for classification."
        logger.info(msg)
        return create_response(status=422, message=msg)

    messages = []
    messages.append({"role": "system",
                     "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    messages.append({"role": "user",
                     "content": f"""Can you help determine if the following customer support conversation transcript needs follow up actions created in linear?
                     ```
                     {data.get("input_text")}
                     ```
                     """})
    openai_manager = OpenAIManager()
    MODEL = 'gpt-3.5-turbo'
    openai_response = openai_manager.call_completion_with_retry(MODEL, messages,
                                                                tools=[TRANSCRIPT_CLASSIFIER_TOOL],
                                                                tool_choice={"type": "function", "function": {
                                                                    "name": "classify_transcript"}}
                                                                ).choices[0].message
    prediction = None
    message = "No Linear ticket created."
    if openai_response.tool_calls[0].function.name == "classify_transcript":
        input_text = json.loads(openai_response.tool_calls[0].function.arguments)["input_text"]
        prediction = transcript_classifier(input_text, openai_manager)
        logger.info(f"Input text was classified as: {prediction}")
        if prediction == FEATURE or prediction == BUG:
            L = LinearManager()
            if prediction == FEATURE:
                label_id = os.getenv("LINEAR_FEATURE_LABEL_UUID")
            else:
                label_id = os.getenv("LINEAR_BUG_LABEL_UUID")
            # TODO: Have GPT create a better issue title and description
            title = f"New {prediction} ticket from customer conversation"
            description = f"""This ticket was created based on the following customer service conversation: 
```
{input_text}
```
"""

            L.create_issue(title,
                           description,
                           label_id,
                           os.getenv("LINEAR_PROJECT_ID"),
                           os.getenv("LINEAR_STATE_ID"),
                           os.getenv("LINEAR_TEAM_ID"),
                           )
            message = f"Linear ticket for {prediction} successfully created"

    return create_response(
        message=message,
        data={"action_taken": prediction},
    )
