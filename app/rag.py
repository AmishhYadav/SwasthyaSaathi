import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings as HuggingFaceEmbeddings

# Load .env file from project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

DB_PATH = "data/faiss_index"

# Custom prompt: use the retrieved context if helpful, otherwise use your own knowledge.
# Always add a medical disclaimer.
HYBRID_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are SwasthyaSathi, an AI public health assistant for India.
Your role is to provide accurate, helpful health information to users.

Use the following retrieved context to answer the question. If the context is relevant, 
prioritize it. If the context does NOT contain enough information to fully answer the 
question, use your own medical knowledge to provide a helpful, accurate answer.

Retrieved Context:
{context}

User Question: {question}

Instructions:
- Answer clearly in simple language that a common person can understand.
- If the question is about medicines, include price comparisons and Jan Aushadhi availability when relevant.
- If the question is about a disease, cover symptoms, prevention, and when to see a doctor.
- If asked about symptoms, suggest possible conditions but emphasize seeing a doctor for diagnosis.
- Be concise but thorough.

⚠️ DISCLAIMER: This information is for educational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

Answer:"""
)


def get_faq_agent():
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        if not api_key:
            print("Error: API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY in .env")
            return None

        # Local embeddings for retrieval
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        os.environ["GOOGLE_API_KEY"] = api_key

        model_names = ["gemini-2.5-flash"]

        llm = None
        last_error = None

        for model_name in model_names:
            try:
                print(f"Attempting to initialize model: {model_name}")
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=0.3,
                    google_api_key=api_key
                )
                print(f"✅ Successfully initialized with model: {model_name}")
                break
            except Exception as e:
                error_str = str(e)
                last_error = e
                if "404" in error_str or "not found" in error_str.lower():
                    print(f"❌ Model {model_name} not available")
                else:
                    print(f"❌ Failed to initialize {model_name}: {error_str[:150]}")
                continue

        if llm is None:
            raise Exception(f"Failed to initialize any model. Last error: {last_error}")

        # Build the hybrid RAG chain with our custom prompt
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": HYBRID_PROMPT},
        )
        return qa
    except Exception as e:
        print(f"Error initializing RAG agent: {e}")
        import traceback
        traceback.print_exc()
        return None
