from src.utils.retriever import Retriever
from src.utils.generator import Generator

def main():
    # Initialize retriever and generator
    retriever = Retriever(index_dir="./index")   # adjust index_dir if needed
    generator = Generator()

    # Example question
    question = "How do I improve video intros?"

    # Step 1: Retrieve passages
    retrieved = retriever.retrieve(question, top_k=4)

    # Step 2: Generate answer
    answer = generator.generate_answer(question, retrieved)

    # Step 3: Print results
    
    print("Generated Answer:\n")
    print(answer)

if __name__ == "__main__":
    main()
