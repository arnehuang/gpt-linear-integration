FEATURE = 'feature'
BUG = 'bug'
NEITHER = 'neither'

TRANSCRIPT_CLASSIFIER_TOOL = {
    "type": "function",
    "function": {
        "name": "classify_transcript",
        "description": "Classifies a customer support transcript as either 'feature', 'bug' or 'neither'",
        "parameters": {
            "type": "object",
            "properties": {
                "input_text": {
                    "type": "string",
                    "description": "The customer support transcript as a string",
                },
            },
            "required": ["input_text"],
        },
    }
}


def transcript_classifier(input_text, openai_manager):
    """
    Given an input text string of a customer service transcript, returns a classification of what to add to linear
    :param input_text: string of a customer service transcript
    :return: 'feature', 'bug', or 'neither'
    """

    MODEL = "gpt-3.5-turbo"
    SYSTEM_PROMPT = f"""You are a classifier that predicts if a customer service transcript should result in a feature request, a bug report or neither.
    return only one of the following: ['{FEATURE}', '{BUG}' or '{NEITHER}']
    """

    # TODO: Can return probabilities instead of pure classification and only create tickets if the probabliity exceeds a threshold

    # call the openai api
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": input_text},
    ]
    openai_response = openai_manager.call_completion_with_retry(MODEL, messages)
    classification = openai_response.choices[0].message.content
    return classification
