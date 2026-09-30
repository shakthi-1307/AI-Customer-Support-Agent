def extract_brand_responses(conversation):
    responses = []

    for line in conversation.split("\n"):
        if line.startswith("AMAZONHELP:"):
            response = line.replace("AMAZONHELP:", "", 1).strip()

            if response:
                responses.append(response)

    return responses


def build_context(results):
    context = []

    for i, result in enumerate(results, 1):
        responses = extract_brand_responses(
            result["conversation"]
        )

        context.append(
            f"Example {i}:\n"
            f"Similarity: {result['score']:.3f}\n"
            f"Customer conversation:\n"
            f"{result['conversation']}\n"
            f"Historical AmazonHelp responses:\n"
            + "\n".join(
                f"- {response}" for response in responses
            )
        )

    return "\n\n".join(context)