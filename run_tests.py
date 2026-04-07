from agent import graph

def run_tests(file_path="test_cases.txt", output_file="test_results.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        test_cases = [line.strip() for line in f if line.strip()]

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# Test Results\n\n")

        for i, test in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test}")

            result = graph.invoke({
                "messages": [("human", test)]
            })

            final = result["messages"][-1]

            # Ghi ra file giống console log
            out.write(f"## Test {i}\n")
            out.write(f"**User:** {test}\n\n")
            out.write(f"**Agent:** {final.content}\n\n")
            out.write("---\n\n")

    print(f"\nĐã xuất kết quả ra {output_file}")


if __name__ == "__main__":
    run_tests()