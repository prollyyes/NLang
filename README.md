# NLang
A natural language programming language.
# Aion: A Natural‑Language Programming Language for AI

## 1. Vision & Scope

Design a programming language that blends the readability of plain English with the precision of formal code, empowering both humans and AI systems to read, write, and reason about programs. Aion targets rapid prototyping of machine‑learning workflows, data manipulation, and agent orchestration while remaining general‑purpose.

## 2. Design Principles

1. **Natural Syntax ≥ Symbolic Syntax** – Core constructs use everyday words; symbols are optional.
2. **Single Source of Truth** – Every sentence is executable; no separate docstrings required.
3. **Explainability First** – Programs are self‑documenting and can be narrated step‑by‑step by an AI.
4. **Interoperability** – Transpiles to Python + popular ML libs (PyTorch, Transformers, sklearn).
5. **Gradual Formality** – Authors can start with fuzzy sentences and progressively refine.
6. **Conversational Workflow** – REPL accepts follow‑up questions (“Why did accuracy drop?”) and emits answers.

## 3. Core Linguistic Metaphor

| English part               | Aion concept             | Example                                           |
| -------------------------- | ------------------------ | ------------------------------------------------- |
| **Nouns**                  | *Entities*               | *dataset*, *model*, *tensor*, *file*              |
| **Verbs**                  | *Actions*                | *load*, *train*, *predict*, *visualise*           |
| **Adjectives/Adverbs**     | *Qualifiers*             | *robust*, *quickly*, *deterministic*              |
| **Prepositions & Clauses** | *Relations / Conditions* | *from csv “iris.csv”*, *if accuracy > 90 percent* |

Sentences combine these parts to form executable instructions.

## 4. Lexical & Formatting Rules

* Case‑insensitive keywords (`train`, `Train`, and `TRAIN` are equivalent).
* Sentences end with a period **or** newline. Commas separate clauses.
* Indentation indicates hierarchy within multi‑step blocks, mirroring Python’s significance of whitespace.
* Comments start with `#` anywhere in a line.

## 5. Basic Sentence Patterns

### 5.1 Declarations

```
Let learning‑rate be 3e‑4.
Start with list items [1, 2, 3].
```

### 5.2 Functions ("Procedures")

```
To square a number n: return n multiplied by n.
```

Plain‑language verbs *To*, *Given*, *Return* introduce the definition body.

### 5.3 Control Flow

```
If accuracy exceeds 90 percent, announce "We did it!".
Otherwise, lower learning‑rate by half and train again.
```

### 5.4 Loops

```
For each record in validation‑set:
    predict label using network.
    count correct predictions.
```

## 6. Data & AI‑Specific Types

* **Number** – int or float detected from context.
* **Text** – unicode string.
* **Boolean** – true/false.
* **List / Table** – ordered / tabular collections.
* **Tensor** – n‑dimensional numeric array.
* **Dataset** – wrapper around data source with schema.
* **Model** – trainable object exposing `fit`, `predict`, `save`.
* **Prompt** – text template + variables.

Type names double as constructors: `Dataset from csv "iris.csv".`

## 7. Built‑in AI Verbs

| Verb Phrase             | Effect                     |
| ----------------------- | -------------------------- |
| `load dataset from …`   | Reads data into memory.    |
| `define model as …`     | Instantiates architecture. |
| `train model with …`    | Calls underlying `.fit`.   |
| `evaluate model on …`   | Returns metrics struct.    |
| `generate text using …` | Calls language model.      |
| `save model to …`       | Persists weights.          |

These verbs map directly to library calls after transpilation.

## 8. Conversational REPL

Aion shells maintain program state. Users (or another AI) can ask:

> *Why did loss plateau after epoch 3?*

The runtime introspects variables and responds in natural language.

## 9. Error Handling & Suggestions

Runtime messages use friendly English:

```
I couldn’t find a variable called "learning‑rate". Did you mean "lr"?
```

When running under an LLM‑enhanced environment, the interpreter proposes fixes.

## 10. Transpilation Pipeline

1. **NL Parser** – Converts sentences to an Abstract Syntax Tree (AST) using a context‑free grammar plus optional LLM disambiguation.
2. **Semantic Pass** – Resolves references and infers types.
3. **Code Generator** – Emits Python (or other backend) with explicit imports.
4. **Executor** – Runs and streams outputs back into the REPL.

## 11. Sample Program (Iris classifier)

```
Load dataset iris from csv "iris.csv". Split it into train as 80 percent and test as 20 percent.
Define model as random‑forest with 100 trees and max‑depth 5.
Train model with train. Evaluate model on test, calling the score accuracy.
If accuracy is at least 95 percent, say "Success!". Otherwise, enlarge the forest to 300 trees and train again.
```

Transpiles to \~25 lines of Python using scikit‑learn.

## 12. Extensibility

* **Domain Packs** – YAML/JSON files declare new nouns/verbs.
* **Inline DSL** – Embed SQL or Bash blocks guarded by `shell or `sql fences.
* **Plugins** – Custom AST nodes compiled to user‑supplied Python.

## 13. Security & Sandboxing

By default the interpreter runs inside a restricted container, limiting filesystem and network. Dangerous actions require explicit `allow` clauses: `allow network access to "huggingface.co".`
***
