from langchain_core.tools import Tool

class PDFChatNode:
    def __init__(self, llm, tools=None):
        self.llm = llm
        self.tools = tools or []

    def process(self, state):
        user_message = state["messages"][-1] if state["messages"] else ""
        pdf_content = state.get("pdf_content", "")
        prompt = (
            f"You are an assistant. The user uploaded a PDF. "
            f"PDF content:\n{pdf_content[:2000]}\n"
            f"User question: {user_message}"
        )
        # Multi-tooling: If tools are available, bind them
        if self.tools:
            llm_with_tools = self.llm.bind_tools(self.tools)
            answer = llm_with_tools.invoke([{"role": "user", "content": prompt}])
        else:
            answer = self.llm.invoke([{"role": "user", "content": prompt}])
        state["answer"] = answer.content
        return state

    def summarize(self, state):
        pdf_content = state.get("pdf_content", "")
        prompt = (
            f"Summarize the following PDF content in concise bullet points:\n{pdf_content[:2000]}"
        )
        if self.tools:
            llm_with_tools = self.llm.bind_tools(self.tools)
            summary = llm_with_tools.invoke([{"role": "user", "content": prompt}])
        else:
            summary = self.llm.invoke([{"role": "user", "content": prompt}])
        state["summary"] = summary.content
        return state

    def tool_search(self, state):
        if not self.tools:
            state["tool_results"] = []
            return state

        tool = self.tools[0]
        user_message = state["messages"][-1] if state["messages"] else ""

        print("DEBUG: user_message type:", type(user_message))
        print("DEBUG: user_message value:", user_message)

        # Extract text from HumanMessage or dict
        query_text = None

        # Try to import HumanMessage if available
        try:
            from langchain_core.messages import HumanMessage
            is_human_message = isinstance(user_message, HumanMessage)
        except ImportError:
            is_human_message = False

        if is_human_message:
            query_text = user_message.content
        elif isinstance(user_message, dict) and "content" in user_message:
            query_text = user_message["content"]
        elif hasattr(user_message, "content"):
            query_text = user_message.content
        else:
            query_text = str(user_message)

        print("DEBUG: query_text to Tavily:", query_text)
        print("DEBUG: type passed to Tavily:", type({"query": query_text}))

        # Pass as dict to Tavily tool
        results = tool.run({"query": query_text})

        state["tool_results"] = results
        return state