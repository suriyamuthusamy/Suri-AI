import time


def print_sources(results):
    print("\n📚 Sources:")

    for i, result in enumerate(results, 1):
        title = result.get("title", "No Title")
        url = result.get("url", "No URL")

        print(f"\n{i}. {title}")
        print(f"   {url}")


def print_response_time(start_time):
    end_time = time.time()
    print(f"\n⏱ Response Time: {end_time - start_time:.2f} seconds")
    print("-" * 60)