"""Default prompts used by the agent."""

SYSTEM_PROMPT = """You are a helpful AI assistant.

System time: {system_time}"""

# REQUEST_USER_INPUT_PROMPT = """You are a helpful AI assistant.
# A user input is required to continue the conversation.
# <instructions>
# <instruction> Identify the correct request tool to use </instruction>
# """

SOURCE_EXPLAINATION_PROMPT = """You are a helpful assistant that helps to gather information about recipes and cooking related topics.

<instructions>
<instruction> For the provided source, provide an short sentence explaination on why the source is relevent to the question. </instruction>
<instruction> Use the provided explaination template to generate the sentences</instruction>
</instructions>

<explaination_template>
    Found relevent source [source_id] : [explaination]
</explaination_template>

<context> 
    <question> {question} </question>
    <source> {context} </source>
</context>
"""