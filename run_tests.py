from agent import graph

def run_tests(file_path="test_cases.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        test_cases = [line.strip() for line in f if line.strip()]

    print("=" * 60)
    print("RUNNING TEST CASES")
    print("=" * 60)

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}")
        print(f"User: {test}")
        print("Agent đang suy nghĩ...")

        result = graph.invoke({
            "messages": [("human", test)]
        })

        final = result["messages"][-1]

        print(f"Agent: {final.content}")
        print("-" * 50)


if __name__ == "__main__":
    run_tests()