# RAG Document Chatbot

## Project Overview

This project is a Retrieval-Augmented Generation (RAG)
system that answers questions using uploaded PDF documents.

It retrieves relevant document chunks from ChromaDB
and uses Google's Gemini API to generate grounded answers.

## Technologies Used

- Python
- Flask
- ChromaDB
- Sentence Transformers
- Gemini API
- PyPDF
- HTML, CSS, JavaScript

## Features

- PDF document ingestion
- Text extraction
- 500-token chunking with 80-token overlap
- Embedding generation
- Vector database storage
- Similarity-based document retrieval
- AI-powered question answering
- Source document and page references
- With RAG vs Without RAG comparison

## Project Structure

RAG-Document-Chatbot/
- app.py
- ingest.py
- rag.py
- requirements.txt
- documents/
- chroma_db/
- templates/
- static/

## Installation

1. Clone the repository.

2. Create a virtual environment.

3. Install dependencies:

   pip install -r requirements.txt

4. Add your Gemini API key to .env:

   GEMINI_API_KEY=your_api_key

5. Add PDF documents to the documents folder.

6. Run document ingestion:

   python ingest.py

7. Start the application:

   python app.py

8. Open http://127.0.0.1:5000

## RAG vs Without RAG

Question:
What is inheritance in Java?
<img width="953" height="454" alt="Screenshot 2026-11-09 163500" src="https://github.com/user-attachments/assets/86a3dd6f-fa71-4508-b153-2686377f48af" />
<img width="954" height="467" alt="Screenshot 2026-11-09 163918" src="https://github.com/user-attachments/assets/d87c1d3a-f537-4bc6-a757-a82b17c97fda" />
<img width="959" height="431" alt="Screenshot 2026-11-09 163924" src="https://github.com/user-attachments/assets/2b814c34-7de8-48b3-bf9b-4758ec2a065e" />


Without RAG:
**Inheritance in Java** is a fundamental concept of Object-Oriented Programming (OOP) that allows one class (the **subclass** or **child class**) to acquire the properties (fields) and behaviors (methods) of another class (the **superclass** or **parent class**).

It represents an **IS-A relationship** (e.g., a *Dog* **is an** *Animal*).

---

### Key Terminology

* **Superclass (Parent Class):** The class whose features are inherited.
* **Subclass (Child Class):** The class that inherits features from the superclass. It can reuse fields and methods from the parent and can also define its own new fields and methods.
* **`extends` Keyword:** The keyword used by a subclass to inherit from a superclass.

---

### Simple Example

```java
// Parent class
class Animal {
    void eat() {
        System.out.println("This animal eats food.");
    }
}

// Child class inherits from Animal
class Dog extends Animal {
    void bark() {
        System.out.println("The dog barks.");
    }
}

public class Main {
    public static void main(String[] args) {
        Dog myDog = new Dog();
        
        // Calling inherited method from Animal
        myDog.eat();  // Output: This animal eats food.
        
        // Calling child-specific method
        myDog.bark(); // Output: The dog barks.
    }
}
```

---

### Types of Inheritance Supported in Java

1. **Single Inheritance:** A class inherits from a single parent class.  
   *(Class B extends Class A)*
2. **Multilevel Inheritance:** A class inherits from a child class, forming a chain.  
   *(Class C extends Class B, and Class B extends Class A)*
3. **Hierarchical Inheritance:** Multiple classes inherit from a single parent class.  
   *(Class B extends Class A, and Class C extends Class A)*

> **Note on Multiple Inheritance:** Java does **not** support multiple inheritance with classes (i.e., a class cannot extend more than one class directly) to avoid ambiguity issues like the "Diamond Problem." However, multiple inheritance can be achieved in Java using **interfaces**.

---

### Why Use Inheritance?

* **Code Reusability:** You write common logic once in the superclass, and all subclasses inherit it without rewriting the code.
* **Method Overriding:** Allows a subclass to provide a specific implementation of a method that is already defined in its parent class (enabling **Runtime Polymorphism**).

---

### Important Rules to Remember

* **`java.lang.Object`:** Every class in Java implicitly inherits from the `Object` class, making it the root of the class hierarchy.
* **Private Members:** `private` fields and methods of a parent class are not directly accessible by the child class (though they can be accessed via `public` or `protected` getters/setters).
* **Constructors:** Constructors are not inherited, but a subclass constructor can call the parent class constructor using the `super()` keyword.

With RAG:
Based on the provided context, **inheritance** in Java allows a class to extend another class to reuse or specialize its behavior. 

Key points include:
* **Subclasses and the `extends` keyword:** The `extends` keyword is used to declare a subclass. 
* **Inherited members:** A subclass inherits accessible members from the parent class and can add new members or override inherited methods.
* **Single class inheritance:** Java classes have single class inheritance, meaning a class can directly extend only one class. 
* **Purpose:** It is useful for representing genuine subtype relationships.
Sources: java_oops.pdf, page 2 | java_oops.pdf, page 1 | java_oops.pdf, page 3 | java_introduction.pdf, page 1


## Author

Sakthinatchiyar K
