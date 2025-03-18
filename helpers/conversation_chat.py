from langchain.chat_models.openai import ChatOpenAI as OpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain

from constants import OPENAI_API_KEY, SYSTEM_PROMPT


def get_conversation_chain(vector_store):
    """Create ConversationalRetrievalChain for chatbot."""
    llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=ChatMessageHistory(),
        return_messages=True,
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return chain
