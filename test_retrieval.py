from rag import retrieve_documents

question = "What is inheritance in Java?"

results = retrieve_documents(question)

print("\nQUESTION:", question)

print("\nRETRIEVED DOCUMENTS:")

for result in results:
    print("\nSource:", result["source"])
    print("Page:", result["page"])
    print("Content:", result["text"])